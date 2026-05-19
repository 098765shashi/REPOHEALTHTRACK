"""Clone a repo and walk commits using GitPython."""
import os, tempfile, shutil
from collections import defaultdict
from datetime import datetime
from git import Repo

def clone_repo(url: str, branch: str = "main") -> str:
    tmp = tempfile.mkdtemp(prefix="repohealth-")
    try:
        Repo.clone_from(url, tmp, branch=branch, depth=500)
    except Exception:
        # fallback default branch
        shutil.rmtree(tmp, ignore_errors=True)
        tmp = tempfile.mkdtemp(prefix="repohealth-")
        Repo.clone_from(url, tmp, depth=500)
    return tmp

def walk_commits(path: str, max_commits: int = 500):
    repo = Repo(path)
    commits = []
    file_churn = defaultdict(int)
    file_authors = defaultdict(lambda: defaultdict(int))
    author_commits = defaultdict(int)
    for i, c in enumerate(repo.iter_commits()):
        if i >= max_commits: break
        author = (c.author.name or "unknown").strip()
        author_commits[author] += 1
        stats = c.stats.files
        for f, s in stats.items():
            changes = s.get("insertions", 0) + s.get("deletions", 0)
            file_churn[f] += changes
            file_authors[f][author] += changes
        commits.append({
            "sha": c.hexsha[:10],
            "author": author,
            "timestamp": datetime.fromtimestamp(c.committed_date).isoformat(),
            "message": c.message.strip().splitlines()[0][:200] if c.message else "",
            "files_changed": len(stats),
        })
    return {
        "commits": commits,
        "file_churn": dict(file_churn),
        "file_authors": {k: dict(v) for k, v in file_authors.items()},
        "author_commits": dict(author_commits),
    }
