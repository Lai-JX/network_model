import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt

# 1. 从txt文件中加载网络
nodes = set()
G = nx.Graph()
with open('facebook_combined.txt', 'r') as file:
    for line in file:
        from_node, to_node = map(int, line.strip().split())
        nodes.add(from_node)
        nodes.add(to_node)
        G.add_edge(from_node, to_node)


# print(len(nodes))
random_nodes = list(random.sample(nodes, 3700))
# 2. 可以在这里进行网络分析和简化操作
#    例如，你可以使用NetworkX提供的函数来删除节点或边，或者进行其他操作来简化网络结构
# print(G)
# node_to_remove = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
G.remove_nodes_from(random_nodes)

# nx.draw(G, node_size=20)
# plt.show()

print(G)
# 3. 将处理后的网络导出到txt文件
with open('processed_facebook_combined-another.txt', 'w') as file:
    for edge in G.edges():
        from_node, to_node = edge
        file.write(f"{from_node} {to_node}\n")

# 读取txt文件
with open('processed_facebook_combined-another.txt', 'r') as f:
    lines = f.readlines()

# 创建节点列表并找出唯一的节点ID
nodes = set()
for line in lines:
    from_node, to_node = line.strip().split()
    nodes.add(from_node)
    nodes.add(to_node)

# 将节点按顺序排列
node_list = sorted(list(nodes))
print(len(node_list))
# 创建一个矩阵并初始化为"N"
matrix = [['N'] * (len(node_list) + 1) for _ in range(len(node_list) + 1)]

# 填充矩阵的第一行和第一列
matrix[0][0] = 'ID'
for i, node in enumerate(node_list, start=1):
    matrix[i][0] = node
    matrix[0][i] = node

# 将边的连接信息填入矩阵
for line in lines:
    from_node, to_node = line.strip().split()
    row_idx = node_list.index(from_node) + 1
    col_idx = node_list.index(to_node) + 1
    matrix[row_idx][col_idx] = 'Y'
    matrix[col_idx][row_idx] = 'Y'
    if row_idx == col_idx:
        matrix[col_idx][row_idx] = 'N'

# 创建DataFrame
df = pd.DataFrame(matrix)

# 保存为xls文件
df.to_csv('output_facebook_combined.csv', index=True, header=False)