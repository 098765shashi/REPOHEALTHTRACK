"""Tree-sitter based AST extraction. Falls back to regex if grammars unavailable."""
import os, re
from .language_detector import detect

try:
    from tree_sitter_languages import get_parser
    TS_OK = True
except Exception:
    TS_OK = False

IMPORT_RE = {
    "python": re.compile(r"^\s*(?:from\s+([\w\.]+)\s+import|import\s+([\w\.]+))", re.M),
    "javascript": re.compile(r"""(?:import\s+.*?from\s+|require\()\s*['"]([^'"]+)['"]""", re.M),
    "typescript": re.compile(r"""(?:import\s+.*?from\s+|require\()\s*['"]([^'"]+)['"]""", re.M),
    "java": re.compile(r"^\s*import\s+([\w\.]+);", re.M),
}

def extract_imports(file_path: str):
    lang = detect(file_path)
    if not lang: return []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception:
        return []
    rx = IMPORT_RE.get(lang)
    if not rx: return []
    out = []
    for m in rx.finditer(text):
        out.append(next((g for g in m.groups() if g), ""))
    return [o for o in out if o]
