def hotspots(complexity: dict, churn: dict, n: int = 20):
    out = []
    for f, cx in complexity.items():
        ch = churn.get(f, 0)
        score = cx * (1 + ch)
        out.append({"file": f, "complexity": round(cx, 2), "churn": ch, "score": round(score, 2)})
    return sorted(out, key=lambda x: -x["score"])[:n]
