from random import sample
import networkx as nx
import matplotlib.pyplot as plt
from main import build_graph
# build graph
G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv', None)
print(G)
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])


# remove randomly selected nodes (to make example fast)
# num_to_remove = int(len(G) / 1.5)
# nodes = sample(list(G.nodes), num_to_remove)
# G.remove_nodes_from(nodes)

# remove low-degree nodes
low_degree = [n for n, d in G.degree() if d < 0]
G.remove_nodes_from(low_degree)
print(G)
print("number_connected_components:",nx.number_connected_components(G))

# largest connected component
components = nx.connected_components(G)
component_graphs=[G.subgraph(c).copy() for c in components]

largest_component = max(nx.connected_components(G), key=len)

H = G.subgraph(largest_component)
print(H)
# compute centrality
centrality = nx.betweenness_centrality(H, k=10, endpoints=True) # 

# compute community structure
lpc = nx.community.label_propagation_communities(H)
community_index = {n: i for i, com in enumerate(lpc) for n in com}

#### draw graph ####
fig, ax = plt.subplots(figsize=(20, 15))
pos = nx.spring_layout(H, k=0.15, seed=4572321)
node_color = [community_index[n] for n in H]
node_size = [v * 20000 for v in centrality.values()]
nx.draw_networkx(
    H,
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