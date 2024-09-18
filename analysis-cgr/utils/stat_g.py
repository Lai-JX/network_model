import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt

G = nx.Graph()

# 读取txt文件
with open('processed_email-Eu-core-750.txt', 'r') as f:
    lines = f.readlines()

# 创建节点列表并找出唯一的节点ID
nodes = set()
for line in lines:
    from_node, to_node = line.strip().split()
    nodes.add(from_node)
    nodes.add(to_node)
    G.add_edge(from_node, to_node)

print(G)
# # 将节点按顺序排列
# node_list = sorted(list(nodes))
# print(len(node_list))
# # 创建一个矩阵并初始化为"N"
# matrix = [['N'] * (len(node_list) + 1) for _ in range(len(node_list) + 1)]

# # 填充矩阵的第一行和第一列
# matrix[0][0] = 'ID'
# for i, node in enumerate(node_list, start=1):
#     matrix[i][0] = node
#     matrix[0][i] = node

# # 将边的连接信息填入矩阵
# for line in lines:
#     from_node, to_node = line.strip().split()
#     row_idx = node_list.index(from_node) + 1
#     col_idx = node_list.index(to_node) + 1
#     matrix[row_idx][col_idx] = 'Y'
#     matrix[col_idx][row_idx] = 'Y'
#     if row_idx == col_idx:
#         matrix[col_idx][row_idx] = 'N'

# # 创建DataFrame
# df = pd.DataFrame(matrix)

# # 保存为xls文件
# df.to_csv('output_another.csv', index=True, header=False)