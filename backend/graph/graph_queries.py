import networkx as nx
def most_central(g, n=10):
    if not g.nodes: return []
    try:
        c = nx.degree_centrality(g)
        return sorted(c.items(), key=lambda kv: -kv[1])[:n]
    except Exception:
        return []
