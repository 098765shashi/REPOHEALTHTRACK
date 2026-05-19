def top_churn(file_churn: dict, n: int = 20):
    return sorted(file_churn.items(), key=lambda x: x[1], reverse=True)[:n]
