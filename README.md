# Graph Robustness Score C(G)

**One clean number that tells you how robust any network is.**

C(G) = w₁·spectral gap − w₂·singular-value variance + w₃·average Ollivier–Ricci curvature

---

### 🎯 Live Demo (try it now — no install needed)
**[🧠 Open the web demo](https://graph-robustness-score.streamlit.app)**

Upload any edgelist CSV or click “Try sample graph” to see your score instantly.

---

### Why this score?
Most graph metrics only look at one thing (connectivity, clustering, or degree distribution).  
C(G) combines **three complementary views** in a single interpretable number:

- **Spectral gap** → how well the whole network is connected (big gap = harder to disconnect)
- **Singular-value variance** → penalises “superstar” hubs (high variance = fragile to targeted attacks)
- **Ollivier–Ricci curvature** → rewards strong local clustering and shortcuts (positive curvature = more robust locally)

Result: a simple scalar that highlights **structurally robust motifs** even inside random graphs.

---

### Quick start

```bash
# 1. Download the full package
wget https://github.com/syedrazaaftab/graph-robustness-score/raw/main/computational-testbed.zip

# 2. One-click reproduction (includes paper, data, plots, weight sensitivity)
python notebooks/exploratory.py

How to choose the weights (w₁, w₂, w₃)
Default (recommended for most cases): w₁ = w₂ = w₃ = 1
This balances global connectivity, uniformity, and local clustering.
Quick rules of thumb:
•  Supply-chain / infrastructure graphs → increase w₁ (connectivity matters most)
•  Social / influencer networks → increase w₂ (penalise hubs more)
•  Biological / molecular graphs → increase w₃ (local clustering is key)
The full package includes a weight-sensitivity heatmap so you can tune them for your domain.

Paper
“Complexity Functionals on Sparse Random Graphs” (Feb 19, 2026)
Exact analytic decomposition, regular-graph results, finite-size scaling up to N=800, and 20-run error bars.
Download PDF inside the ZIP

Commercial use & consulting
I offer paid network robustness audits (5–7 business days):
•  Supply-chain resilience reports
•  Fraud / transaction graph analysis
•  Molecular / protein interaction robustness
•  Cybersecurity attack-surface scoring
First 3 clients this month get 30% off + free 30-min call.
Email: syedrazaaftab@gmail.com
or book a free 15-min discovery call (Calendly link coming soon)

Made with ❤️ by Syed Raza Aftab
Independent Researcher, Princeton Meadows, New Jersey, USA
MIT License • Feel free to use the score in your own work (commercial or academic).
Just cite the paper or link back to this repo.
