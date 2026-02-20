import streamlit as st
import networkx as nx
import numpy as np
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Graph Robustness Score", page_icon="🧠")
st.title("🧠 Graph Robustness Score C(G)")
st.markdown("**One clean number** that tells you how robust any network is.\nSpectral gap − singular-value variance + Ollivier–Ricci curvature (demo version)")

# Sample graph button
if st.button("🚀 Try a sample small graph (3-node triangle)"):
    sample_csv = "source,target\n1,2\n1,3\n2,3"
    G = nx.read_edgelist(StringIO(sample_csv), delimiter=",", nodetype=int)
    st.success("Sample triangle graph loaded!")

else:
    uploaded_file = st.file_uploader("Or upload your own edgelist CSV (source,target)", type=["csv"])

if 'G' not in st.session_state:
    uploaded_file = st.file_uploader("Upload your edgelist CSV (source,target)", type=["csv"])
    if uploaded_file is not None:
        G = nx.read_edgelist(uploaded_file, delimiter=",", nodetype=int)
    else:
        st.stop()
else:
    G = st.session_state.G

st.success(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

A = nx.adjacency_matrix(G).todense()
ev = np.linalg.eigvals(A)
lambda_max = np.max(np.real(ev))
lambda_next = sorted(np.real(ev), reverse=True)[1] if len(ev) > 1 else 0
delta = lambda_max - lambda_next

sigma = np.linalg.svd(A, compute_uv=False)
var_sigma = np.var(sigma)

kappa_approx = nx.average_clustering(G)

C = delta - var_sigma + kappa_approx * 10

st.metric("**Your C(G) Score**", f"{C:.3f}")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Spectral Gap", f"{delta:.3f}")
with col2: st.metric("Singular-Value Variance", f"{var_sigma:.3f}")
with col3: st.metric("Curvature (approx)", f"{kappa_approx:.3f}")

st.info("💡 This is a quick demo. Full package has exact Ollivier–Ricci + weight sliders + stable motif detection.")

st.markdown("[📥 Download full package + paper](https://github.com/syedrazaaftab/graph-robustness-score/raw/main/computational-testbed.zip)")

st.caption("Built with C(G) by Syed Raza Aftab • Princeton Meadows, NJ\nEmail for paid audits: syedrazaaftab@gmail.com")
