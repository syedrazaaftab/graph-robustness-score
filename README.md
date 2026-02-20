# Graph Robustness Score C(G)

**One clean number that tells you how robust any network is.**

C(G) = w₁·spectral gap − w₂·singular-value variance + w₃·average Ollivier–Ricci curvature

**What it does**
- Detects globally well-connected networks (spectral gap)
- Penalises overly uneven “superstar” structures (variance)
- Rewards local clustering and robustness (curvature)

**Key features**
- Exact analytic decomposition for regular graphs
- Stable motifs in sparse random graphs (p = 3/N)
- Full weight sensitivity analysis
- One-click reproducible experiments (N up to 800)

**Try it now**
```bash
python notebooks/exploratory.py
