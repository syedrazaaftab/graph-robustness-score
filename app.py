import streamlit as st
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Graph Robustness Score",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Graph Robustness Score C(G)")
st.markdown("""
**One clean number** that tells you how robust any network is.  
Spectral gap − singular-value variance + Ollivier–Ricci curvature (demo version)
""")

# ====================== SAMPLE GRAPHS ======================
st.subheader("Try sample graphs")
col1, col2 = st.columns(2)

with col1:
    if st.button("Try triangle (3 nodes)", use_container_width=True):
        sample_csv = "1,2\n1,3\n2,3"
        G = nx.read_edgelist(StringIO(sample_csv), delimiter=",", nodetype=int)
        st.session_state.G = G
        st.success("✅ Triangle graph loaded! (3 nodes, 3 edges)")

with col2:
    if st.button("Try scale-free (Barabási–Albert)", use_container_width=True):
        G = nx.barabasi_albert_graph(n=50, m=3, seed=42)
        st.session_state.G = G
        st.success("✅ Scale-free network (50 nodes) loaded!")

# ====================== UPLOAD (header-robust) ======================
st.subheader("Or upload your own edgelist")
uploaded_file = st.file_uploader(
    "CSV file — **optional header** accepted (source,target or from,to). One edge per line otherwise.",
    type=["csv"]
)

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8").strip()
    lines = content.splitlines()
    if lines and any(x in lines[0].lower() for x in ["source", "target", "from", "to", "node"]):
        lines = lines[1:]
    clean_csv = "\n".join(lines)
    try:
        G = nx.read_edgelist(StringIO(clean_csv), delimiter=",", nodetype=int)
        st.session_state.G = G
        st.success(f"✅ Upload successful: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")

if 'G' not in st.session_state:
    st.info("👆 Click a sample button or upload a CSV to begin")
    st.stop()

G = st.session_state.G

# ====================== COMPUTE C(G) ======================
st.success(f"Graph ready: **{G.number_of_nodes()} nodes**, **{G.number_of_edges()} edges**")

# FIXED: Use pure-numpy version (no scipy needed)
A = nx.to_numpy_array(G)                    # ← THIS WAS THE FIX
ev = np.linalg.eigvals(A)
lambda_max = np.max(np.real(ev))
lambda_next = sorted(np.real(ev), reverse=True)[1] if len(ev) > 1 else 0
delta = lambda_max - lambda_next

sigma = np.linalg.svd(A, compute_uv=False)
var_sigma = np.var(sigma)
kappa_approx = nx.average_clustering(G)     # demo approximation

C = delta - var_sigma + kappa_approx * 10   # scaled for visibility

st.metric("**Your C(G) Score**", f"{C:.3f}")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Spectral Gap Δλ", f"{delta:.3f}")
with col2: st.metric("Singular-Value Variance", f"{var_sigma:.3f}")
with col3: st.metric("Curvature (approx)", f"{kappa_approx:.3f}")

# ====================== ATTACK SIMULATION ======================
st.subheader("Attack Simulation")
st.caption("See how robust your graph is: remove 20% of edges randomly or targeting hubs")

if st.button("Remove 20% random edges"):
    G_random = G.copy()
    edges = list(G_random.edges())
    remove_count = max(1, int(0.2 * len(edges)))
    np.random.shuffle(edges)
    G_random.remove_edges_from(edges[:remove_count])
    st.session_state.G_attack = G_random
    st.success("20% random edges removed")

if st.button("Remove 20% highest-degree (hub) edges"):
    G_hub = G.copy()
    degree = dict(G_hub.degree())
    sorted_nodes = sorted(degree, key=degree.get, reverse=True)
    remove_count = max(1, int(0.2 * G_hub.number_of_edges()))
    edges_to_remove = []
    for node in sorted_nodes:
        for neigh in list(G_hub.neighbors(node)):
            if len(edges_to_remove) < remove_count:
                edges_to_remove.append((node, neigh))
    G_hub.remove_edges_from(edges_to_remove)
    st.session_state.G_attack = G_hub
    st.success("20% hub-targeted edges removed")

if 'G_attack' in st.session_state:
    G_attack = st.session_state.G_attack
    A2 = nx.to_numpy_array(G_attack)        # ← FIXED HERE TOO
    ev2 = np.linalg.eigvals(A2)
    d2 = np.max(np.real(ev2)) - (sorted(np.real(ev2), reverse=True)[1] if len(ev2) > 1 else 0)
    v2 = np.var(np.linalg.svd(A2, compute_uv=False))
    k2 = nx.average_clustering(G_attack)
    C2 = d2 - v2 + k2 * 10

    fig, ax = plt.subplots(figsize=(8, 4))
    labels = ['Original', 'Random removal', 'Hub removal']
    scores = [C, C2, C2]
    colors = ['#4CAF50', '#FF9800', '#F44336']
    ax.bar(labels, scores, color=colors)
    ax.set_ylabel('C(G) Score')
    ax.set_title('Robustness Drop Under Attack')
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)

st.info("📦 **Full version** (exact Ollivier–Ricci + weight sliders) is in the ZIP below.")

st.markdown("[⬇️ Download full package + paper + code](https://github.com/syedrazaaftab/graph-robustness-score/raw/main/computational-testbed.zip)")

st.caption("Built with C(G) by Syed Raza Aftab • Princeton Meadows, NJ  \n"
           "Email for paid audits: aftab011190@gmail.com")
