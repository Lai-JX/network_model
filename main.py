import networkx as nx
import matplotlib.pyplot as plt
import random
random.seed(2024)

def build_graph(data_path, num_sample=1000):
    G = nx.Graph()

    # 读取txt文件
    with open(data_path, 'r') as f:
        lines = f.readlines()
    edges = random.sample(lines[1:num_sample+1], num_sample)

    # 创建节点列表并找出唯一的节点ID
    nodes = set()
    for line in edges:
        from_node, to_node = line.strip().split(",")
        nodes.add(from_node)
        nodes.add(to_node)
        G.add_edge(from_node, to_node)
    return G, nodes

g, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
print(g)
nx.draw(G=g,node_size=10)
plt.show()
