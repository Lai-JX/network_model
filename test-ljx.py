from random import sample
import networkx as nx
import matplotlib.pyplot as plt
from main import build_graph, draw_graph, find_subgraph,draw_betweenness_centrality
import numpy as np

# build graph
G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv', 1000)
print(G)
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])

draw_graph(G, 'network.png')

H = find_subgraph(G)
print(H)

draw_betweenness_centrality(H)