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

# 1. 构建图
G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

print(f"Number of nodes in G: {G.number_of_nodes()}")

# 2. 使用 cdlib 的 Louvain 算法进行社区检测
communities = algorithms.louvain(G)

# 统计社区数和每个社区的节点数
community_list = communities.communities
community_sizes = [len(c) for c in community_list]
print(f"Number of communities: {len(community_list)}")
for i, c in enumerate(community_list):
    print(f"Community {i+1}: {len(c)} nodes")

# 画社区规模分布直方图
plt.figure(figsize=(12,9))
plt.bar(range(1, len(community_sizes)+1), community_sizes, width=0.8, align='center')
plt.xlabel('Community Index')
plt.ylabel('Community Size')
plt.title('Community Sizes (Louvain)')
plt.tight_layout()
plt.xticks(range(1, len(community_sizes)+1))
plt.show()
