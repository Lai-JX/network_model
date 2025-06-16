import networkx as nx
import matplotlib.pyplot as plt
from cdlib import algorithms
import random

def detect_and_draw_communities(G, save_path=None, show=True):
    """
    对图G进行社区检测（Louvain），并绘制社区分布直方图和着色网络图。
    :param G: networkx.Graph
    :param save_path: 保存图片路径（可选）
    :param show: 是否直接plt.show()
    :return: None
    """
    # 社区检测
    communities = algorithms.louvain(G)
    community_list = communities.communities
    community_sizes = [len(c) for c in community_list]
    print(f"Number of communities: {len(community_list)}")
    for i, c in enumerate(community_list):
        print(f"Community {i+1}: {len(c)} nodes")

    # 直方图
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.bar(range(1, len(community_sizes)+1), community_sizes, width=0.8, align='center')
    plt.xlabel('Community Index')
    plt.ylabel('Community Size')
    plt.title('Community Sizes (Louvain)')
    plt.xticks(range(1, len(community_sizes)+1))

    # 网络图着色
    plt.subplot(1,2,2)
    pos = nx.spring_layout(G, seed=2024)
    color_map = {}
    colors = []
    # 生成随机颜色
    palette = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(community_list))]
    for idx, comm in enumerate(community_list):
        for node in comm:
            color_map[node] = palette[idx]
    node_colors = [color_map.get(node, "#cccccc") for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.title('Community Visualization (Louvain)')
    plt.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Community detection result saved to {save_path}")
    if show:
        plt.show()
