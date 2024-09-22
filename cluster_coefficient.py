import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def average_cluster_coefficient(g):
    node_cc = nx.clustering(g)
    cc_sum = 0
    for node in node_cc:
        cc_sum += node_cc[node]
    return cc_sum / g.number_of_nodes()

def draw_cluster_coefficient_distribution(g):
    node_cc = nx.clustering(g)
    cc_sequence = sorted(node_cc.values(), reverse=True)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(*np.unique(cc_sequence, return_counts=True), width=0.005, color='red')
    ax.set_title("clustering coefficient histogram")
    ax.set_xlabel("clustering coefficient")
    ax.set_ylabel("# of Nodes")
    fig.tight_layout()
    plt.show()