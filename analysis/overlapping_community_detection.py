import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
from collections import Counter, defaultdict

# 路径设置
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from libs.utils import build_graph
from cdlib import algorithms, evaluation, viz

# 1. 构建图
graph_path = './data/git_web_ml/musae_git_edges.csv'
G, nodes = build_graph(graph_path)
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

print(f"Number of nodes in G: {G.number_of_nodes()}")

# 2. 使用 cdlib 的 CONGA 算法进行重叠社区检测
# 探索不同 number_communities 下的 EQ 得分
# 结果是33最高，每次运行太耗时，所以先注释
# k_range = range(20, 50)
# eq_scores = []
# for k in k_range:
#     comms = algorithms.conga(G, number_communities=k)
#     eq = evaluation.erdos_renyi_modularity(G, comms).score
#     eq_scores.append(eq)

# plt.figure(figsize=(10,6))
# plt.plot(list(k_range), eq_scores, marker='o')
# plt.xlabel('number_communities')
# plt.ylabel('EQ (Erdos-Renyi Modularity)')
# plt.title('EQ vs number_communities (CONGA)')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig('./data/overlapping_community_detection_EQ_vs_k.png')
# plt.show()

# 选择 EQ 最大时的 number_communities
# best_k = list(k_range)[int(np.argmax(eq_scores))]
# print(f"Best number_communities (max EQ): {best_k}")

# number_communities = best_k
number_communities = 33
communities = algorithms.conga(G, number_communities=number_communities)


# 输出整体扩展模块度（EQ）
eq = evaluation.erdos_renyi_modularity(G, communities).score
print(f"EQ (CONGA): {eq:.4f}")

# 统计每个节点在重叠社区中出现的次数
node_overlap_count = Counter()
for comm in communities.communities:
    node_overlap_count.update(comm)

# 统计每种重叠次数的节点数量
count_hist = defaultdict(int)
for node, cnt in node_overlap_count.items():
    count_hist[cnt] += 1

# 控制台输出
print("Node overlap count (number of nodes with given overlap times):")
for overlap_times in sorted(count_hist):
    print(f"Overlap {overlap_times}: {count_hist[overlap_times]} nodes")

# 绘制柱状图
plt.figure(figsize=(10,6))
x_ticks = np.arange(1, max(count_hist.keys())+1)
y_vals = [count_hist.get(x, 0) for x in x_ticks]
plt.bar(x_ticks, y_vals, color='tab:green')
plt.xlabel('Node Overlap Times')
plt.ylabel('Number of Nodes')
plt.title(f'Node Overlap Distribution (CONGA, k={number_communities})')
plt.xticks(x_ticks)  # 显示所有横坐标
plt.tight_layout()
plt.savefig('./data/overlapping_community_detection_node_overlap_hist.png')
plt.show()


# 统计社区数和每个社区的节点数（已按规模从大到小排序）
community_list = sorted(communities.communities, key=len, reverse=True)
community_sizes = [len(c) for c in community_list]
community_densities = [nx.density(G.subgraph(c)) for c in community_list]
print(f"Number of communities: {len(community_list)}")
for i, (c, d) in enumerate(zip(community_list, community_densities)):
    print(f"Community {i+1}: {len(c)} nodes, density={d:.4f}")



# 使用 cdlib.viz.plot_network_highlighted_clusters 绘制社区高亮图
position = nx.spring_layout(G, seed=42)
viz.plot_network_highlighted_clusters(G, communities, position=position, figsize=(12, 9), node_size=30)
plt.title(f'Overlapping Community Visualization (CONGA, highlighted clusters, k={number_communities})')
plt.tight_layout()
plt.savefig('./data/overlapping_community_detection_highlighted_clusters.png')
plt.show()

fig, ax1 = plt.subplots(figsize=(12,6))
x = np.arange(1, len(community_sizes)+1)
color1 = 'tab:blue'
color2 = 'tab:orange'
ax1.set_xlabel('Community Index (sorted by size)')
ax1.set_ylabel('Community Size', color=color1)
ln1 = ax1.plot(x, community_sizes, color=color1, marker='o', label='Community Size')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(x)

ax2 = ax1.twinx()
ax2.set_ylabel('Density', color=color2)
ln2 = ax2.plot(x, community_densities, color=color2, marker='s', label='Community Density')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_xticks(x)

lns = ln1 + ln2
labels = [l.get_label() for l in lns]
ax1.legend(lns, labels, loc='upper right')
plt.title(f'Overlapping Community Size and Density (CONGA, sorted, k={number_communities})')
plt.tight_layout()
plt.savefig('./data/overlapping_community_detection_size_density.png')
plt.show()
