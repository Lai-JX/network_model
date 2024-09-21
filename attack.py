import networkx as nx
import copy
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from main import build_graph, find_subgraph, draw_graph, draw_seed
from betweenness import random_attack_edge_betweenness, random_attack_node_betweenness

class Attack_base:
    def __init__(self, parent_container, graph_seed, G):
        self.parent_container = parent_container
        self.graph_seed = graph_seed
        self.draw_seed = draw_seed
        self.pos = nx.spring_layout(G, seed=draw_seed)
        self.G = copy.deepcopy(G)
        self._g = copy.deepcopy(G)

        self.g_diameter = round(nx.diameter(G),4)
        self.average_clustering = round(nx.average_clustering(G),4)
        self.average_shortest_path_length = round(nx.average_shortest_path_length(G),4)
        self.connected_components = round(nx.number_connected_components(G),4)

    def window(self):
        top = Toplevel(self.parent_container, width=800, height=900)

        graph = Frame(top, width=600, height=900)
        graph.pack(side='left')
        _operation = Frame(top, width=200, height=900)
        _operation.pack(side='left')


        image_pre = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}.png').resize((600,450)))     # .resize((800,400))
        image_label_pre=Label(graph, image=image_pre)
        image_label_pre.pack()

        image_after = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}.png').resize((600,450)))     # .resize((800,400))
        self.image_label_after=Label(graph, image=image_after)
        self.image_label_after.pack()

        show_frame = Frame(_operation, height= 500)
        show_frame.pack()

        attack_frame = Frame(_operation)
        attack_frame.pack(expand=True)


        # 创建行标题的 Treeview
        row_headers = ttk.Treeview(show_frame, show="headings",height=4)
        row_headers["columns"] = ("Row")
        row_headers.heading("Row", text="属性")
        row_headers.column("Row", width=150, anchor="center")

        # 添加行标题数据
        row_headers.insert("", "end", values=("Diameter",))
        row_headers.insert("", "end", values=("Clustering coefficient",))
        row_headers.insert("", "end", values=("Average Path Length",))
        row_headers.insert("", "end", values=("Connected Components",))

        # 放置行标题的 Treeview
        row_headers.grid(row=0, column=0, sticky="nsew")

        # 创建主表格
        tree = ttk.Treeview(show_frame, columns=("before", "after"), show='headings',height=4)
        self.tree = tree
        # 设置每列的标题
        tree.heading("before", text="攻击前")
        tree.heading("after", text="攻击后")

        # 设置每列的宽度
        tree.column("before", width=50)
        tree.column("after", width=50)

        # 插入一些初始数据
        tree.insert("", "end", values=(self.g_diameter,self.g_diameter))
        tree.insert("", "end", values=(self.average_clustering, self.average_clustering))
        tree.insert("", "end", values=(self.average_shortest_path_length, self.average_shortest_path_length))
        tree.insert("", "end", values=(self.connected_components, self.connected_components))

        # 放置主表格
        tree.grid(row=0, column=1, sticky="nsew")

        self.set_attack_frame(attack_frame)
        tk.Button(attack_frame, text="重置", command=self.reset, width=10).grid(row=4, column=0, pady=15, padx=10, sticky="w", columnspan=2)

        
        mainloop()
    
    def set_attack_frame(self, attack_frame):
        tk.Label(attack_frame, text="攻击边:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=2)
        tk.Button(attack_frame, text="开始一次攻击", command=self.attack_edge).grid(row=1, column=0, padx=(20,10), sticky="w", columnspan=2)

        tk.Label(attack_frame, text="攻击点:", font=("黑体",14)).grid(row=2, column=0, padx=10, pady=5, sticky="w", columnspan=2)
        tk.Button(attack_frame, text="开始一次攻击", command=self.attack_node).grid(row=3, column=0, padx=(20,10), sticky="w", columnspan=2)

        
    def reset(self):
        self._g = copy.deepcopy(self.G)

        self.g_diameter = round(nx.diameter(self.G),4)
        self.average_clustering = round(nx.average_clustering(self.G),4)
        self.average_shortest_path_length = round(nx.average_shortest_path_length(self.G),4)
        self.connected_components = round(nx.number_connected_components(self.G),4)

        _image = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}.png').resize((600,450)))     # .resize((800,400))
        self.image_label_after.configure(image = _image)
        self.image_label_after.image = _image      # 这步很重要，防止图片被垃圾回收

        self.modify_data_in_table(0,1, self.g_diameter)
        self.modify_data_in_table(1,1, self.average_clustering)
        self.modify_data_in_table(2,1, self.average_shortest_path_length)
        self.modify_data_in_table(3,1, self.connected_components)




    def attack_edge(self):
        self._g, attacked_edge, attacked_betweenness = random_attack_edge_betweenness(self._g)
        print('attack_edge', self._g, attacked_edge, attacked_betweenness)
        self.attack_method()

    def attack_node(self):
        self._g, attacked_node, attacked_betweenness = random_attack_node_betweenness(self._g)
        print('attack_edge',self._g, attacked_node, attacked_betweenness)
        self.attack_method()

        

    def modify_data_in_table(self, row_index, col_index, new_value):
        items = self.tree.get_children()
        
        if row_index < len(items):
            item_id = items[row_index]
            current_values = list(self.tree.item(item_id, "values"))
            
            if col_index < len(current_values):
                current_values[col_index] = round(new_value,4) if not isinstance(new_value, str) else new_value
                self.tree.item(item_id, values=current_values)
            else:
                print("列索引超出范围")
        else:
            print("行索引超出范围")
    def attack_method(self):
        draw_graph(self._g, f'./data/network-{self.graph_seed}-after.png', False, self.pos)

        num = nx.number_connected_components(self._g)
        if num > 1:
            h = find_subgraph(self._g)
            self.modify_data_in_table(0,1, nx.diameter(h))
            self.modify_data_in_table(2,1, nx.average_shortest_path_length(h))
        else:
            self.modify_data_in_table(0,1, nx.diameter(self._g))
            self.modify_data_in_table(2,1, nx.average_shortest_path_length(self._g))
        self.modify_data_in_table(1,1, nx.average_clustering(self._g))
        self.modify_data_in_table(3,1, num)

        _image = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}-after.png').resize((600,450)))     # .resize((800,400))
        self.image_label_after.configure(image = _image)
        self.image_label_after.image = _image      # 这步很重要，防止图片被垃圾回收

