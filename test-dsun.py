import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from main import build_graph

# build graph
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv', 500)
g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
print(g)

# draw graph
# fig = plt.figure("Degree of a random graph", figsize=(8, 21))
fig, ax = plt.subplots(figsize=(20, 15))
# Create a gridspec for adding subplots of different sizes
# axgrid = fig.add_gridspec(21, 4)
# ax0 = fig.add_subplot(axgrid[0:3, :])
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g, seed=10396953)
nx.draw_networkx_nodes(g, pos, ax=ax, node_size=20)
nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.4)
ax.set_title("Graph")
ax.set_axis_off()
fig.tight_layout()
plt.show()

# calculate diameter error: disconnected

# d = nx.diameter(g)
# print(d)

# calculate clustering coefficient

node_cc = nx.clustering(g)
flag = True
for node in node_cc:
    cc = node_cc[node]
    if cc != 0:
        flag = False
        print('find a non-zero clustering coefficient:', cc)
if flag:
    print('all clustering coefficients are 0')

# calculate average path length (of each connected component)

component_count = 1
for component in (g.subgraph(component).copy() for component in nx.connected_components(g)):
    print('average path length of component', component_count, ':',nx.average_shortest_path_length(component))
    component_count += 1

# calculate average degree

node_deg_pairs = nx.degree(g)
node_deg = 0
for pair in node_deg_pairs:
    node_deg += pair[1]
print('average degree:', node_deg / g.number_of_nodes())

# calculate and draw degree distribution

degree_sequence = sorted((d for n, d in node_deg_pairs), reverse=True)
fig, ax = plt.subplots(figsize=(20, 15))
ax.plot(degree_sequence, "b-", marker="o")
ax.set_title("Degree Rank Plot")
ax.set_ylabel("Degree")
ax.set_xlabel("Rank")
fig.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(20, 15))
ax.bar(*np.unique(degree_sequence, return_counts=True), color='red')
ax.set_title("Degree histogram")
ax.set_xlabel("Degree")
ax.set_ylabel("# of Nodes")
fig.tight_layout()
plt.show()

# calculate and draw coreness distribution and k-core of graph

node_coreness = nx.core_number(g)
closeness_sequence = sorted(node_coreness.values(), reverse=True)
fig, ax = plt.subplots(figsize=(20, 15))
ax.bar(*np.unique(closeness_sequence, return_counts=True), width=0.1)
ax.set_title("Coreness histogram")
ax.set_xlabel("Coreness")
ax.set_ylabel("# of Nodes")
fig.tight_layout()
plt.show()

g3 = nx.k_core(g, 3)
fig, ax = plt.subplots(figsize=(20, 15))
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g3, seed=10396953)
nx.draw_networkx_nodes(g3, pos, ax=ax, node_size=20)
nx.draw_networkx_edges(g3, pos, ax=ax, alpha=0.4)
ax.set_title("3-core of G")
ax.set_axis_off()
fig.tight_layout()
plt.show()

g2 = nx.k_core(g, 2)
fig, ax = plt.subplots(figsize=(20, 15))
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g2, seed=10396953)
nx.draw_networkx_nodes(g2, pos, ax=ax, node_size=20)
nx.draw_networkx_edges(g2, pos, ax=ax, alpha=0.4)
ax.set_title("2-core of G")
ax.set_axis_off()
fig.tight_layout()
plt.show()


g1 = nx.k_core(g, 1)
fig, ax = plt.subplots(figsize=(20, 15))
# ax6 = fig.add_subplot(axgrid[18:22, :])
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g1, seed=10396953)
nx.draw_networkx_nodes(g1, pos, ax=ax, node_size=20)
nx.draw_networkx_edges(g1, pos, ax=ax, alpha=0.4)
ax.set_title("1-core of G")
ax.set_axis_off()
fig.tight_layout()
plt.show()

# calculate and draw closeness distributio
node_closeness = nx.closeness_centrality(g)
closeness_sequence = sorted(node_closeness.values(), reverse=True)
fig, ax = plt.subplots(figsize=(20, 15))
ax.bar(*np.unique(closeness_sequence, return_counts=True), width=0.005)
ax.set_title("Closeness histogram")
ax.set_xlabel("Closeness")
ax.set_ylabel("# of Nodes")
fig.tight_layout()
plt.show()


