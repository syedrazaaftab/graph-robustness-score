import streamlit as st
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# Real Ollivier-Ricci
try:
    from GraphRicciCurvature.OllivierRicci import OllivierRicci
    REAL_CURVATURE_AVAILABLE = True
except ImportError:
    REAL_CURVATURE_AVAILABLE = False

# ====================== PAGE CONFIG ======================
st.set_page_config(page_title="Graph Robustness Score", page_icon="🧠", layout="centered")

st.title("🧠 Graph Robustness Score C(G)")
st.markdown("""
**One clean number** that tells you how robust any network is.  
Spectral gap − singular-value variance + Ollivier–Ricci curvature  
**✓ Full version** (real curvature, weight sliders)
""")

# ====================== SAMPLE GRAPHS ======================
st.subheader("Try sample graphs")
col1, col2 = st.columns(2)

with col1:
    if st.button("Try triangle (3 nodes)", use_container_width=True):
        sample_csv = "1,2\n1,3\n2,3"
        G = nx.read_edgelist(StringIO(sample_csv), delimiter=",", nodetype=int)
        st.session_state.G = G
        st.success("✅ Triangle loaded!")

with col2:
    if st.button("Try scale-free (Barabási–Albert)", use_container_width=True):
        G = nx.barabasi_albert_graph(n=50, m=3, seed=42)
        st.session_state.G = G
        st.success("✅ Scale-free (50 nodes) loaded!")

# ====================== UPLOAD ======================
st.subheader("Or upload your own edgelist")
uploaded_file = st.file_uploader(
    "CSV — optional header (source,target or from,to). One edge per line.",
    type=["csv"]
)

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8").strip()
    lines = content.splitlines()
    if lines and any(x in lines[0].lower() for x in ["source","target","from","to","node"]):
        lines = lines[1:]
    clean_csv = "\n".join(lines)
    try:
        G = nx.read_edgelist(StringIO(clean_csv), delimiter=",", nodetype=int)
        st.session_state.G = G
        st.success(f"✅ {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        st.error(f"Parse error: {e}")

if 'G' not in st.session_state:
    st.info("👆 Click a sample or upload to begin")
    st.stop()

G = st.session_state.G

# ====================== WEIGHT SLIDERS ======================
st.subheader("Weights (w₁, w₂, w₃)")
col1, col2, col3 = st.columns(3)
w1 = col1.slider("Spectral gap weight", 0.0, 3.0, 1.0, 0.1)
w2 = col2.slider("Variance penalty weight", 0.0, 3.0, 1.0, 0.1)
w3 = col3.slider("Curvature weight", 0.0, 3.0, 1.0, 0.1)

# ====================== COMPUTE C(G) WITH REAL CURVATURE ======================
st.success(f"Graph ready: **{G.number_of_nodes()} nodes**, **{G.number_of_edges()} edges**")

A = nx.to_numpy_array(G)
ev = np.linalg.eigvals(A)
lambda_max = np.max(np.real(ev))
lambda_next = sorted(np.real(ev), reverse=True)[1] if len(ev) > 1 else 0
delta = lambda_max - lambda_next

sigma = np.linalg.svd(A, compute_uv=False)
var_sigma = np.var(sigma)

# REAL OLLIVIER–RICCI (exactly as in your paper)
if REAL_CURVATURE_AVAILABLE and G.number_of_edges() > 0:
    with st.spinner("Computing real Ollivier–Ricci curvature..."):
        orc = OllivierRicci(G, alpha=0.5, method="Sinkhorn", verbose="ERROR")
        orc.compute_ricci_curvature()
        curvatures = list(nx.get_edge_attributes(orc.G, "ricciCurvature").values())
        kappa = sum(curvatures) / len(curvatures) if curvatures else 0.0
else:
    kappa = nx.average_clustering(G)  # fallback (very rare)
    st.caption("⚠️ Using clustering approximation (real curvature unavailable)")

C = w1 * delta - w2 * var_sigma + w3 * kappa

st.metric("**C(G) Score**", f"{C:.4f}")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Spectral Gap Δλ", f"{delta:.4f}")
with col2: st.metric("Singular-Value Variance", f"{var_sigma:.4f}")
with col3: st.metric("Avg Ollivier–Ricci κ", f"{kappa:.4f}")

# ====================== ATTACK SIM (real curvature on attacked graphs too) ======================
st.subheader("Attack Simulation")
if st.button("Remove 20% random edges"):
    G_attack = G.copy()
    edges = list(G_attack.edges())
    remove_count = max(1, int(0.2 * len(edges)))
    np.random.shuffle(edges)
    G_attack.remove_edges_from(edges[:remove_count])
    st.session_state.G_attack = G_attack
    st.success("Random attack done")

if st.button("Remove 20% hub edges"):
    G_attack = G.copy()
    degree = dict(G_attack.degree())
    sorted_nodes = sorted(degree, key=degree.get, reverse=True)
    remove_count = max(1, int(0.2 * G_attack.number_of_edges()))
    edges_to_remove = []
    for node in sorted_nodes:
        for neigh in list(G_attack.neighbors(node)):
            if len(edges_to_remove) < remove_count:
                edges_to_remove.append((node, neigh))
    G_attack.remove_edges_from(edges_to_remove)
    st.session_state.G_attack = G_attack
    st.success("Hub attack done")

if 'G_attack' in st.session_state:
    Ga = st.session_state.G_attack
    Aa = nx.to_numpy_array(Ga)
    eva = np.linalg.eigvals(Aa)
    da = np.max(np.real(eva)) - (sorted(np.real(eva), reverse=True)[1] if len(eva)>1 else 0)
    va = np.var(np.linalg.svd(Aa, compute_uv=False))
    
    if REAL_CURVATURE_AVAILABLE and Ga.number_of_edges() > 0:
        orca = OllivierRicci(Ga, alpha=0.5, method="Sinkhorn", verbose="ERROR")
        orca.compute_ricci_curvature()
        curva = list(nx.get_edge_attributes(orca.G, "ricciCurvature").values())
        ka = sum(curva) / len(curva) if curva else 0.0
    else:
        ka = nx.average_clustering(Ga)
    
    Ca = w1 * da - w2 * va + w3 * ka

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Original', 'Random attack', 'Hub attack'], [C, Ca, Ca], color=['#4CAF50', '#FF9800', '#F44336'])
    ax.set_ylabel('C(G) Score')
    ax.set_title('Robustness Drop Under Attack')
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)

st.info("📦 Full reproducible package (larger N, exact experiments) → [Download ZIP](https://github.com/syedrazaaftab/graph-robustness-score/raw/main/computational-testbed.zip)")

st.caption("Built by Syed Raza Aftab • Princeton Meadows, NJ  \n"
           "Paid network robustness audits available — email: aftab011190@gmail.com")
