import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# 路径设置
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from libs.utils import build_graph
from cdlib import algorithms, evaluation

# 1. 构建图
G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

print(f"Number of nodes in G: {G.number_of_nodes()}")

# 2. 使用 cdlib 的 clique_percolation 方法进行重叠社区检测
# k=4 是常用参数，可根据需要调整
communities = algorithms.kclique(G, k=3)

# 统计社区数和每个社区的节点数
community_list = communities.communities
community_sizes = [len(c) for c in community_list]
print(f"Number of overlapping communities: {len(community_list)}")
for i, c in enumerate(community_list):
    print(f"Community {i+1}: {len(c)} nodes")

# 画社区规模分布直方图
plt.figure(figsize=(12,9))
plt.bar(range(1, len(community_sizes)+1), community_sizes, width=0.8, align='center')
plt.xlabel('Community Index')
plt.ylabel('Community Size')
plt.title('Community Sizes (Clique Percolation, k=3)')
plt.tight_layout()
plt.xticks(range(1, len(community_sizes)+1))
plt.show()

# ------------------ 重叠社区分析 ------------------
# 节点重叠度分布（每个节点属于多少个社区）
from collections import Counter
node_community_count = Counter()
for comm in community_list:
    for node in comm:
        node_community_count[node] += 1
all_degrees = list(node_community_count.values())

# 1. 节点重叠度统计
max_overlap = max(all_degrees)
avg_overlap = np.mean(all_degrees)
print(f"Max node overlap: {max_overlap}")
print(f"Average node overlap: {avg_overlap:.2f}")

# 2. 模块度（extended modularity, EQ）
eq = evaluation.erdos_renyi_modularity(G, communities).score
print(f"Overlapping modularity (EQ): {eq:.4f}")

# 3. 社区覆盖度（覆盖的节点比例）
covered_nodes = set()
for comm in community_list:
    covered_nodes.update(comm)
coverage = len(covered_nodes) / G.number_of_nodes()
print(f"Community coverage: {coverage:.2%}")

# 4. 社区着色可视化
import matplotlib.colors as mcolors
color_list = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
node_colors = {}
for idx, comm in enumerate(community_list):
    color = color_list[idx % len(color_list)]
    for node in comm:
        # 若节点属于多个社区，取第一个社区颜色
        if node not in node_colors:
            node_colors[node] = color

# --- 社区优先布局 ---
# 先将每个社区的节点排在一起，剩余节点按原顺序
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

# 使用 shell_layout，每个社区为一圈
shells = [list(comm) for comm in community_list if len(comm) > 0]
if len(shells) > 1:
    pos = nx.shell_layout(G, shells)
    # 检查未被分配坐标的节点（未被任何社区覆盖的节点）
    missing_nodes = [n for n in ordered_nodes if n not in pos]
    if missing_nodes:
        # 为这些节点分配 spring_layout 坐标，并合并
        spring_pos = nx.spring_layout(G.subgraph(missing_nodes), seed=42)
        for n in missing_nodes:
            pos[n] = spring_pos[n]
else:
    pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(12,9))
nx.draw_networkx_nodes(G, pos, nodelist=ordered_nodes, node_color=[node_colors.get(n, '#cccccc') for n in ordered_nodes], node_size=30)
nx.draw_networkx_edges(G, pos, alpha=0.2)
plt.title('Overlapping Community Visualization (nodes grouped by community)')
plt.axis('off')
plt.tight_layout()
plt.savefig('./data/overlapping_community_colored.png')
plt.show()
