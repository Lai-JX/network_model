import networkx as nx

def average_cluster_coefficient(g):
    node_cc = nx.clustering(g)
    cc_sum = 0
    for node in node_cc:
        cc_sum += node_cc[node]
    return cc_sum / g.number_of_nodes()