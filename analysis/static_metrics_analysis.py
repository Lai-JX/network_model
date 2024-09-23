import random

import networkx as nx
import matplotlib.pyplot as plt
import datetime as dt

import numpy as np

from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from libs.utils import build_graph

# build graph
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
print(g)

# draw graph
fig, ax = plt.subplots(figsize=(12, 9))
pos = nx.spring_layout(g, seed=2024)
nx.draw_networkx_nodes(g, pos, ax=ax, node_size=20)
nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.4)
ax.set_title("Graph", fontsize=24)
ax.set_axis_off()
fig.tight_layout()
plt.show()

# diameter
print('diameter:', nx.diameter(g))

# clustering coefficient
from libs.cluster_coefficient import average_cluster_coefficient, draw_cluster_coefficient_distribution

print('average clustering coefficient:', average_cluster_coefficient(g))
draw_cluster_coefficient_distribution(g)

# average path length (of each connected component)
component_count = 1
for component in (g.subgraph(component).copy() for component in nx.connected_components(g)):
    print('average path length of component', component_count, ':', nx.average_shortest_path_length(component))
    component_count += 1

# degree
from libs.degree import draw_degree_distribution, average_degree, draw_degree_rank

print('average degree:', average_degree(g))
draw_degree_distribution(g)
draw_degree_rank(g)

# coreness
from libs.coreness import draw_coreness_distribution, draw_k_core

print('average coreness:', np.average(list(nx.core_number(g).values())))
draw_coreness_distribution(g)
draw_k_core(g, 1)
draw_k_core(g, 2)
draw_k_core(g, 3)
draw_k_core(g, 4)
draw_k_core(g, 5)

# closeness
from libs.closeness import draw_closeness_distribution

draw_closeness_distribution(g)
print('average closeness:', np.average(list(nx.closeness_centrality(g).values())))


# edge and node betweenness
from libs.betweenness import draw_edge_betweenness_distribution, get_max_betweenness_edge, \
    intentional_attack_edge_betweenness, random_attack_edge_betweenness, draw_node_betweenness_distribution

print('average edge betweenness:', np.average(list(nx.edge_betweenness_centrality(g).values())))
print('average node betweenness:', np.average(list(nx.betweenness_centrality(g).values())))

draw_edge_betweenness_distribution(g)
draw_node_betweenness_distribution(g)


max_betweenness, max_edge = get_max_betweenness_edge(g)
print('max betweenness:', max_betweenness)
print('max edge:', max_edge)
print('intentionally attacked graph', intentional_attack_edge_betweenness(g))
random_attacked_g, attacked_edge, attacked_betweenness = random_attack_edge_betweenness(g)
print('attacked betweenness:', attacked_betweenness)
print('attacked edge:', attacked_edge)
print('randomly attacked graph', random_attacked_g)

random_attacked_g_itr, _, _ = random_attack_edge_betweenness(g)
for i in range(50):
    random_attacked_g_itr, _, _ = random_attack_edge_betweenness(random_attacked_g_itr)

print('randomly attacked 50 times graph', random_attacked_g_itr)
