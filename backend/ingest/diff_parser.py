"""Parses commit diffs to extract per-file change magnitudes."""
def summarize_churn(file_churn: dict, top_n: int = 20):
    return sorted(file_churn.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
