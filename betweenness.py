import random
import datetime as dt
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def draw_edge_betweenness_distribution(g):
    edge_bet = nx.edge_betweenness_centrality(g)
    bet_sequence = sorted(edge_bet.values(), reverse=True)
    fig, ax = plt.subplots(figsize=(4, 3))
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

def get_max_betweenness_node(g):
    node_bet = nx.betweenness_centrality(g)
    max_betweenness = 0
    max_node = 0
    for n in node_bet:
        b = node_bet[n]
        if b > max_betweenness:
            max_betweenness = b
            max_node = n
    return max_betweenness, max_node


def intentional_attack_edge_betweenness(g, attacked_edge=None):
    g = nx.Graph(g)
    if attacked_edge is None:
        max_betweenness, attacked_edge = get_max_betweenness_edge(g)
    g.remove_edge(*attacked_edge)
    return g, attacked_edge, max_betweenness

def intentional_attack_node_betweenness(g, attacked_node=None):
    g = nx.Graph(g)
    if attacked_node is None:
        max_betweenness, attacked_node = get_max_betweenness_node(g)
    g.remove_node(attacked_node)
    return g, attacked_node, max_betweenness

def random_attack_edge_betweenness(g):
    random.seed(int(dt.datetime.now().timestamp() * 1000))
    g = nx.Graph(g)
    attacked_edge = random.sample(list(g.edges), 1)[0]
    attacked_betweenness = nx.edge_betweenness_centrality(g)[attacked_edge]
    g.remove_edge(*attacked_edge)
    return g, attacked_edge, attacked_betweenness
def random_attack_node_betweenness(g):
    random.seed(int(dt.datetime.now().timestamp() * 1000))
    g = nx.Graph(g)
    attacked_node = random.sample(list(g.nodes), 1)[0]
    attacked_betweenness = nx.betweenness_centrality(g)[attacked_node]
    g.remove_node(attacked_node)
    return g, attacked_node, attacked_betweenness