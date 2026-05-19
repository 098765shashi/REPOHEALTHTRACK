"""Coupling: files that change together frequently."""
from collections import defaultdict

def co_change(commits_files: list, top: int = 15):
    """commits_files: list of file-sets (one per commit)."""
    pair = defaultdict(int)
    for files in commits_files:
        files = list(set(files))
        for i in range(len(files)):
            for j in range(i+1, len(files)):
                a, b = sorted([files[i], files[j]])
                pair[(a, b)] += 1
    items = sorted(pair.items(), key=lambda kv: -kv[1])[:top]
    return [{"a": a, "b": b, "count": c} for (a, b), c in items if c > 1]
