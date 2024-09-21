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
#########################################################



dataset_var = tk.StringVar()
def _build_graph():
    path = dataset_path_map[dataset_var.get()]
    G, nodes = build_graph(path, 500)
    H = find_subgraph(G)
    draw_graph(H, 'network.png', None, False)
    return
    



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

##############################################################################################
tk.Label(operation1, text="选择数据集",font=20).grid(padx=10, pady=10,row=0, column=0, sticky="w")
dataset_dropdown = ttk.Combobox(operation1, textvariable=dataset_var)
dataset_dropdown['values'] = ['musae_git_edges']
dataset_dropdown.current(0)
dataset_dropdown.grid(row=0, column=1, sticky="w", columnspan=2)

tk.Button(operation1, text="画图", command=_build_graph).grid(row=0, column=3, padx=(20,0), sticky="w")

tk.Label(operation1, text="计算clustering coefficient:", font=("黑体",14)).grid(row=1, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Label(operation1, text="选择顶点:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
clustering_vertex_spinbox = tk.Spinbox(operation1, from_=0, to=100, width=5)
clustering_vertex_spinbox.grid(row=2, column=1, pady=5, sticky="w")
tk.Button(operation1, text="输出").grid(row=2, column=2, sticky="w")
clustering_output = tk.Entry(operation1,width=10, )
clustering_output.grid(row=2, column=3, padx=(0,10), pady=10, sticky="w")
tk.Button(operation1, text="平均").grid(row=3, column=2, sticky="w")
clustering_avg_output = tk.Entry(operation1,width=10, )
clustering_avg_output.grid(row=3, column=3, padx=(0,10), pady=10, sticky="w")

##############################################################################################
# Degree 相关的布局
tk.Label(operation2, text="计算Degree:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Label(operation2, text="选择顶点:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
degree_vertex_spinbox = tk.Spinbox(operation2, from_=0, to=100, width=10)
degree_vertex_spinbox.grid(row=1, column=1,padx=10)
tk.Button(operation2, text="输出").grid(row=1, column=2,padx=10)
degree_output = tk.Entry(operation2, width=10)
degree_output.grid(row=1, column=3, padx=10)
tk.Button(operation2, text="显示度的分布").grid(row=2, column=0, padx=10, pady=5, columnspan=4)

# 计算平均最短路径
tk.Label(operation2, text="计算平均最短路径:", font=("黑体",14)).grid(row=3, column=0, padx=10, pady=5, sticky="w", columnspan=4)
tk.Button(operation2, text="输出").grid(row=4, column=0, padx=10, pady=5)
avg_path_output = tk.Entry(operation2, width=10)
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
