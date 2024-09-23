import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

def draw_closeness_distribution(g, save_path=None, is_show=True):
    node_closeness = nx.closeness_centrality(g)
    closeness_sequence = sorted(node_closeness.values(), reverse=True)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(*np.unique(closeness_sequence, return_counts=True), width=0.005)
    ax.set_title("Closeness histogram")
    ax.set_xlabel("Closeness")
    ax.set_ylabel("# of Nodes")
    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    if is_show:
        plt.show()

def get_max_closeness_node(g):
    node_closeness = nx.closeness_centrality(g)
    max_closeness = -1
    max_node = None
    for n, c in node_closeness.items():
        if c > max_closeness:
            max_closeness = c
            max_node = n
    return max_node, max_closeness


def intentional_attack_node_closeness(g):
    g = nx.Graph(g)
    attacked_node, attacked_closeness = get_max_closeness_node(g)
    g.remove_node(attacked_node)
    return g, attacked_node, attacked_closeness
