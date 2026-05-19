"""OpenAI-powered narrative. Falls back to template if no key."""
import os, json
from openai import OpenAI

def generate_report(repo_name: str, metrics: dict, health: dict) -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    summary_input = {
        "repo": repo_name,
        "health": health,
        "top_hotspots": metrics.get("hotspots", [])[:5],
        "bus_factor": metrics.get("bus_factor", {}),
        "cycles_count": len(metrics.get("cycles", [])),
        "top_authors": metrics.get("author_ownership", [])[:5],
    }
    if not key or key.startswith("sk-your"):
        return _fallback(summary_input)
    try:
        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a senior engineering manager. Write a crisp executive summary of repository health: 4 short paragraphs covering overall health, hotspots, contributor risk, and recommendations. Be specific, use the numbers."},
                {"role": "user", "content": json.dumps(summary_input)},
            ],
            temperature=0.4,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return _fallback(summary_input) + f"\n\n_(AI fallback: {e})_"

def _fallback(s):
    h = s["health"]
    bf = s["bus_factor"].get("bus_factor", "?")
    return (
        f"**Health: {h['score']}/100 ({h['level']})** — composite score blending complexity, hotspot, bus-factor, and dependency risk.\n\n"
        f"**Hotspots**: top {len(s['top_hotspots'])} files concentrate complexity and churn — prioritize refactoring there.\n\n"
        f"**Contributors**: bus factor of {bf} signals "
        f"{'concentration risk — onboard reviewers' if isinstance(bf,int) and bf<=2 else 'reasonable distribution'}.\n\n"
        f"**Architecture**: {s['cycles_count']} circular dependency cluster(s) detected. Break cycles to improve testability."
    )
