"""Schema reference: Developer -> Commit -> File -> Function (logical model)."""
SCHEMA = {
    "nodes": ["Developer", "Commit", "File", "Function"],
    "edges": [
        ("Developer", "AUTHORED", "Commit"),
        ("Commit", "TOUCHED", "File"),
        ("File", "CONTAINS", "Function"),
        ("File", "IMPORTS", "File"),
    ],
}
