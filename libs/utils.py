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

    print("before: ", G)
    G = find_subgraph(G)
    print("after: ",G)

    # reindex the graph to ensure node IDs are continuous and start from 0
    G = reindex_graph(G)

    # 记录pos，用于后续上色
    pos = nx.spring_layout(G, seed=seed, k=0.15)
    G.pos = pos

    return G

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
    # if pos is None:
    #     pos = nx.spring_layout(g, seed=draw_seed,k=0.15)
    nx.draw_networkx_nodes(g, pos, ax=ax,  node_color=node_color, node_size=node_size)  # node_size=20,
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.4, edge_color=edge_color, width=edge_size)

    # 显示节点编号（标签）
    if show_labels:
        nx.draw_networkx_labels(g, pos, ax=ax, font_size=8, font_color="black",)  # 添加这行显示节点编号

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
    original_nodes.sort()  # 确保节点按字母顺序排序
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




## This code is part of the CDlib library, which is used for community detection in networks.
## Rewritten by the CDlib team, this function visualizes communities in a given ax.
import warnings
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import networkx as nx
from cdlib import NodeClustering
from cdlib.utils import convert_graph_formats

COLOR = (
    (1, 0, 0),
    (0, 0, 1),
    (0, 0.5, 0),
    (0, 0.75, 0.75),
    (0.75, 0, 0.75),
    (0.75, 0.75, 0),
    (0, 0, 0),
    (0.8, 0.8, 0.8),
    (0.2, 0.2, 0.2),
    (0.6, 0.6, 0.6),
    (0.4, 0.4, 0.4),
    (0.7, 0.7, 0.7),
    (0.3, 0.3, 0.3),
    (0.9, 0.9, 0.9),
    (0.1, 0.1, 0.1),
    (0.5, 0.5, 0.5),
)

def __filter(partition: list, top_k: int, min_size: int) -> list:
    if isinstance(min_size, int) and min_size > 0:
        partition = list(filter(lambda nodes: len(nodes) >= min_size, partition))
    if isinstance(top_k, int) and top_k > 0:
        partition = partition[:top_k]
    return partition

