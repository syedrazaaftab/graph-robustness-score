# Graph Robustness Score C(G)

[![Try it live](https://img.shields.io/badge/Try%20it%20live-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://graph-robustness-score.streamlit.app)

**One clean number** that tells you how robust any network is.  
**Spectral gap − singular-value variance + real Ollivier–Ricci curvature**

**Live Demo** • [Paper (Feb 19, 2026)](https://github.com/syedrazaaftab/graph-robustness-score/raw/main/Graph_Robustness_Paper.pdf) • [Full package + experiments](computational-testbed.zip)

I offer **paid network robustness audits** (supply-chain, transaction graphs, biotech interaction networks, cyber attack surfaces).  
First 3 clients this month get **30% off**.

---

### Why this score?
Most graph metrics only look at one thing (connectivity, clustering, or degree distribution).  
C(G) combines **three complementary views** in a single interpretable number:

- **Spectral gap** → how well the whole network is connected (big gap = harder to disconnect)  
- **Singular-value variance** → penalises “superstar” hubs (high variance = fragile to targeted attacks)  
- **Ollivier–Ricci curvature** → rewards strong local clustering and shortcuts (positive curvature = more robust locally)

**Result:** a simple scalar that highlights **structurally robust motifs** even inside random graphs.

---

### Quick start

```bash
# 1. Download the full package
wget https://github.com/syedrazaaftab/graph-robustness-score/raw/main/computational-testbed.zip

# 2. One-click reproduction
python notebooks/exploratory.py

How to choose the weights (w₁, w₂, w₃)
Default (recommended for most cases): w₁ = w₂ = w₃ = 1
This balances global connectivity, uniformity, and local clustering.
Quick rules of thumb:
•  Supply-chain / infrastructure graphs → increase w₁
•  Social / influencer networks → increase w₂
•  Biological / molecular graphs → increase w₃
The full package includes a weight-sensitivity heatmap.

Paper
“Complexity Functionals on Sparse Random Graphs: Spectral Gap, Singular-Value Variance, and Ollivier–Ricci Curvature Contributions”
Syed Raza Aftab, February 19, 2026
Exact analytic decomposition, regular-graph results, finite-size scaling up to N=800.

Commercial use & consulting
I offer paid network robustness audits (5–7 business days turnaround):
•  Supply-chain resilience reports
•  Fraud / transaction graph analysis
•  Molecular / protein interaction robustness
•  Cybersecurity attack-surface scoring
First 3 clients this month get 30% off + free 30-min call.
Email: aftab011190@gmail.com
or book a free 15-min discovery call (Calendly link coming soon).

Made with ❤️ by Syed Raza Aftab
Independent Researcher, Princeton Meadows, New Jersey, USA
MIT License • Feel free to use the score in your own work (commercial or academic).
Just cite the paper or link back to this repo.
