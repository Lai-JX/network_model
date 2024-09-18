import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt
import statistics

# 1. 从txt文件中加载网络
nodes = set()
G = nx.Graph()

index = 1
mapping_dict = {}
with open('data/processed_facebook_combined-another.txt', 'r') as f:
    for line in f:
        from_node, to_node = map(int, line.strip().split())
        nodes.add(from_node)
        nodes.add(to_node)

node_list = sorted(list(nodes))

for i in range(len(node_list)):
    mapping_dict[node_list[i]] = i + 1

with open('data/processed_facebook_combined-another.txt', 'r') as f:
    for line in f:
        from_node, to_node = map(int, line.strip().split())
        G.add_edge(mapping_dict[from_node],mapping_dict[to_node])

# print(nx.is_connected(G))

G.remove_nodes_from(nx.isolates(G))
# G.remove_edges_from(nx.selfloop_edges(G))
# print(list(nx.isolates(G)))

# print(nx.average_shortest_path_length(G))
H = list(G.subgraph(c) for c in nx.connected_components(G))[0]
print(nx.diameter(H))
degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)
dmean = statistics.mean(degree_sequence)
print(dmean)
print(dmax)
# print(nx.average_clustering(G))
