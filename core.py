import networkx as nx
import numpy as np
from typing import Tuple

def compute_cg(
    G: nx.Graph,
    weights: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> float:
    """Exact C(G) from your live Streamlit app."""
    if G.number_of_nodes() < 2:
        return 0.0

    A = nx.adjacency_matrix(G).todense()

    ev = np.real(np.linalg.eigvals(A))
    ev_sorted = np.sort(ev)[::-1]
    spectral_gap = ev_sorted[0] - ev_sorted[1] if len(ev_sorted) > 1 else ev_sorted[0]

    sigma = np.linalg.svd(A, compute_uv=False)
    sing_var = np.var(sigma)

    clustering = nx.average_clustering(G)
    curvature_proxy = clustering * 10.0

    w1, w2, w3 = weights
    score = w1 * spectral_gap - w2 * sing_var + w3 * curvature_proxy
    return float(score)
