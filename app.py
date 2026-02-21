import streamlit as st
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# Real Ollivier-Ricci
try:
    from GraphRicciCurvature.OllivierRicci import OllivierRicci
    REAL_CURVATURE = True
except ImportError:
    REAL_CURVATURE = False

st.set_page_config(page_title="Graph Robustness Score", page_icon="🧠", layout="centered")

st.title("🧠 Graph Robustness Score C(G)")
st.markdown("""
**One clean number** that tells you how robust any network is.  
Spectral gap − singular-value variance + Ollivier–Ricci curvature
""")

# ====================== SAMPLE GRAPHS ======================
st.subheader("Try sample graphs")
col1, col2 = st.columns(2)

with col1:
    if st.button("Try triangle (3 nodes)", use_container_width=True):
        G = nx.complete_graph(3)
        st.session_state.G = G
        st.success("✅ Triangle loaded (3 nodes, 3 edges)")

with col2:
    if st.button("Try scale-free (50 nodes)", use_container_width=True):
        G = nx.barabasi_albert_graph(50, 3, seed=42)
        st.session_state.G = G
        st.success("✅ Scale-free network loaded")

# ====================== UPLOAD ======================
st.subheader("Or upload your own edgelist")
uploaded = st.file_uploader("CSV — optional header accepted", type=["csv"])
if uploaded:
    content = uploaded.read().decode().strip()
    lines = content.splitlines()
    if lines and any(x in lines[0].lower() for x in ["source","target","from","to"]):
        lines = lines[1:]
    try:
        G = nx.read_edgelist(StringIO("\n".join(lines)), delimiter=",", nodetype=int)
        st.session_state.G = G
        st.success(f"✅ Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        st.error(f"Parse error: {e}")

if 'G' not in st.session_state:
    st.info("👆 Click a sample or upload a CSV to begin")
    st.stop()

G = st.session_state.G

# ====================== WEIGHTS ======================
st.subheader("Adjust weights")
c1, c2, c3 = st.columns(3)
w1 = c1.slider("Spectral gap (w₁)", 0.0, 3.0, 1.0, 0.1)
w2 = c2.slider("Variance penalty (w₂)", 0.0, 3.0, 1.0, 0.1)
w3 = c3.slider("Curvature (w₃)", 0.0, 3.0, 1.0, 0.1)

# ====================== COMPUTE ======================
A = nx.to_numpy_array(G)
ev = np.linalg.eigvals(A)
delta = np.max(np.real(ev)) - (sorted(np.real(ev), reverse=True)[1] if len(ev) > 1 else 0)
var_sigma = np.var(np.linalg.svd(A, compute_uv=False))

if REAL_CURVATURE and G.number_of_edges() > 0:
    with st.spinner("Computing real Ollivier–Ricci curvature..."):
        orc = OllivierRicci(G, alpha=0.5, method="Sinkhorn", verbose="ERROR")
        orc.compute_ricci_curvature()
        kappa = np.mean(list(nx.get_edge_attributes(orc.G, "ricciCurvature").values()))
else:
    kappa = nx.average_clustering(G)

C = w1 * delta - w2 * var_sigma + w3 * kappa

st.metric("**C(G) Score**", f"{C:.4f}")
col1, col2, col3 = st.columns(3)
col1.metric("Spectral Gap Δλ", f"{delta:.4f}")
col2.metric("Singular-Value Var", f"{var_sigma:.4f}")
col3.metric("Avg Ollivier–Ricci κ", f"{kappa:.4f}")

# ====================== ATTACK SIMULATION (fixed) ======================
st.subheader("Attack Simulation")
if st.button("Remove 20% random edges"):
    Gr = G.copy()
    edges = list(Gr.edges())
    np.random.shuffle(edges)
    Gr.remove_edges_from(edges[:max(1, int(0.2 * len(edges)))])
    st.session_state.G_random = Gr
    st.success("Random attack done")

if st.button("Remove 20% hub edges"):
    Gh = G.copy()
    deg = sorted(Gh.degree(), key=lambda x: x[1], reverse=True)
    remove_count = max(1, int(0.2 * Gh.number_of_edges()))
    to_remove = []
    for node, _ in deg:
        for neigh in list(Gh.neighbors(node)):
            if len(to_remove) < remove_count:
                to_remove.append((node, neigh))
    Gh.remove_edges_from(to_remove)
    st.session_state.G_hub = Gh
    st.success("Hub attack done")

# ====================== PLOT (dynamic - only shows run attacks) ======================
if 'G_random' in st.session_state or 'G_hub' in st.session_state:
    st.subheader("Robustness Drop Under Attack")
    labels = ["Original"]
    scores = [C]
    colors = ["#4CAF50"]

    for name, key, color in [("Random", "G_random", "#FF9800"), ("Hub", "G_hub", "#F44336")]:
        if key in st.session_state:
            Ga = st.session_state[key]
            Aa = nx.to_numpy_array(Ga)
            da = np.max(np.real(np.linalg.eigvals(Aa))) - (sorted(np.real(np.linalg.eigvals(Aa)), reverse=True)[1] if len(Aa) > 1 else 0)
            va = np.var(np.linalg.svd(Aa, compute_uv=False))
            if REAL_CURVATURE and Ga.number_of_edges() > 0:
                orca = OllivierRicci(Ga, alpha=0.5, method="Sinkhorn", verbose="ERROR")
                orca.compute_ricci_curvature()
                ka = np.mean(list(nx.get_edge_attributes(orca.G, "ricciCurvature").values()))
            else:
                ka = nx.average_clustering(Ga)
            Ca = w1 * da - w2 * va + w3 * ka
            labels.append(name)
            scores.append(Ca)
            colors.append(color)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, scores, color=colors)
    ax.set_ylabel("C(G) Score")
    ax.set_title("How robust is your graph?")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

st.info("📦 Full reproducible package (paper + experiments) → [Download ZIP](https://github.com/syedrazaaftab/graph-robustness-score/raw/main/computational-testbed.zip)")

st.caption("Built by Syed Raza Aftab • Princeton Meadows, NJ\n"
           "Paid network robustness audits available — email: aftab011190@gmail.com")
