def normalize(value, lo=0, hi=1):
    if value <= lo: return 0.0
    if value >= hi: return 1.0
    return (value - lo) / (hi - lo)

def compute_health(metrics: dict) -> dict:
    cx_values = list(metrics.get("complexity", {}).values()) or [1]
    avg_cx = sum(cx_values) / len(cx_values)
    complexity_risk = normalize(avg_cx, 3, 25)

    hotspots = metrics.get("hotspots", [])
    top_hs = sum(h["score"] for h in hotspots[:5])
    hotspot_risk = normalize(top_hs, 50, 2000)

    bus = metrics.get("bus_factor", {}).get("risk", 0.5)
    bus_factor_risk = bus

    cycles = metrics.get("cycles", [])
    dependency_risk = normalize(len(cycles), 0, 10)

    score = 100 - (0.30*complexity_risk + 0.20*hotspot_risk + 0.20*bus_factor_risk + 0.30*dependency_risk) * 100
    score = max(0.0, min(100.0, round(score, 1)))
    level = "excellent" if score >= 85 else "good" if score >= 70 else "fair" if score >= 50 else "at-risk"
    return {
        "score": score,
        "level": level,
        "breakdown": {
            "complexity_risk": round(complexity_risk, 3),
            "hotspot_risk": round(hotspot_risk, 3),
            "bus_factor_risk": round(bus_factor_risk, 3),
            "dependency_risk": round(dependency_risk, 3),
        },
    }
