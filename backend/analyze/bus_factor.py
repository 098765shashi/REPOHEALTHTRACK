def bus_factor(author_commits: dict, threshold: float = 0.5):
    if not author_commits: return {"bus_factor": 0, "risk": 1.0}
    items = sorted(author_commits.items(), key=lambda kv: -kv[1])
    total = sum(v for _, v in items) or 1
    cum, count = 0, 0
    for _, v in items:
        cum += v; count += 1
        if cum / total >= threshold: break
    risk = max(0.0, 1.0 - (count - 1) / 4)  # 1 contributor=1.0, 5+=0.0
    return {"bus_factor": count, "risk": round(min(1.0, risk), 3), "top_contributors": items[:10]}
