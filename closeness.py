import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

def draw_closeness_distribution(g):
    node_closeness = nx.closeness_centrality(g)
    closeness_sequence = sorted(node_closeness.values(), reverse=True)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(*np.unique(closeness_sequence, return_counts=True), width=0.005)
    ax.set_title("Closeness histogram")
    ax.set_xlabel("Closeness")
    ax.set_ylabel("# of Nodes")
    fig.tight_layout()
    plt.show()