from tkinter import Label
import networkx as nx
import matplotlib.pyplot as plt
from cdlib import algorithms
import random
from PIL import Image, ImageTk

from libs.utils import draw_graph

def detect_and_draw_communities(G, save_path=None, show=True, image_label:Label=None, seed=None):
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
    if image_label is not None:
        # 获取plt第二个图
        update_image_label(G, community_list, image_label, seed=None)
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
    # pos = nx.spring_layout(G, seed=2024)
    pos = G.pos if hasattr(G, 'pos') else nx.spring_layout(G, seed=seed)
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
    
def update_image_label(G, community_list, image_label, seed=None):
    pos = G.pos if hasattr(G, 'pos') else nx.spring_layout(G, seed=seed)
    color_map = {}
    palette = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(community_list))]
    for idx, comm in enumerate(community_list):
        for node in comm:
            color_map[node] = palette[idx]
    node_colors = [color_map.get(node, "#cccccc") for node in G.nodes()]
    # nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3)
    # # nx.draw_networkx_edges(G, pos, alpha=0.3)
    # plt.axis('off')
    # plt.savefig('./data/temp_community_detection.png')
    draw_graph(G, save_path='./data/temp_community_detection.png', is_show=False, pos=pos, show_labels=True, node_color=node_colors)
    image_color = ImageTk.PhotoImage(Image.open('./data/temp_community_detection.png').resize((1200,600)))     # .resize((800,400))
    image_label.config(image=image_color)
    image_label.image = image_color  # 防止被垃圾回收