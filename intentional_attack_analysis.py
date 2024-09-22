import matplotlib.pyplot as plt
import networkx as nx

from betweenness import intentional_attack_node_betweenness, intentional_attack_edge_betweenness
from closeness import intentional_attack_node_closeness
from coreness import intentional_attack_node_coreness
from degree import intentional_attack_node_degree
from utils import build_graph

# 构建并保存未被攻击的初始图
g_original, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g_original = g_original.subgraph(sorted(nx.connected_components(g_original), key=len, reverse=True)[0])

# 初始化攻击次数
attack_counts = 200

# 对节点的度数进行攻击
print("\nStarting Node Degree Attacks")
g = g_original.copy()  # 开始攻击时，复制初始图
max_subgraph_sizes_degree = []
for _ in range(attack_counts):
    g, attacked_node, attacked_degree = intentional_attack_node_degree(g)
    print(f"Attacked Node (Degree): {attacked_node}, Degree: {attacked_degree}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_degree.append(len(largest_cc))

# 对节点的 coreness 进行攻击
print("\nStarting Node Coreness Attacks")
g = g_original.copy()  # 复制初始图
max_subgraph_sizes_coreness = []
for _ in range(attack_counts):
    g, attacked_node, attacked_coreness = intentional_attack_node_coreness(g)
    print(f"Attacked Node (Coreness): {attacked_node}, Coreness: {attacked_coreness}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_coreness.append(len(largest_cc))

# 对节点的 betweenness 进行攻击
print("\nStarting Node Betweenness Attacks")
g = g_original.copy()  # 复制初始图
max_subgraph_sizes_betweenness = []
for _ in range(attack_counts):
    g, attacked_node, attacked_betweenness = intentional_attack_node_betweenness(g)
    print(f"Attacked Node (Betweenness): {attacked_node}, Betweenness: {attacked_betweenness}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_betweenness.append(len(largest_cc))

# 对节点的 closeness 进行攻击
print("\nStarting Node Closeness Attacks")
g = g_original.copy()  # 复制初始图
max_subgraph_sizes_closeness = []
for _ in range(attack_counts):
    g, attacked_node, attacked_closeness = intentional_attack_node_closeness(g)
    print(f"Attacked Node (Closeness): {attacked_node}, Closeness: {attacked_closeness}")
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_closeness.append(len(largest_cc))

# 对边的 betweenness 进行攻击
print("\nStarting Edge Betweenness Attacks")
g = g_original.copy()  # 复制初始图
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
plt.show()

# 绘制对节点 coreness 的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_coreness, marker='o', color='r')
plt.title("Max Subgraph Size During Node Coreness Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()

# 绘制对节点 betweenness 的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_betweenness, marker='o', color='g')
plt.title("Max Subgraph Size During Node Betweenness Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()

# 绘制对节点 closeness 的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_closeness, marker='o', color='m')
plt.title("Max Subgraph Size During Node Closeness Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()

# 绘制对边 betweenness 的攻击图
plt.figure(figsize=(8, 6))
plt.plot(range(attack_counts), max_subgraph_sizes_edge_betweenness, marker='o', color='c')
plt.title("Max Subgraph Size During Edge Betweenness Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.grid()
plt.tight_layout()
plt.show()
