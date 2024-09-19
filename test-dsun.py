import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from main import build_graph

# build graph
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
print(g)

# draw graph
fig = plt.figure("Degree of a random graph", figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(5, 4)
ax0 = fig.add_subplot(axgrid[0:3, :])
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g, seed=10396953)
nx.draw_networkx_nodes(g, pos, ax=ax0, node_size=20)
nx.draw_networkx_edges(g, pos, ax=ax0, alpha=0.4)
ax0.set_title("Connected components of G")
ax0.set_axis_off()

# calculate diameter error: disconnected
# d = nx.diameter(g)
# print(d)

# calculate clustering coefficient
node_cc = nx.clustering(g)
print('all clustering coefficients:', node_cc)
for node in node_cc:
    cc = node_cc[node]
    if cc != 0:
        print('find a non-zero clustering coefficient:', cc)

# calculate average path length (of each connected component)
component_count = 1
for component in (g.subgraph(component).copy() for component in nx.connected_components(g)):
    print('average path length of component', component_count, ':',nx.average_shortest_path_length(component))
    component_count += 1

# calculate average degree
node_deg_pairs = nx.degree(g)
print('all degrees:', node_deg_pairs)
node_deg = 0
for pair in node_deg_pairs:
    node_deg += pair[1]
print('average degree:', node_deg / g.number_of_nodes())

# calculate and draw degree distribution
degree_sequence = sorted((d for n, d in node_deg_pairs), reverse=True)
ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")
ax2 = fig.add_subplot(axgrid[3:, 2:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")
fig.tight_layout()
plt.show()

# calculate betweenness:
print('all betweennesses:', nx.betweenness_centrality(g))
