import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt

# 1. 从txt文件中加载网络
nodes = set()
G = nx.Graph()

index = 1
mapping_dict = {}
with open('processed_email-Eu-core-750.txt', 'r') as f:
    for line in f:
        from_node, to_node = map(int, line.strip().split())
        nodes.add(from_node)
        nodes.add(to_node)

node_list = sorted(list(nodes))

for i in range(len(node_list)):
    mapping_dict[node_list[i]] = i + 1

with open('processed_email-Eu-core-750.txt', 'r') as f:
    for line in f:
        from_node, to_node = map(int, line.strip().split())
        G.add_edge(mapping_dict[from_node],mapping_dict[to_node])

betweenness = nx.closeness_centrality(G)
tmp = sorted(betweenness.items(),key = lambda x:x[1],reverse=True)
print(tmp)
betweeness_nodes_descend = []
for i in range(len(tmp)):
    betweeness_nodes_descend.append(tmp[i][0])
print(betweeness_nodes_descend)