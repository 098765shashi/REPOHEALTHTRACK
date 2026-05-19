from collections import defaultdict
from datetime import datetime

def commit_timeline(commits):
    buckets = defaultdict(int)
    for c in commits:
        ts = c["timestamp"][:10]
        buckets[ts] += 1
    return [{"date": d, "commits": n} for d, n in sorted(buckets.items())]
