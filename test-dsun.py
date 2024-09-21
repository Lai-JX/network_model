import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import false

from main import build_graph

# build graph
g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv', 500)
print(g)

# draw graph
fig = plt.figure("Degree of a random graph", figsize=(8, 21))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(21, 4)
ax0 = fig.add_subplot(axgrid[0:3, :])
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g, seed=10396953)
nx.draw_networkx_nodes(g, pos, ax=ax0, node_size=20)
nx.draw_networkx_edges(g, pos, ax=ax0, alpha=0.4)
ax0.set_title("G")
ax0.set_axis_off()

# calculate diameter error: disconnected
# d = nx.diameter(g)
# print(d)

# calculate clustering coefficient
node_cc = nx.clustering(g)
# print('all clustering coefficients:', node_cc)
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
# print('all degrees:', node_deg_pairs)
node_deg = 0
for pair in node_deg_pairs:
    node_deg += pair[1]
print('average degree:', node_deg / g.number_of_nodes())

# calculate and draw degree distribution

degree_sequence = sorted((d for n, d in node_deg_pairs), reverse=True)
ax1 = fig.add_subplot(axgrid[3:6, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[3:6, 2:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")


# calculate and draw coreness distribution and k-core of graph

node_coreness = nx.core_number(g)
print('all coreness:', node_coreness)
coreness_sequence = sorted(node_coreness.values(), reverse=True)
ax3 = fig.add_subplot(axgrid[6:10, :])
ax3.bar(*np.unique(coreness_sequence, return_counts=True))
ax3.set_title("Coreness histogram")
ax3.set_xlabel("Coreness")
ax3.set_ylabel("# of Nodes")

g3 = nx.k_core(g, 3)
ax4 = fig.add_subplot(axgrid[10:14, :])
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g3, seed=10396953)
nx.draw_networkx_nodes(g3, pos, ax=ax4, node_size=20)
nx.draw_networkx_edges(g3, pos, ax=ax4, alpha=0.4)
ax4.set_title("3-core of G")
ax4.set_axis_off()

g2 = nx.k_core(g, 2)
ax5 = fig.add_subplot(axgrid[14:18, :])
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g2, seed=10396953)
nx.draw_networkx_nodes(g2, pos, ax=ax5, node_size=20)
nx.draw_networkx_edges(g2, pos, ax=ax5, alpha=0.4)
ax5.set_title("2-core of G")
ax5.set_axis_off()

g1 = nx.k_core(g, 1)
ax6 = fig.add_subplot(axgrid[18:22, :])
# Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
pos = nx.spring_layout(g1, seed=10396953)
nx.draw_networkx_nodes(g1, pos, ax=ax6, node_size=20)
nx.draw_networkx_edges(g1, pos, ax=ax6, alpha=0.4)
ax6.set_title("2-core of G")
ax6.set_axis_off()

fig.tight_layout()
plt.show()

# closeness


