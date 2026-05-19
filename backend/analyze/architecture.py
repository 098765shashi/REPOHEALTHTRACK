"""Detect circular deps in import graph."""
import networkx as nx

def detect_cycles(graph: nx.DiGraph):
    try:
        cycles = list(nx.simple_cycles(graph))
        return [c for c in cycles if len(c) > 1][:20]
    except Exception:
        return []
