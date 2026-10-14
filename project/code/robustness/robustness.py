import os
import zipfile
import numpy as np
import pandas as pd
import networkx as nx
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_ZIP = os.path.join(HERE, "..", "..", "data", "ml-100k.zip")
OUT = os.path.join(HERE, "output_robustness")
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(7)
THRESHOLDS = (60, 90)
FRACS = np.linspace(0, 0.9, 31)


def build(T):
    with zipfile.ZipFile(DATA_ZIP) as z, z.open("ml-100k/u.data") as f:
        df = pd.read_csv(f, sep="\t", names=["u", "i", "r", "t"])
    A = sp.csr_matrix((np.ones(len(df)), (df.u - 1, df.i - 1)))
    pop = np.asarray(A.sum(0)).ravel()
    co = (A.T @ A).toarray()
    np.fill_diagonal(co, 0)
    adj = sp.csr_matrix(co >= T)
    keep = np.where(adj.sum(1).A1 > 0)[0]  # drop isolated movies
    return adj[keep][:, keep], pop[keep]


def giant_fraction(adj, alive, n0):
    sub = adj[alive][:, alive]
    if sub.shape[0] == 0:
        return 0.0
    _, lab = connected_components(sub, directed=False)
    return np.bincount(lab).max() / n0


def curve(adj, order, n0):
    n = adj.shape[0]
    out = []
    for f in FRACS:
        alive = np.sort(order[int(round(f * n)):])
        out.append(giant_fraction(adj, alive, n0))
    return np.array(out)


def null_graph(adj, seed):
    deg = adj.sum(1).A1.astype(int)
    G = nx.configuration_model(deg.tolist(), seed=seed)
    G = nx.Graph(G)
    G.remove_edges_from(nx.selfloop_edges(G))
    return sp.csr_matrix(nx.to_scipy_sparse_array(G, nodelist=range(len(deg)), format="csr"))


def attack_orders(adj, pop):
    G = nx.from_scipy_sparse_array(adj)
    deg = adj.sum(1).A1
    btw = np.array(list(nx.betweenness_centrality(G, k=300, seed=1).values()))
    return {"degree": np.argsort(-deg), "betweenness": np.argsort(-btw),
            "popularity": np.argsort(-pop)}, deg, btw


def analyse(T):
    adj, pop = build(T)
    n0 = adj.shape[0]
    deg_mean = adj.sum() / n0
    print(f"\n=== T={T}: N={n0}, L={adj.nnz // 2}, <k>={deg_mean:.1f}, "
          f"giant={giant_fraction(adj, np.arange(n0), n0):.2f} ===")
    orders, deg, btw = attack_orders(adj, pop)
    G = nx.from_scipy_sparse_array(adj)
    print(f"clustering={nx.average_clustering(G):.3f}, "
          f"assortativity={nx.degree_assortativity_coefficient(G):.3f}")
    rho = spearmanr(deg, btw)[0], spearmanr(deg, pop)[0]
    print(f"Spearman degree~betweenness={rho[0]:.2f}, degree~popularity={rho[1]:.2f}")

    adj_null = null_graph(adj, seed=3)
    res = {}
    for label, g in [("real", adj), ("null", adj_null)]:
        nd = g.sum(1).A1
        for name, order in [("random", None), ("degree", np.argsort(-nd)),
                            ("betweenness", orders["betweenness"] if label == "real" else None),
                            ("popularity", orders["popularity"] if label == "real" else None)]:
            if name == "random":
                res[(label, name)] = np.mean([curve(g, RNG.permutation(n0), n0) for _ in range(20)], 0)
            elif order is not None:
                res[(label, name)] = curve(g, order, n0)
    rows = []
    for (label, name), s in res.items():
        fc = FRACS[np.argmax(s < 0.05)] if (s < 0.05).any() else np.nan
        rows.append({"T": T, "graph": label, "removal": name,
                     "robustness_R": s.mean(), "f_at_S<0.05": fc})
    tab = pd.DataFrame(rows)
    print(tab.round(3).to_string(index=False))
    return tab, res


def main():
    tabs = []
    fig, axs = plt.subplots(1, len(THRESHOLDS), figsize=(6 * len(THRESHOLDS), 4.2))
    for ax, T in zip(np.atleast_1d(axs), THRESHOLDS):
        tab, res = analyse(T)
        tabs.append(tab)
        for (label, name), s in res.items():
            ax.plot(FRACS, s, "--" if label == "null" else "-", label=f"{name} ({label})")
        ax.set_xlabel("fraction of movies removed f"); ax.set_ylabel("giant component S(f)")
        ax.set_title(f"Movie co-rating network, T={T}"); ax.legend(fontsize=7)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "robustness.png"), dpi=150)
    pd.concat(tabs).to_csv(os.path.join(OUT, "robustness.csv"), index=False)


if __name__ == "__main__":
    main()
