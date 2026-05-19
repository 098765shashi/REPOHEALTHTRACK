"""Builds a NetworkX graph of file -> imported module."""
import os, networkx as nx
from ingest.ast_extractor import extract_imports
from ingest.language_detector import detect

def build_import_graph(root: str):
    g = nx.DiGraph()
    for dirpath, _, files in os.walk(root):
        if "/.git" in dirpath or "node_modules" in dirpath: continue
        for fn in files:
            p = os.path.join(dirpath, fn)
            lang = detect(p)
            if not lang: continue
            rel = os.path.relpath(p, root)
            g.add_node(rel, lang=lang)
            for imp in extract_imports(p):
                g.add_edge(rel, imp)
    return g

def graph_to_json(g, max_nodes: int = 200):
    nodes = list(g.nodes(data=True))[:max_nodes]
    names = {n for n, _ in nodes}
    return {
        "nodes": [{"id": n, "lang": d.get("lang", "")} for n, d in nodes],
        "edges": [{"source": u, "target": v} for u, v in g.edges() if u in names and v in names][:1000],
    }
