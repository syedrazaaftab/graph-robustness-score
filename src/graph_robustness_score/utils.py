import networkx as nx
from io import StringIO

def graph_from_edgelist(csv_string: str) -> nx.Graph:
    """Load graph from CSV edge list string (for future use)."""
    return nx.read_edgelist(StringIO(csv_string), delimiter=",", nodetype=str)
