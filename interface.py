import tkinter as tk
from tkinter import *
from tkinter import ttk
import networkx as nx
# import main

from main import build_graph, find_subgraph, draw_graph
from degree import draw_degree_rank
from cluster_coefficient import average_cluster_coefficient
from coreness import draw_k_core
from PIL import Image, ImageTk

#########################################################
root = Tk()
root.title("Modeling of Complex Networks")
# root.iconbitmap("my_icon.ico")
root.geometry("1200x800+200+100")    
# root.resizable(False, False)

# graph
image_path = './data/network.png'
image = ImageTk.PhotoImage(Image.open(image_path).resize((1200,600)))     # .resize((800,400))
image_label=Label(root, image=image)
image_label.pack()

# operate
operation = Frame(root, width=1200, height=200)
operation.pack()
##############################################################################################

operation1 = Frame(operation, width=400, height=200,)
operation1.grid(row=0, column=0)
operation1.grid_propagate(0)

operation2 = Frame(operation, width=400, height=200)
operation2.grid(row=0, column=1)
operation2.grid_propagate(0)

operation3 = Frame(operation, width=400, height=200)
operation3.grid(row=0, column=2)
operation3.grid_propagate(0)
#########################################################

global G
# G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv', 1000)
# G = find_subgraph(G)
# draw_graph(G, 'network.png', False)

dataset_var = tk.IntVar()

coefficient_node = tk.StringVar()

degree_node = tk.StringVar()

coreness_node = tk.StringVar()

def _build_graph():
    seed = dataset_var.get()
    global G
    G = None
    G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv', 8000, seed)
    print("before: ", G)
    G = find_subgraph(G)
    print("after: ",G)

    draw_graph(G, f'./data/network-{seed}.png', False)
    _image = ImageTk.PhotoImage(Image.open(f'./data/network-{seed}.png').resize((1200,600)))     # .resize((800,400))

    image_label.configure(image = _image)
    image_label.image = _image      # 这步很重要，防止图片被垃圾回收

    clustering_vertex_spinbox.configure(values=list(G.nodes))
    clustering_vertex_spinbox.values = list(G.nodes)
    degree_vertex_spinbox.configure(values=list(G.nodes))
    degree_vertex_spinbox.values = list(G.nodes)
    coreness_vertex_spinbox.configure(values=list(G.nodes))
    coreness_vertex_spinbox.values = list(G.nodes)

    diameter_output.configure(text=nx.diameter(G))
    diameter_output.text = nx.diameter(G)

    clustering_avg_output.configure(text=nx.average_clustering(G))
    clustering_avg_output.text = nx.average_clustering(G)

    print(nx.average_shortest_path_length(G))

    avg_path_output.configure(text = round(nx.average_shortest_path_length(G), 4))
    avg_path_output.text = round(nx.average_shortest_path_length(G), 4)


def output_coefficient():
    node = coefficient_node.get()
    coefficient = nx.clustering(G, node)
    print(G)
    print(coefficient)
    clustering_output.configure(text=coefficient)
    clustering_output.text = coefficient

def output_degree():
    node = degree_node.get()
    degree = G.degree[node]
    degree_output.configure(text=degree)
    degree_output.text=degree

def show_degree_distribution():
    draw_degree_rank(G, './data/degree_distribution.png', False)
    top = Toplevel(operation2)
    image_path = './data/degree_distribution.png'
    image = ImageTk.PhotoImage(Image.open(image_path).resize((800,600)))     # .resize((800,400))
    image_label=Label(top, image=image)
    image_label.pack()
    mainloop()

def output_coreness():
    node = coreness_node.get()
    coreness = nx.core_number(G)[node]
    coreness_output.configure(text=coreness)
    coreness_output.text=coreness

def show_1core_distribution():
    draw_k_core(G, 1, './data/1-core.png', False)
    top = Toplevel(operation3)
    image_path = './data/1-core.png'
    image = ImageTk.PhotoImage(Image.open(image_path).resize((800,600)))     # .resize((800,400))
    image_label=Label(top, image=image)
    image_label.pack()
    mainloop()

def show_2core_distribution():
    draw_k_core(G, 2, './data/2-core.png', False)
    top = Toplevel(operation3)
    image_path = './data/2-core.png'
    image = ImageTk.PhotoImage(Image.open(image_path).resize((800,600)))     # .resize((800,400))
    image_label=Label(top, image=image)
    image_label.pack()
    mainloop()

def show_3core_distribution():
    draw_k_core(G, 3, './data/3-core.png', False)
    top = Toplevel(operation3)
    image_path = './data/3-core.png'
    image = ImageTk.PhotoImage(Image.open(image_path).resize((800,600)))     # .resize((800,400))
    image_label=Label(top, image=image)
    image_label.pack()
    mainloop()




