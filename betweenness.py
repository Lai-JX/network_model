import random
import datetime as dt
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def draw_edge_betweenness_distribution(g):
    edge_bet = nx.edge_betweenness_centrality(g)
    bet_sequence = sorted(edge_bet.values(), reverse=True)
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.bar(*np.unique(bet_sequence, return_counts=True), width=0.005, color='red')
    ax.set_title("Edge betweenness histogram")
    ax.set_xlabel("Edge betweenness")
    ax.set_ylabel("# of Edges")
    fig.tight_layout()
    plt.show()


def get_max_betweenness_edge(g):
    edge_bet = nx.edge_betweenness_centrality(g)
    max_betweenness = 0
    max_edge = (0, 0)
    for e in edge_bet:
        b = edge_bet[e]
        if b > max_betweenness:
            max_betweenness = b
            max_edge = e
    return max_betweenness, max_edge


def intentional_attack_edge_betweenness(g, attacked_edge=None):
    g = nx.Graph(g)
    if attacked_edge is None:
        _, attacked_edge = get_max_betweenness_edge(g)
    g.remove_edge(*attacked_edge)
    return g

def random_attack_edge_betweenness(g):
    random.seed(int(dt.datetime.now().timestamp() * 1000))
    g = nx.Graph(g)
    attacked_edge = random.sample(list(g.edges), 1)[0]
    attacked_betweenness = nx.edge_betweenness_centrality(g)[attacked_edge]
    g.remove_edge(*attacked_edge)
    return g, attacked_edge, attacked_betweenness