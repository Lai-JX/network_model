import networkx as nx
import matplotlib.pyplot as plt
import random
random.seed(2024)

draw_seed = 2024

def build_graph(data_path, num_nodes=2000, seed=2024):
    G = nx.Graph()

    # 读取txt文件
    with open(data_path, 'r') as f:
        lines = f.readlines()

    edges = lines[1:]

    # 创建节点列表并找出唯一的节点ID
    nodes = set()
    for line in edges:
        from_node, to_node = line.strip().split(",")
        nodes.add(from_node)
        nodes.add(to_node)
        G.add_edge(from_node, to_node)

    print('seed:',seed)
    random.seed(seed)

    for i in range(37700 - num_nodes):
        removed_node = random.sample(list(G.nodes), 1)[0]
        G.remove_node(removed_node)

    return G, nodes

# def build_graph(data_path, num_sample=10000, seed=2024,):
#     G = nx.Graph()
#
#     # 读取txt文件
#     with open(data_path, 'r') as f:
#         lines = f.readlines()
#     if num_sample is None:
#         edges = lines[1:]
#     else:
#         print('seed:',seed)
#         random.seed(seed)
#         edges = random.sample(lines[1:], num_sample)
#
#     # 创建节点列表并找出唯一的节点ID
#     nodes = set()
#     for line in edges:
#     # for line in lines[1:]:
#         from_node, to_node = line.strip().split(",")
#         nodes.add(from_node)
#         nodes.add(to_node)
#         G.add_edge(from_node, to_node)
#     return G, nodes

# def draw_graph(G, save_path=None, is_show=True):
#     '''
#         Draw graph G
#         The node size is determined based on the degree if arg node_size is None.
#     '''
#     #### draw graph ####
#     fig, ax = plt.subplots(figsize=(30, 15))
#     pos = nx.spring_layout(G, k=0.15, seed=4572321)
#     # node_color = [community_index[n] for n in H]
#     # if not isinstance(node_size, list):
#     node_size = [d * 3 for n, d in G.degree()]
#     nx.draw_networkx(
#         G,
#         pos=pos,
#         with_labels=False,
#         # node_color=node_color,
#         node_size=node_size,
#         edge_color="gainsboro",
#         width=1,
#         alpha=0.6,
#     )

#     # Title/legend
#     font = {"color": "k", "fontweight": "bold", "fontsize": 20}
#     # ax.set_title("Gene functional association network (C. elegans)", font)
#     # Change font color for legend
#     font["color"] = "r"

#     # ax.text(
#     #     0.80,
#     #     0.10,
#     #     "node color = community structure",
#     #     horizontalalignment="center",
#     #     transform=ax.transAxes,
#     #     fontdict=font,
#     # )
#     # ax.text(
#     #     0.80,
#     #     0.06,
#     #     "node size = betweenness centrality",
#     #     horizontalalignment="center",
#     #     transform=ax.transAxes,
#     #     fontdict=font,
#     # )

#     # Resize figure for label readability
#     # ax.margins(0.1, 0.05)
#     fig.tight_layout()
#     plt.axis("off")
#     if save_path is not None:
#         plt.savefig(save_path)
#     if is_show:
#         plt.show()
def draw_graph(g, save_path=None, is_show=True, pos=None, show_labels =True, node_color=None, edge_color=None, node_size=None, edge_size=None):
    fig, ax = plt.subplots(figsize=(12, 9))
    if pos is None:
        pos = nx.spring_layout(g, seed=draw_seed,k=0.15)
    nx.draw_networkx_nodes(g, pos, ax=ax,  node_color=node_color, node_size=node_size)  # node_size=20,
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.4, edge_color=edge_color, width=edge_size)

    # 显示节点编号（标签）
    if show_labels:
        nx.draw_networkx_labels(g, pos, ax=ax, font_size=12, font_color="black")  # 添加这行显示节点编号

    ax.set_title("Graph", fontsize=24)
    ax.set_axis_off()
    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    if is_show:
        plt.show()
    else:
        plt.close()
    


def find_subgraph(G):
    '''
        Remove nodes (degree < delete_degree_min)
        Find largest_component 
        Returns the corresponding subgraph
    '''
    # remove low-degree nodes
    # low_degree = [n for n, d in G.degree() if d < delete_degree_min]
    # G.remove_nodes_from(low_degree)
    print("number_connected_components:",nx.number_connected_components(G))

    # components = nx.connected_components(G)
    # component_graphs=[G.subgraph(c).copy() for c in components]

    # largest connected component
    largest_component = max(nx.connected_components(G), key=len)
    H = G.subgraph(largest_component)
    return H

def draw_betweenness_centrality(G):
    '''
        from:https://networkx.org/documentation/stable/auto_examples/algorithms/plot_betweenness_centrality.html
    '''

    # compute centrality
    centrality = nx.betweenness_centrality(G, k=10, endpoints=True) # 

    # compute community structure
    lpc = nx.community.label_propagation_communities(G)
    community_index = {n: i for i, com in enumerate(lpc) for n in com}

    #### draw graph ####
    fig, ax = plt.subplots(figsize=(12, 9), fontsize=24)
    pos = nx.spring_layout(G, k=0.15, seed=4572321)
    node_color = [community_index[n] for n in G]
    node_size = [v * 20000 for v in centrality.values()]
    nx.draw_networkx(
        G,
        pos=pos,
        with_labels=False,
        node_color=node_color,
        node_size=node_size,
        edge_color="gainsboro",
        alpha=0.4,
    )

    # Title/legend
    font = {"color": "k", "fontweight": "bold", "fontsize": 20}
    ax.set_title("Gene functional association network (C. elegans)", font)
    # Change font color for legend
    font["color"] = "r"

    ax.text(
        0.80,
        0.10,
        "node color = community structure",
        horizontalalignment="center",
        transform=ax.transAxes,
        fontdict=font,
    )
    ax.text(
        0.80,
        0.06,
        "node size = betweenness centrality",
        horizontalalignment="center",
        transform=ax.transAxes,
        fontdict=font,
    )

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")
    plt.show()

def reindex_graph(G):
    # 创建一个示例图

    # 获取原始节点列表
    original_nodes = list(G.nodes())

    # 创建一个新的图
    new_G = nx.Graph()

    # 创建节点映射
    node_mapping = {original_nodes[i]: i for i in range(len(original_nodes))}

    # 重新添加节点到新图中
    new_G.add_nodes_from(node_mapping.values())

    # 重新添加边
    for u, v in G.edges():
        new_G.add_edge(node_mapping[u], node_mapping[v])
    return new_G




