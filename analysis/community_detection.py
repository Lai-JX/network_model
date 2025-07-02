import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# 路径设置
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from libs.utils import build_graph
from cdlib import algorithms
from cdlib import evaluation
import matplotlib.colors as mcolors

# 1. 构建图
G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

print(f"Number of nodes in G: {G.number_of_nodes()}")

# 2. 使用 cdlib 的 Louvain 算法进行社区检测
communities = algorithms.louvain(G)

# 统计社区数和每个社区的节点数（已按规模从大到小排序）
community_list = sorted(communities.communities, key=len, reverse=True)
community_sizes = [len(c) for c in community_list]
print(f"Number of communities: {len(community_list)}")
for i, c in enumerate(community_list):
    print(f"Community {i+1}: {len(c)} nodes")

# --- 社区分块布局 ---
color_list = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
node_colors = {}
for idx, comm in enumerate(community_list):
    color = color_list[idx % len(color_list)]
    for node in comm:
        node_colors[node] = color

ordered_nodes = []
added = set()
for comm in community_list:
    for node in comm:
        if node not in added:
            ordered_nodes.append(node)
            added.add(node)
for node in G.nodes:
    if node not in added:
        ordered_nodes.append(node)

num_communities = len(community_list)
block_centers = []
block_radius = 3.0
for i in range(num_communities):
    angle = 2 * np.pi * i / num_communities
    x = block_radius * np.cos(angle)
    y = block_radius * np.sin(angle)
    block_centers.append((x, y))

np.random.seed(42)
pos = {}
for idx, comm in enumerate(community_list):
    cx, cy = block_centers[idx]
    for node in comm:
        if node not in pos:
            pos[node] = (cx + 0.5 * np.random.randn(), cy + 0.5 * np.random.randn())
for node in G.nodes:
    if node not in pos:
        pos[node] = (0 + 5 * np.random.randn(), 0 + 5 * np.random.randn())

plt.figure(figsize=(12,9))
nx.draw_networkx_nodes(G, pos, nodelist=ordered_nodes, node_color=[node_colors.get(n, '#cccccc') for n in ordered_nodes], node_size=30)
nx.draw_networkx_edges(G, pos, alpha=0.2)
plt.title('Community Visualization (Louvain, block layout)')
plt.axis('off')
plt.tight_layout()
plt.savefig('./data/community_colored.png')
plt.show()

# 只保留一张合并的社区规模和密度图，横轴为整数
community_densities = []
for comm in community_list:
    subg = G.subgraph(comm)
    density = nx.density(subg)
    community_densities.append(density)
print(f"Community density: mean={np.mean(community_densities):.4f}, std={np.std(community_densities):.4f}, min={np.min(community_densities):.4f}, max={np.max(community_densities):.4f}")

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
plt.title('Community Size and Density (Louvain, sorted)')
plt.tight_layout()
plt.show()

# 只输出大社区覆盖率（前3个最大社区）
big_communities = community_list[:3]
big_covered = set()
for c in big_communities:
    big_covered.update(c)
big_coverage = len(big_covered) / G.number_of_nodes()
print(f"Large community coverage (top 3 by size): {big_coverage:.2%}")
