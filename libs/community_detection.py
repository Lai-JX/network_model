import os
import pickle
from tkinter import Label
import networkx as nx
import matplotlib.pyplot as plt
from cdlib import algorithms, viz, evaluation
import random
from PIL import Image, ImageTk
import numpy as np
from libs.utils import draw_graph, plot_network_highlighted_clusters

def detect_and_draw_communities(G, save_path=None, show=True, image_label:Label=None, seed=None):
    """
    对图G进行社区检测（Louvain），并并列输出社区规模密度折线图和着色网络图。
    :param G: networkx.Graph
    :param save_path: 保存图片路径（可选）
    :param show: 是否直接plt.show()
    :return: None
    """
    # 社区检测
    communities = algorithms.louvain(G)
    community_list = sorted(communities.communities, key=len, reverse=True)
    community_sizes = [len(c) for c in community_list]
    community_densities = [nx.density(G.subgraph(c)) for c in community_list]
    print(f"Number of communities: {len(community_list)}")
    for i, c in enumerate(community_list):
        print(f"Community {i+1}: {len(c)} nodes")
    # --- 着色网络图数据准备 ---
    pos = G.pos if hasattr(G, 'pos') else nx.spring_layout(G, seed=seed)
    color_map = {}
    palette = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(community_list))]
    for idx, comm in enumerate(community_list):
        for node in comm:
            color_map[node] = palette[idx]
    node_colors = [color_map.get(node, "#cccccc") for node in G.nodes()]
    # --- 并列输出 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    # 左侧：社区规模和密度双y轴折线
    x = np.arange(1, len(community_sizes)+1)
    color1 = 'tab:blue'
    color2 = 'tab:orange'
    ax1.set_xlabel('Community Index (sorted by size)')
    ax1.set_ylabel('Community Size', color=color1)
    ln1 = ax1.plot(x, community_sizes, color=color1, marker='o', label='Community Size')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xticks(x)
    ax1b = ax1.twinx()
    ax1b.set_ylabel('Density', color=color2)
    ln2 = ax1b.plot(x, community_densities, color=color2, marker='s', label='Community Density')
    ax1b.tick_params(axis='y', labelcolor=color2)
    ax1b.set_xticks(x)
    lns = ln1 + ln2
    labels = [l.get_label() for l in lns]
    ax1.legend(lns, labels, loc='upper right')
    ax1.set_title('Community Size and Density (Louvain, sorted)')
    # 右侧：着色网络图
    # viz.plot_network_highlighted_clusters(G, communities,pos)
    plot_network_highlighted_clusters(G, communities, pos, node_size=30, ax=ax2)

    # nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=20, ax=ax2)
    # nx.draw_networkx_edges(G, pos, alpha=0.3, ax=ax2)
    ax2.set_title('Community Visualization (Louvain)')
    ax2.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Community detection result saved to {save_path}")
    if show:
        plt.show()
    if image_label is not None:
        # 只更新右侧着色图像到界面
        draw_graph(G, save_path='./data/temp_community_detection.png', is_show=False, pos=pos, show_labels=True, node_color=node_colors)
        image_color = ImageTk.PhotoImage(Image.open('./data/temp_community_detection.png').resize((1200,600)))
        image_label.config(image=image_color)
        image_label.image = image_color  # 防止被垃圾回收

def detect_and_draw_overlapping_communities(G, save_path=None, show=True, image_label:Label=None, seed=None):
    """
    对图G进行社区检测（Louvain），并并列输出社区规模密度折线图和着色网络图。
    :param G: networkx.Graph
    :param save_path: 保存图片路径（可选）
    :param show: 是否直接plt.show()
    :return: None
    """
    # 社区检测
    number_communities = 33
    res_save_path = f'./data/communities_eq_num{number_communities}_{seed}.pkl'
    if os.path.exists(res_save_path):
        with open(res_save_path, 'rb') as f:
            data = pickle.load(f)
        eq = data['eq']
        communities = data['communities']
        print(f"Loaded eq and community_list from {res_save_path}")
    else:
        communities = algorithms.conga(G, number_communities=number_communities)
        # 输出整体扩展模块度（EQ）
        eq = evaluation.erdos_renyi_modularity(G, communities).score
        
        # 基于pickle将eq和community_list保存起来
        data = {
            'eq': eq,
            'communities': communities
        }
        with open(res_save_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"eq 和 community_list 已保存到 {res_save_path}")

    print(f"EQ (CONGA): {eq:.4f}")
    # 统计社区数和每个社区的节点数（已按规模从大到小排序）
    community_list = sorted(communities.communities, key=len, reverse=True)
    community_sizes = [len(c) for c in community_list]
    community_densities = [nx.density(G.subgraph(c)) for c in community_list]


    print(f"Number of communities: {len(community_list)}")
    for i, (c, d) in enumerate(zip(community_list, community_densities)):
        print(f"Community {i+1}: {len(c)} nodes, density={d:.4f}")
    # --- 着色网络图数据准备 ---
    pos = G.pos if hasattr(G, 'pos') else nx.spring_layout(G, seed=seed)
    color_map = {}
    palette = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(community_list))]
    for idx, comm in enumerate(community_list):
        for node in comm:
            color_map[node] = palette[idx]
    node_colors = [color_map.get(node, "#cccccc") for node in G.nodes()]
    # --- 并列输出 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
    # 左侧：社区规模和密度双y轴折线
    x = np.arange(1, len(community_sizes)+1)
    color1 = 'tab:blue'
    color2 = 'tab:orange'
    ax1.set_xlabel('Community Index (sorted by size)')
    ax1.set_ylabel('Community Size', color=color1)
    ln1 = ax1.plot(x, community_sizes, color=color1, marker='o', label='Community Size')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xticks(x)

    ax1b = ax1.twinx()
    ax1b.set_ylabel('Density', color=color2)
    ln2 = ax1b.plot(x, community_densities, color=color2, marker='s', label='Community Density')
    ax1b.tick_params(axis='y', labelcolor=color2)
    ax1b.set_xticks(x)

    lns = ln1 + ln2
    labels = [l.get_label() for l in lns]
    ax1.legend(lns, labels, loc='upper right')

    # 使用 cdlib.viz.plot_network_highlighted_clusters 绘制社区高亮图
    # position = nx.spring_layout(G, seed=42)
    plot_network_highlighted_clusters(G, communities, pos, node_size=30, ax=ax2)


    ax2.set_title('Community Visualization (Louvain)')
    ax2.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Community detection result saved to {save_path}")
    if show:
        plt.show()
    if image_label is not None:
        # 只更新右侧着色图像到界面
        draw_graph(G, save_path='./data/temp_community_overlap_detection.png', is_show=False, pos=pos, show_labels=True, node_color=node_colors)
        image_color = ImageTk.PhotoImage(Image.open('./data/temp_community_overlap_detection.png').resize((1200,600)))
        image_label.config(image=image_color)
        image_label.image = image_color  # 防止被垃圾回收
