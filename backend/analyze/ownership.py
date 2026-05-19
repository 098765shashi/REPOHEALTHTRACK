def ownership(file_authors: dict):
    out = {}
    for f, authors in file_authors.items():
        total = sum(authors.values()) or 1
        top_author, top = max(authors.items(), key=lambda kv: kv[1])
        out[f] = {"top_author": top_author, "share": round(top/total, 3), "contributors": len(authors)}
    return out

def author_ownership(file_authors: dict):
    totals = {}
    for f, authors in file_authors.items():
        for a, v in authors.items():
            totals[a] = totals.get(a, 0) + v
    s = sum(totals.values()) or 1
    return [{"author": a, "share": round(v/s, 3), "lines": v} for a, v in sorted(totals.items(), key=lambda x:-x[1])]
