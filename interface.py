import tkinter as tk
from tkinter import *
from tkinter import ttk
# import main

from main import *
from PIL import Image, ImageTk

dataset_path_map = {
    'musae_git_edges':'./data/git_web_ml/musae_git_edges.csv'
}
#########################################################
root = Tk()
root.title("Modeling of Complex Networks")
# root.iconbitmap("my_icon.ico")
root.geometry("1200x800+200+100")    
# root.resizable(False, False)

# graph
image_path = './network.png'
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


G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv', 1000)
G = find_subgraph(G)

dataset_var = tk.StringVar()
coefficient_node = tk.StringVar()
coefficient_var = tk.DoubleVar()
coefficient_avg_var = tk.DoubleVar()
coefficient_avg_var.set(nx.average_clustering(G))

degree_node = tk.StringVar()
degree_var = tk.IntVar()

path_length_avg_var = tk.DoubleVar()
path_length_avg_var.set(nx.average_shortest_path_length(G))

def _build_graph():
    path = dataset_path_map[dataset_var.get()]
    G, nodes = build_graph(path, 500)
    H = find_subgraph(G)
    draw_graph(H, 'network.png', None, False)
    return

def output_coefficient():
    node = coefficient_node.get()
    coefficient = nx.clustering(G, node)
    print(coefficient)
    coefficient_var.set(coefficient)

def output_degree():
    node = degree_node.get()
    degree = G.degree[node]
    degree_var.set(degree)

def show_degree_distribution():

    top = Toplevel(operation2)
    image_path = './degree_distribution.png'
    image = ImageTk.PhotoImage(Image.open(image_path).resize((800,600)))     # .resize((800,400))
    image_label=Label(top, image=image)
    image_label.pack()
    mainloop()




##############################################################################################
tk.Label(operation1, text="选择数据集",font=20).grid(padx=10, pady=10,row=0, column=0, sticky="w")
dataset_dropdown = ttk.Combobox(operation1, textvariable=dataset_var)
dataset_dropdown['values'] = ['musae_git_edges']
dataset_dropdown.current(0)
dataset_dropdown.grid(row=0, column=1, sticky="w", columnspan=2)

tk.Button(operation1, text="画图", command=_build_graph).grid(row=0, column=3, padx=(20,0), sticky="w")

tk.Label(operation1, text="计算clustering coefficient:", font=("黑体",14)).grid(row=1, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Label(operation1, text="选择顶点:").grid(row=2, column=0, padx=10, pady=5, sticky="w")

clustering_vertex_spinbox = ttk.Combobox(operation1, textvariable=coefficient_node)
clustering_vertex_spinbox['values'] = list(G.nodes)
dataset_dropdown.current(0)
clustering_vertex_spinbox.grid(row=2, column=1, pady=5, sticky="w")
tk.Button(operation1, text="输出", command=output_coefficient).grid(row=2, column=2, sticky="w")
clustering_output = tk.Entry(operation1,width=10, textvariable=coefficient_var)
clustering_output.grid(row=2, column=3, padx=(0,10), pady=10, sticky="w")
tk.Button(operation1, text="平均").grid(row=3, column=2, sticky="w")
clustering_avg_output = tk.Entry(operation1,width=10, textvariable=coefficient_avg_var)
clustering_avg_output.grid(row=3, column=3, padx=(0,10), pady=10, sticky="w")

##############################################################################################
# Degree 相关的布局
tk.Label(operation2, text="计算Degree:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Label(operation2, text="选择顶点:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
degree_vertex_spinbox = ttk.Combobox(operation2, textvariable=degree_node)
degree_vertex_spinbox['values'] = list(G.nodes)
degree_vertex_spinbox.grid(row=1, column=1,padx=10)
tk.Button(operation2, text="输出",command=output_degree).grid(row=1, column=2,padx=10)
degree_output = tk.Entry(operation2, width=10, textvariable=degree_var)
degree_output.grid(row=1, column=3, padx=10, )
tk.Button(operation2, text="显示度的分布", command=show_degree_distribution).grid(row=2, column=0, padx=10, pady=5, columnspan=4)

# 计算平均最短路径
tk.Label(operation2, text="计算平均最短路径:", font=("黑体",14)).grid(row=3, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Button(operation2, text="输出", ).grid(row=4, column=0, padx=10, pady=5)
avg_path_output = tk.Entry(operation2, width=10, textvariable=path_length_avg_var)
avg_path_output.grid(row=4, column=1, padx=10, pady=5)

##############################################################################################
# 计算 coreness
tk.Label(operation3, text="计算coreness:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=5, sticky="w",columnspan=4)
tk.Label(operation3, text="选择顶点:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
coreness_vertex_spinbox = tk.Spinbox(operation3, from_=0, to=100, width=10)
coreness_vertex_spinbox.grid(row=1, column=1, pady=5, padx=10)
tk.Button(operation3, text="输出").grid(row=1, column=2, pady=5, padx=10)
coreness_output = tk.Entry(operation3, width=10)
coreness_output.grid(row=1, column=3, pady=5,padx=10)

tk.Label(operation3, text="计算图的coreness:", font=("黑体",14)).grid(row=2, column=0, padx=10, pady=5, sticky="w",columnspan=4)
tk.Button(operation3, text="输出").grid(row=3, column=0, padx=10,  pady=5)
graph_coreness_output = tk.Entry(operation3)
graph_coreness_output.grid(row=3, column=1, pady=5)

# 测试图的鲁棒性
tk.Label(operation3, text="测试图的鲁棒性:").grid(row=4, column=0, padx=10, pady=5, sticky="w",columnspan=4)
tk.Button(operation3, text="随机的攻击测试").grid(row=4, column=1, columnspan=2)
tk.Button(operation3, text="有意的攻击测试").grid(row=4, column=2, columnspan=2)


root.mainloop()
