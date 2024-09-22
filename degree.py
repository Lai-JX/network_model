import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def average_degree(g):
    node_deg_pairs = nx.degree(g)
    deg_sum = 0
    for pair in node_deg_pairs:
        deg_sum += pair[1]
    return deg_sum / g.number_of_nodes()


def draw_degree_distribution(g):
    node_deg_pairs = nx.degree(g)
    degree_sequence = sorted((d for n, d in node_deg_pairs), reverse=True)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(*np.unique(degree_sequence, return_counts=True), color='red')
    ax.set_title("Degree histogram")
    ax.set_xlabel("Degree")
    ax.set_ylabel("# of Nodes")
    fig.tight_layout()
    plt.show()


def draw_degree_rank(g, save_path=None, is_show=True):
    node_deg_pairs = nx.degree(g)
    degree_sequence = sorted((d for n, d in node_deg_pairs), reverse=True)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(degree_sequence, "b-", marker="o")
    ax.set_title("Degree Rank Plot")
    ax.set_ylabel("Degree")
    ax.set_xlabel("Rank")
    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    if is_show:
        plt.show()


def get_max_degree_node(g):
    node_degree = dict(g.degree())
    max_degree = 0
    max_node = None
    for n, d in node_degree.items():
        if d > max_degree:
            max_degree = d
            max_node = n
    return max_node, max_degree


def intentional_attack_node_degree(g):
    g = nx.Graph(g)
    attacked_node, attacked_degree = get_max_degree_node(g)
    g.remove_node(attacked_node)
    return g, attacked_node, attacked_degree