##############################################################################################
tk.Label(operation1, text="选择数据集",font=20).grid(padx=10, pady=10,row=0, column=0, sticky="w")
dataset_dropdown = tk.Entry(operation1,  textvariable=dataset_var)
dataset_dropdown.grid(row=7, column=1, padx=10, pady=5)
dataset_dropdown.grid(row=0, column=1, sticky="w", columnspan=2)

tk.Button(operation1, text="画图", command=_build_graph).grid(row=0, column=3, padx=(20,0), sticky="w")

tk.Label(operation1, text="直径",font=18).grid(row=1, column=0, padx=10,  pady=5)
diameter_output = tk.Label(operation1, text=0, width=10, background='white')
diameter_output.grid(row=1, column=1, pady=5)

tk.Label(operation1, text="计算clustering coefficient:", font=("黑体",14)).grid(row=2, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Label(operation1, text="选择顶点:").grid(row=3, column=0, padx=10, pady=5, sticky="w")

clustering_vertex_spinbox = ttk.Combobox(operation1, textvariable=coefficient_node, width=10)
# clustering_vertex_spinbox['values'] = list([1])
# clustering_vertex_spinbox.current(0)
clustering_vertex_spinbox.grid(row=3, column=1, pady=5, sticky="w")
tk.Button(operation1, text="输出", command=output_coefficient).grid(row=3, column=2, sticky="w")
clustering_output = tk.Label(operation1,width=10, text=0, background='white')
clustering_output.grid(row=3, column=3, padx=(0,10), pady=10, sticky="w")
tk.Button(operation1, text="平均").grid(row=4, column=2, sticky="w")
clustering_avg_output = tk.Label(operation1,width=10, background='white')
clustering_avg_output.grid(row=4, column=3, padx=(0,10), pady=10, sticky="w")

##############################################################################################
# Degree 相关的布局
tk.Label(operation2, text="计算Degree:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Label(operation2, text="选择顶点:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
degree_vertex_spinbox = ttk.Combobox(operation2, textvariable=degree_node, width=10)
# degree_vertex_spinbox['values'] = list([1])
# degree_vertex_spinbox.current(0)
degree_vertex_spinbox.grid(row=1, column=1,padx=10)
tk.Button(operation2, text="输出",command=output_degree).grid(row=1, column=2,padx=10)
degree_output = tk.Label(operation2, width=10, background='white')
degree_output.grid(row=1, column=3, padx=10, )
tk.Button(operation2, text="显示度的分布", command=show_degree_distribution).grid(row=2, column=0, padx=10, pady=5, columnspan=4)

# 计算平均最短路径
tk.Label(operation2, text="计算平均最短路径:", font=("黑体",14)).grid(row=3, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Button(operation2, text="输出", ).grid(row=4, column=0, padx=10, pady=5)
avg_path_output = tk.Label(operation2, width=10, background='white')
avg_path_output.grid(row=4, column=1, padx=10, pady=5)

##############################################################################################
# 计算 coreness
tk.Label(operation3, text="计算coreness:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=5, sticky="w",columnspan=4)
tk.Label(operation3, text="选择顶点:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
coreness_vertex_spinbox = ttk.Combobox(operation3, textvariable=coreness_node, width=10)
# coreness_vertex_spinbox['values'] = list([1])
# coreness_vertex_spinbox.current(0)
coreness_vertex_spinbox.grid(row=1, column=1, pady=5, padx=10)
tk.Button(operation3, text="输出", command=output_coreness).grid(row=1, column=2, pady=5, padx=10)
coreness_output = tk.Label(operation3, width=10, background='white')
coreness_output.grid(row=1, column=3, pady=5,padx=10)

tk.Label(operation3, text="计算图的coreness:", font=("黑体",14)).grid(row=2, column=0, padx=10, pady=5, sticky="w",columnspan=4)
tk.Button(operation3, text="1-core", command=show_1core_distribution).grid(row=3, column=0, padx=(20,10), pady=5)
tk.Button(operation3, text="2-core", command=show_2core_distribution).grid(row=3, column=1, padx=10,  pady=5)
tk.Button(operation3, text="3-core", command=show_1core_distribution).grid(row=3, column=2, padx=10,  pady=5)

# 测试图的鲁棒性
tk.Label(operation3, text="测试图的鲁棒性:").grid(row=4, column=0, padx=10, pady=5, sticky="w",columnspan=4)
tk.Button(operation3, text="随机的攻击测试").grid(row=4, column=1, columnspan=2)
tk.Button(operation3, text="有意的攻击测试").grid(row=4, column=2, columnspan=2)


root.mainloop()
