import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def draw_coreness_distribution(g):
    node_coreness = nx.core_number(g)
    closeness_sequence = sorted(node_coreness.values(), reverse=True)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(*np.unique(closeness_sequence, return_counts=True), width=0.1)
    ax.set_title("Coreness histogram")
    ax.set_xlabel("Coreness")
    ax.set_ylabel("# of Nodes")
    fig.tight_layout()
    plt.show()


def draw_k_core(g, k, save_path=None, is_show=True):
    gk = nx.k_core(g, k)
    fig, ax = plt.subplots(figsize=(12, 9))
    pos = nx.spring_layout(gk, seed=10396953)
    nx.draw_networkx_nodes(gk, pos, ax=ax, node_size=20)
    nx.draw_networkx_edges(gk, pos, ax=ax, alpha=0.4)
    ax.set_title(str(k) + "-core of G", fontsize=24)
    ax.set_axis_off()
    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    if is_show:
        plt.show()



def get_max_coreness_node(g):
    node_coreness = nx.core_number(g)
    max_coreness = 0
    max_node = 0
    for n in node_coreness:
        c = node_coreness[n]
        if c > max_coreness:
            max_coreness = c
            max_node = n
    return max_node, max_coreness


def intentional_attack_node_coreness(g):
    g = nx.Graph(g)
    attacked_node, attacked_coreness = get_max_coreness_node(g)
    g.remove_node(attacked_node)
    return g, attacked_node, attacked_coreness
