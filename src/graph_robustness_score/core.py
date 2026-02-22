import networkx as nx
import numpy as np
from typing import Tuple

def compute_cg(
    G: nx.Graph,
    weights: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> float:
    """Compute Graph Robustness Score C(G) — exact match to app.py demo."""
    if G.number_of_nodes() < 2:
        return 0.0

    # Adjacency matrix (exactly as in your app.py)
    A = nx.adjacency_matrix(G).todense()

    # Spectral gap
    ev = np.linalg.eigvals(A)
    real_ev = np.real(ev)
    lambda_max = np.max(real_ev)
    sorted_ev = sorted(real_ev, reverse=True)
    lambda_next = sorted_ev[1] if len(sorted_ev) > 1 else 0.0
    spectral_gap = lambda_max - lambda_next

    # Singular-value variance
    sigma = np.linalg.svd(A, compute_uv=False)
    sing_var = np.var(sigma)

    # Clustering proxy (exactly as demo)
    clustering = nx.average_clustering(G)
    curvature_proxy = clustering * 10.0

    w1, w2, w3 = weights
    score = w1 * spectral_gap - w2 * sing_var + w3 * curvature_proxy
    return float(score)


def compute_cg_after_attack(
    G: nx.Graph, fraction: float = 0.2, targeted: bool = False
) -> float:
    """Simulate 20% edge removal (random or targeted) and return new C(G)."""
    G_attack = G.copy()
    edges = list(G_attack.edges())
    remove_count = max(1, int(fraction * len(edges)))

    if targeted:
        # Targeted: remove edges from highest-degree nodes
        deg = sorted(G_attack.degree(), key=lambda x: x[1], reverse=True)
        to_remove = []
        for node, _ in deg:
            for neigh in list(G_attack.neighbors(node)):
                if len(to_remove) < remove_count:
                    to_remove.append((node, neigh))
                else:
                    break
            if len(to_remove) >= remove_count:
                break
        G_attack.remove_edges_from(to_remove[:remove_count])
    else:
        # Random removal
        np.random.shuffle(edges)
        G_attack.remove_edges_from(edges[:remove_count])

    return compute_cg(G_attack)
