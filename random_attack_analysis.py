import random
import datetime as dt
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from main import build_graph

# 构建图
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
g = nx.Graph(g)  # 立刻重置图

# 初始化
attack_counts = 200

# 随机攻击节点
max_subgraph_sizes_random_node = []
for _ in range(attack_counts):
    random.seed(int(dt.datetime.now().timestamp() * 1000))  # 设置随机种子
    random_node = random.choice(list(g.nodes))
    g.remove_node(random_node)  # 随机攻击节点
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_random_node.append(len(largest_cc))
    print(f"Randomly Attacked Node: {random_node}")

# 重置图以进行随机攻击边
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
g = nx.Graph(g)  # 立刻重置图

# 随机攻击边
max_subgraph_sizes_random_edge = []
for _ in range(attack_counts):
    random.seed(int(dt.datetime.now().timestamp() * 1000))  # 设置随机种子
    random_edge = random.choice(list(g.edges))
    g.remove_edge(*random_edge)  # 随机攻击边
    largest_cc = max(nx.connected_components(g), key=len)
    max_subgraph_sizes_random_edge.append(len(largest_cc))
    print(f"Randomly Attacked Edge: {random_edge}")

# 绘制随机节点攻击图
plt.figure(figsize=(4, 3))
plt.plot(range(attack_counts), max_subgraph_sizes_random_node, marker='o', color='m')
plt.title("Max Subgraph Size During Random Node Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.ylim(bottom=0)  # 纵轴从0开始
plt.grid()
plt.tight_layout()
plt.show()  # 弹出图形窗口

# 绘制随机边攻击图
plt.figure(figsize=(4, 3))
plt.plot(range(attack_counts), max_subgraph_sizes_random_edge, marker='o', color='y')
plt.title("Max Subgraph Size During Random Edge Attacks")
plt.xlabel("Attack Count")
plt.ylabel("Size of Largest Subgraph")
plt.ylim(bottom=0)  # 纵轴从0开始
plt.grid()
plt.tight_layout()
plt.show()  # 弹出图形窗口
