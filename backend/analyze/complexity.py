"""Cyclomatic complexity via Radon (Python). Heuristic for other langs."""
import os
from radon.complexity import cc_visit

def file_complexity(path: str) -> float:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            src = f.read()
        if path.endswith(".py"):
            blocks = cc_visit(src)
            return sum(b.complexity for b in blocks) or 1.0
        # heuristic: branching keywords
        kw = ["if ", "for ", "while ", "case ", "switch ", "catch ", "&& ", "|| ", "elif "]
        return float(1 + sum(src.count(k) for k in kw))
    except Exception:
        return 1.0

def repo_complexity(root: str):
    out = {}
    for dirpath, _, files in os.walk(root):
        if "/.git" in dirpath or "node_modules" in dirpath: continue
        for fn in files:
            if not fn.lower().endswith((".py",".js",".jsx",".ts",".tsx",".java")): continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            out[rel] = file_complexity(p)
    return out
