import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from main import build_graph
from degree import intentional_attack_node_degree
from coreness import intentional_attack_node_coreness
from betweenness import intentional_attack_node_betweenness, intentional_attack_edge_betweenness
from closeness import intentional_attack_node_closeness

# 构建图
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])

# 初始化
attack_counts = 200

# 对节点的度数攻击
max_subgraph_sizes_degree = []
for _ in range(attack_counts):
    g, attacked_node, attacked_degree = intentional_attack_node_degree(g)
    print(f"Attacked Node (Degree): {attacked_node}, Degree: {attacked_degree}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_degree.append(len(largest_cc))

# 重置图以进行节点 coreness 攻击
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])

# 对节点的 coreness 攻击
max_subgraph_sizes_coreness = []
for _ in range(attack_counts):
    g, attacked_node, attacked_coreness = intentional_attack_node_coreness(g)
    print(f"Attacked Node (Coreness): {attacked_node}, Coreness: {attacked_coreness}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_coreness.append(len(largest_cc))

# 重置图以进行节点 betweenness 攻击
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])

# 对节点的 betweenness 攻击
max_subgraph_sizes_betweenness = []
for _ in range(attack_counts):
    g, attacked_node, attacked_betweenness = intentional_attack_node_betweenness(g)
    print(f"Attacked Node (Betweenness): {attacked_node}, Betweenness: {attacked_betweenness}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_betweenness.append(len(largest_cc))

# 重置图以进行边的 betweenness 攻击
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])

# 对边的 betweenness 攻击
max_subgraph_sizes_edge_betweenness = []
for _ in range(attack_counts):
    g, attacked_edge, attacked_betweenness = intentional_attack_edge_betweenness(g)
    print(f"Attacked Edge (Betweenness): {attacked_edge}, Betweenness: {attacked_betweenness}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_edge_betweenness.append(len(largest_cc))

# 绘制对节点度数的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_degree, marker='o', color='b')
plt.title("Max Subgraph Size During Node Degree Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()  # 弹出图形窗口

# 绘制对节点 coreness 的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_coreness, marker='o', color='r')
plt.title("Max Subgraph Size During Node Coreness Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()  # 弹出图形窗口

# 绘制对节点 betweenness 的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_betweenness, marker='o', color='g')
plt.title("Max Subgraph Size During Node Betweenness Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()  # 弹出图形窗口

# 绘制对边 betweenness 的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_edge_betweenness, marker='o', color='c')
plt.title("Max Subgraph Size During Edge Betweenness Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()  # 弹出图形窗口