def plot_network_highlighted_clusters(
    graph: object,
    partition: NodeClustering,
    position: dict = None,
    figsize: tuple = (8, 8),
    node_size: int = 200,  # 200 default value
    plot_overlaps: bool = False,
    plot_labels: bool = False,
    cmap: object = None,
    top_k: int = None,
    min_size: int = None,
    edge_weights_intracluster: int = 200,
    ax: object = None,
) -> object:
    """
    This function plots a network with highlighted communities, node color coding for communities and draws polygons around clusters. It utilizes spring_layout from NetworkX to position nodes, bringing intra-cluster nodes closer. When considering edge weights, this layout adjusts node positions accordingly, facilitating clearer visualizations of community structures.

    :param graph: NetworkX/igraph graph
    :param partition: NodeClustering object
    :param position: A dictionary with nodes as keys and positions as values. Example: networkx.fruchterman_reingold_layout(G). By default, uses nx.spring_layout(g)
    :param figsize: the figure size; it is a pair of float, default (8, 8)
    :param node_size: int, the size of nodes. Default is 200.
    :param plot_overlaps: bool, default False. Flag to control if multiple algorithms memberships are plotted.
    :param plot_labels: bool, default False. Flag to control if node labels are plotted.
    :param cmap: str or Matplotlib colormap, Colormap(Matplotlib colormap) for mapping intensities of nodes. If set to None, original colormap is used.
    :param top_k: int, Show the top K influential communities. If set to zero or negative value indicates all.
    :param min_size: int, Exclude communities below the specified minimum size.
    :param edge_weights_intracluster: The weight of the edges within clusters. Useful for spring_layout.

    Example:

    >>> from cdlib import algorithms, viz
    >>> import networkx as nx
    >>> g = nx.karate_club_graph()
    >>> coms = algorithms.louvain(g)
    >>> position = nx.spring_layout(g)
    >>> viz.plot_network_highlighted_clusters(g, coms, position)
    """
    if not isinstance(cmap, (type(None), str, matplotlib.colors.Colormap)):
        raise TypeError(
            f"The 'cmap' argument must be NoneType, str or matplotlib.colors.Colormap, not{type(cmap).__name__}."
        )

    partition = __filter(partition.communities, top_k, min_size)
    graph = convert_graph_formats(graph, nx.Graph)

    # Assign weight of edge_weights_intracluster (default value is 200) or 1 to intra-community edges
    for community in partition:
        intra_community_edges = [(u, v) for u, v in graph.edges(community)]
        for edge in intra_community_edges:
            if all(node in community for node in edge):
                graph[edge[0]][edge[1]]["weight"] = edge_weights_intracluster
            else:
                graph[edge[0]][edge[1]]["weight"] = 1

    # Update node positions based on edge weights
    position = nx.spring_layout(graph, weight="weight", pos=position)

    n_communities = len(partition)
    if n_communities == 0:
        warnings.warn("There are no communities that match the filter criteria.")
        return None

    if cmap is None:
        n_communities = min(n_communities, len(COLOR))
        cmap = matplotlib.colors.ListedColormap(COLOR[:n_communities])
    else:
        cmap = plt.cm.get_cmap(cmap, n_communities)
    _norm = matplotlib.colors.Normalize(vmin=0, vmax=n_communities - 1)
    fontcolors = list(
        map(
            lambda rgb: ".15" if np.dot(rgb, [0.2126, 0.7152, 0.0722]) > 0.408 else "w",
            [cmap(_norm(i))[:3] for i in range(n_communities)],
        )
    )
    if ax is None:
        plt.figure(figsize=figsize)
        plt.axis("off")

    filtered_nodelist = list(np.concatenate(partition))
    filtered_edgelist = list(
        filter(
            lambda edge: len(np.intersect1d(edge, filtered_nodelist)) == 2,
            graph.edges(),
        )
    )
    if isinstance(node_size, int):
        fig = nx.draw_networkx_nodes(
            graph,
            position,
            node_size=node_size,
            node_color="w",
            nodelist=filtered_nodelist,
            ax=ax,
        )
        fig.set_edgecolor("k")

    filtered_edge_widths = [1] * len(filtered_edgelist)

    nx.draw_networkx_edges(
        graph,
        position,
        alpha=0.25,
        edgelist=filtered_edgelist,
        width=filtered_edge_widths,
        ax=ax,
    )

    if plot_labels:
        nx.draw_networkx_labels(
            graph,
            position,
            font_color=".8",
            labels={node: str(node) for node in filtered_nodelist},
            ax=ax,
        )

    for i in range(n_communities):
        if len(partition[i]) > 0:
            if plot_overlaps:
                size = (n_communities - i) * node_size
            else:
                size = node_size
            fig = nx.draw_networkx_nodes(
                graph,
                position,
                node_size=size,
                nodelist=partition[i],
                node_color=[cmap(_norm(i))],
                ax=ax,
            )
            fig.set_edgecolor("k")

    # Plotting highlighted clusters
    for i, community in enumerate(partition):
        if len(community) > 0:
            # Extracting coordinates of community nodes
            x_values = [position[node][0] for node in community]
            y_values = [position[node][1] for node in community]

            min_x, max_x = min(x_values), max(x_values)
            min_y, max_y = min(y_values), max(y_values)

            # Create a polygon using the min and max coordinates
            polygon = Polygon(
                [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)],
                edgecolor=cmap(_norm(i)),
                facecolor=cmap(_norm(i)),
                alpha=0.3,
            )
            (ax or plt.gca()).add_patch(polygon)

            # Extracting edges intra-community
            intra_community_edges = [
                (u, v) for u, v in graph.edges() if u in community and v in community
            ]

            # Plot edges intra-community with the color of the community and increased width
            nx.draw_networkx_edges(
                graph,
                position,
                edgelist=intra_community_edges,
                edge_color=[cmap(_norm(i))],  # Use color of the community
                width=2,  # Increase edge width
                ax=ax,
            )

    if plot_labels:
        for i in range(n_communities):
            if len(partition[i]) > 0:
                nx.draw_networkx_labels(
                    graph,
                    position,
                    font_color=fontcolors[i],
                    labels={node: str(node) for node in partition[i]},
                    ax=ax,
                )
    return fig