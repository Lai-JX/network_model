import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

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
# 可根据需要调整 number_communities 参数
number_communities = 5
communities = algorithms.conga(G, number_communities=number_communities)

# 输出整体扩展模块度（EQ）
eq = evaluation.erdos_renyi_modularity(G, communities).score
print(f"EQ (CONGA): {eq:.4f}")

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
plt.savefig('./data/overlapping_community_colored.png')
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
plt.show()

