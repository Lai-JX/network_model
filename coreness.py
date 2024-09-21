import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def draw_coreness_distribution(g):
    node_coreness = nx.core_number(g)
    closeness_sequence = sorted(node_coreness.values(), reverse=True)
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.bar(*np.unique(closeness_sequence, return_counts=True), width=0.1)
    ax.set_title("Coreness histogram")
    ax.set_xlabel("Coreness")
    ax.set_ylabel("# of Nodes")
    fig.tight_layout()
    plt.show()


def draw_k_core(g, k):
    gk = nx.k_core(g, k)
    fig, ax = plt.subplots(figsize=(20, 15))
    pos = nx.spring_layout(gk, seed=10396953)
    nx.draw_networkx_nodes(gk, pos, ax=ax, node_size=20)
    nx.draw_networkx_edges(gk, pos, ax=ax, alpha=0.4)
    ax.set_title(str(k) + "-core of G")
    ax.set_axis_off()
    fig.tight_layout()
    plt.show()
