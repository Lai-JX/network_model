import networkx as nx
import copy
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import build_graph, find_subgraph, draw_graph, draw_seed
from betweenness import random_attack_edge_betweenness, random_attack_node_betweenness, get_max_betweenness_edge, \
    get_max_betweenness_node, intentional_attack_edge_betweenness,  intentional_attack_node_betweenness
from degree import intentional_attack_node_degree
from coreness import intentional_attack_node_coreness
from closeness import intentional_attack_node_closeness
node_function_map = {
    'max_degree' : intentional_attack_node_degree,
    'max_betweenness' : intentional_attack_node_betweenness,
    'max_coreness' : intentional_attack_node_coreness,
    'max_closeness': intentional_attack_node_closeness
}

edge_function_map = {
    'max_betweenness' : intentional_attack_edge_betweenness,
}
class Attack_base:
    def __init__(self, parent_container, graph_seed, G):
        self.parent_container = parent_container
        self.graph_seed = graph_seed
        self.draw_seed = draw_seed
        self.pos = nx.spring_layout(G, seed=draw_seed, k=0.15)
        self.G = copy.deepcopy(G)
        self._g = copy.deepcopy(G)

        self.g_diameter = round(nx.diameter(G),4)
        self.average_clustering = round(nx.average_clustering(G),4)
        self.average_shortest_path_length = round(nx.average_shortest_path_length(G),4)
        self.connected_components = round(nx.number_connected_components(G),4)

        # 用于控制攻击的标志
        self.stop_attack = False
        # 初始化折线图数据
        self.attack_count = 0  # 攻击次数
        self.max_subgraph_sizes = []  # 存储每次攻击后的最大子图节点数

        # 初始化折线图 Figure
        self.fig, self.ax = plt.subplots(figsize=(4, 3))
        self.ax.set_xlabel("Attack Count")
        self.ax.set_ylabel("Max Subgraph Size")
        self.line, = self.ax.plot([], [], 'r-')  # 初始化折线图的线
        self.ax.set_xlim(0, 100)  # 攻击次数的范围，可以动态调整
        self.ax.set_ylim(0, len(G.nodes))  # 节点数范围是图的总节点数
        self.fig.tight_layout()
        self.removed_elements = []

        self.attack_edge_num = tk.IntVar()
        self.attack_node_num = tk.IntVar()



    def update_max_subgraph_label(self):
        """
        计算并更新最大连通子图的节点数，更新右上角的折线图数据
        """
        max_subgraph = max(nx.connected_components(self._g), key=len)  # 找到节点最多的子图
        max_subgraph_size = len(max_subgraph)  # 计算最大子图的节点数
        self.max_subgraph_sizes.append(max_subgraph_size)  # 保存最大子图的节点数
        self.attack_count += 1  # 增加攻击次数

    def update_line_chart(self):
        """
        更新右上角的折线图，动态显示最大子图节点数
        """
        # 更新折线图数据
        self.line.set_data(range(self.attack_count), self.max_subgraph_sizes)
        self.ax.set_xlim(0, max(100, self.attack_count))  # 动态调整 x 轴范围
        self.ax.set_ylim(0, max(self.max_subgraph_sizes) + 10)  # 动态调整 y 轴范围
        self.fig.tight_layout()
        # 更新折线图，显示当前删除的节点或边
        self.canvas.draw()  # 刷新图表

    def update_removed_display(self, element):
        """
        更新显示已删除的节点或边
        """
        # 判断是边还是节点
        if isinstance(element, tuple):
            text = f"{element}"
        else:
            text = f"{element}"
        
        # 更新 Label 内容，将新的删除项添加到显示区域
        new_text = text + " →"
        self.removed_display_text.insert(tk.END, new_text)  # 在文本末尾插入文本
        self.removed_display_text.see(tk.END)  # 滚动到最后一行

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

        # 将折线图嵌入到 Tkinter 界面中
        self.canvas = FigureCanvasTkAgg(self.fig, master=_operation)
        self.canvas.get_tk_widget().pack(side='top', padx=10, pady=10)  # 将图表放在右上角

        # 在图下方创建显示删除节点或边的Label
        self.removed_display_text = Text(_operation, height=5, width=50, wrap=tk.WORD)
        self.removed_display_text.pack(side='top', pady=10)
        self.removed_display_text.insert(tk.END, "Removed Nodes/Edges: ")

        show_frame = Frame(_operation, height= 500)
        show_frame.pack()


        attack_frame = Frame(_operation)
        attack_frame.pack(expand=True)


        # 创建行标题的 Treeview
        row_headers = ttk.Treeview(show_frame, show="headings",height=6)
        row_headers["columns"] = ("Row")
        row_headers.heading("Row", text="属性")
        row_headers.column("Row", width=150, anchor="center")

        # 添加行标题数据
        row_headers.insert("", "end", values=("Node Num",))
        row_headers.insert("", "end", values=("Edge Num",))
        row_headers.insert("", "end", values=("Diameter",))
        row_headers.insert("", "end", values=("Clustering Coefficient",))
        row_headers.insert("", "end", values=("Average Path Length",))
        row_headers.insert("", "end", values=("Connected Components",))

        # 放置行标题的 Treeview
        row_headers.grid(row=0, column=0, sticky="nsew")

        # 创建主表格
        tree = ttk.Treeview(show_frame, columns=("before", "after"), show='headings',height=6)
        self.tree = tree
        # 设置每列的标题
        tree.heading("before", text="攻击前")
        tree.heading("after", text="攻击后")

        # 设置每列的宽度
        tree.column("before", width=50)
        tree.column("after", width=50)

        # 插入一些初始数据
        tree.insert("", "end", values=(len(self._g.nodes),len(self._g.nodes)))
        tree.insert("", "end", values=(len(self._g.edges),len(self._g.edges)))
        tree.insert("", "end", values=(self.g_diameter,self.g_diameter))
        tree.insert("", "end", values=(self.average_clustering, self.average_clustering))
        tree.insert("", "end", values=(self.average_shortest_path_length, self.average_shortest_path_length))
        tree.insert("", "end", values=(self.connected_components, self.connected_components))

        # 放置主表格
        tree.grid(row=0, column=1, sticky="nsew")

        self.set_attack_frame(attack_frame)

        
        mainloop()
    
    def set_attack_frame(self, attack_frame):
        tk.Label(attack_frame, text="攻击边:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=(10,0), sticky="w", columnspan=2)
        tk.Label(attack_frame, text="攻击次数:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        tk.Entry(attack_frame, width=10, textvariable=self.attack_edge_num).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.attack_edge_button = tk.Button(attack_frame, text="开始攻击", command=self.attack_edge)
        self.attack_edge_button.grid(row=2, column=0, padx=(20,10), columnspan=2)

        tk.Label(attack_frame, text="攻击点:", font=("黑体",14)).grid(row=3, column=0, padx=10, pady=(10,0), sticky="w", columnspan=2)
        tk.Label(attack_frame, text="攻击次数:").grid(row=4, column=0, padx=15, pady=5, sticky="w")
        tk.Entry(attack_frame, width=10, textvariable=self.attack_node_num).grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.attack_node_button = tk.Button(attack_frame, text="开始攻击", command=self.attack_node)
        self.attack_node_button.grid(row=5, column=0, padx=(20,10), columnspan=2)

        tk.Button(attack_frame, text="重置", command=self.reset, width=20).grid(row=6, column=0, pady=25, padx=10, columnspan=2)


        
    def reset(self):
        self.stop_attack = True  # 停止攻击
        print("Resetting and stopping current attack.")

        self.attack_count = 0  # 攻击次数
        self.max_subgraph_sizes = []  # 存储每次攻击后的最大子图节点数
        # 初始化折线图 Figure
        self.ax.set_xlabel("Attack Count")
        self.ax.set_ylabel("Max Subgraph Size")
        self.line.set_data([],[]) # 初始化折线图的线
        self.ax.set_xlim(0, 100)  # 攻击次数的范围，可以动态调整
        self.ax.set_ylim(0, len(self.G.nodes))  # 节点数范围是图的总节点数
        self.fig.tight_layout()
        self.canvas.draw()  # 刷新图表
        self.parent_container.update()  # 刷新界面，动态显示

        self.removed_display_text.delete("1.0", tk.END)  # 清除之前的文本内容
        self.removed_display_text.insert(tk.END, "Removed Nodes/Edges: ")  # 设置初始文本

        self._g = copy.deepcopy(self.G)

        self.g_diameter = round(nx.diameter(self.G),4)
        self.average_clustering = round(nx.average_clustering(self.G),4)
        self.average_shortest_path_length = round(nx.average_shortest_path_length(self.G),4)
        self.connected_components = round(nx.number_connected_components(self.G),4)

        _image = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}.png').resize((600,450)))     # .resize((800,400))
        self.image_label_after.configure(image = _image)
        self.image_label_after.image = _image      # 这步很重要，防止图片被垃圾回收

        self.modify_data_in_table(0,1, len(self.G.nodes))
        self.modify_data_in_table(1,1, len(self.G.edges))
        self.modify_data_in_table(2,1, self.g_diameter)
        self.modify_data_in_table(3,1, self.average_clustering)
        self.modify_data_in_table(4,1, self.average_shortest_path_length)
        self.modify_data_in_table(5,1, self.connected_components)


    def highlight_deleted_node(self, attacked_node):
        """
        高亮被删除的节点，在图上用不同颜色展示
        """
        # 获取当前图的节点信息
        node_colors = ['#1f78b4' if node != attacked_node else 'red' for node in self._g.nodes]
        node_sizes = [4 if node != attacked_node else 3000 for node in self._g.nodes]

        # 重新绘制图，使用不同颜色高亮显示删除的节点
        draw_graph(self._g, f'./data/network-{self.graph_seed}-after.png', False, self.pos, node_color=node_colors, node_size=node_sizes)

        # 更新界面图片
        _image = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}-after.png').resize((600,450)))
        self.image_label_after.configure(image=_image)
        self.image_label_after.image = _image
        # self.parent_container.update()  # 刷新界面，动态显示

    def highlight_deleted_edge(self, attacked_edge):
        """
        高亮被删除的边，在图上用不同颜色展示
        """
        edge_colors = ['k' if edge != attacked_edge else 'red' for edge in self._g.edges]
        edge_sizes = [1 if edge != attacked_edge else 3 for edge in self._g.edges]

        draw_graph(self._g, f'./data/network-{self.graph_seed}-after.png', False, self.pos, edge_color=edge_colors, edge_size=edge_sizes)
        _image = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}-after.png').resize((600,450)))
        self.image_label_after.configure(image=_image)
        self.image_label_after.image = _image
        # self.parent_container.update()  # 刷新界面，动态显示



    def attack_edge(self):
        # self._g, attacked_edge, attacked_betweenness = random_attack_edge_betweenness(self._g)
        # print('attack_edge', self._g, attacked_edge, attacked_betweenness)
        # self.disable_attack_button(0)
        # self._g, _, _ = random_attack_edge_betweenness(self._g)
        self.stop_attack = False

        attack_num = self.attack_edge_num.get()

        for i in range(attack_num):
            if self.stop_attack:  # 如果标志为True，停止攻击
                print("Edge attack stopped.")
                break
            self._g, attacked_edge, _ = random_attack_edge_betweenness(self._g)
            self.removed_elements.append(attacked_edge)
            self.update_removed_display(attacked_edge)  # 更新显示删除的节点
            self.highlight_deleted_edge(attacked_edge)  # 高亮被删除的边
            self.update_max_subgraph_label()  # 更新最大子图节点数
            self.update_line_chart()  # 更新折线图
            self.attack_method()
            self.parent_container.update()  # 刷新界面，动态显示
        # for i in range(100):
        #     self._g, _, _ = random_attack_edge_betweenness(self._g)
        # self.attack_method()
        # self.enable_attack_button()

    def attack_node(self):
        # self._g, attacked_node, attacked_betweenness = random_attack_node_betweenness(self._g)
        # print('attack_node: ',self._g, attacked_node, attacked_betweenness)
        # self.disable_attack_button(1)
        self.stop_attack = False
        attack_num = self.attack_node_num.get()
        for i in range(attack_num):
            if self.stop_attack:  # 如果标志为True，停止攻击
                print("Node attack stopped.")
                break
            self._g, attacked_node, _ = random_attack_node_betweenness(self._g)
            self.removed_elements.append(attacked_node)
            self.update_removed_display(attacked_node)  # 更新显示删除的节点
            self.highlight_deleted_node(attacked_node)  # 高亮被删除的节点
            self.update_max_subgraph_label()  # 更新最大子图节点数
            self.update_line_chart()  # 更新折线图
            self.attack_method()
            self.parent_container.update()  # 刷新界面，动态显示
        # self._g, _, _ = random_attack_node_betweenness(self._g)
        # for i in range(100):
        #     self._g, _, _ = random_attack_node_betweenness(self._g)
        # self.attack_method()
        # self.enable_attack_button()

        

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
            self.modify_data_in_table(2,1, nx.diameter(h))
            self.modify_data_in_table(4,1, nx.average_shortest_path_length(h))
        else:
            self.modify_data_in_table(2,1, nx.diameter(self._g))
            self.modify_data_in_table(4,1, nx.average_shortest_path_length(self._g))
        self.modify_data_in_table(0,1, len(self._g.nodes))
        self.modify_data_in_table(1,1, len(self._g.edges))
        self.modify_data_in_table(3,1, nx.average_clustering(self._g))
        self.modify_data_in_table(5,1, num)

        _image = ImageTk.PhotoImage(Image.open(f'./data/network-{self.graph_seed}-after.png').resize((600,450)))     # .resize((800,400))
        self.image_label_after.configure(image = _image)
        self.image_label_after.image = _image      # 这步很重要，防止图片被垃圾回收
    
    def disable_attack_button(self, type=0):
        '''
            type 0: edge
            type 1: node
        '''
        self.attack_edge_button_text = self.attack_edge_button.cget('text')
        self.attack_node_button_text = self.attack_node_button.cget('text')
        if type == 0:
            text = "正在攻击边..."
        if type == 1:
            text = "正在攻击点..."

        self.attack_edge_button.configure(text=text, state=tk.DISABLED)
        self.attack_edge_button.text = text
        self.attack_edge_button.state = tk.DISABLED 
        self.attack_node_button.configure(text=text, state=tk.DISABLED)
        self.attack_node_button.text = text
        self.attack_node_button.state = tk.DISABLED 
    
    def enable_attack_button(self):
        '''
            type 0: edge
            type 1: node
        '''
        self.attack_edge_button.configure(text=self.attack_edge_button_text, state=tk.NORMAL)
        self.attack_edge_button.text = self.attack_edge_button_text
        self.attack_edge_button.state = tk.NORMAL 
        self.attack_node_button.configure(text=self.attack_node_button_text, state=tk.NORMAL)
        self.attack_node_button.text = self.attack_node_button_text
        self.attack_node_button.state = tk.NORMAL 


class Intentional_Attack(Attack_base):
    def __init__(self, parent_container, graph_seed, G):
        super().__init__(parent_container, graph_seed, G)
        self.attack_node_metric = tk.StringVar()
        self.attack_edge_metric = tk.StringVar()

    def set_attack_frame(self, attack_frame):
        tk.Label(attack_frame, text="攻击边:", font=("黑体",14)).grid(row=0, column=0, padx=10, pady=(15,0), sticky="w", columnspan=2)
        tk.Label(attack_frame, text="选择指标:", ).grid(row=1, column=0, padx=15, pady=5, sticky="w")
        attack_metric_edge_spinbox = ttk.Combobox(attack_frame, textvariable=self.attack_edge_metric, width=10)
        attack_metric_edge_spinbox['values'] = ['max_betweenness']
        # attack_metric_edge_spinbox.current(0)
        attack_metric_edge_spinbox.grid(row=1, column=1,padx=10)

        tk.Label(attack_frame, text="攻击次数:").grid(row=2, column=0, padx=15, pady=5, sticky="w")
        tk.Entry(attack_frame, width=10, textvariable=self.attack_edge_num).grid(row=2, column=1, padx=15, pady=5, sticky="w")

        self.attack_edge_button = tk.Button(attack_frame, text="开始攻击", command=self.attack_edge)
        self.attack_edge_button.grid(row=3, column=0, padx=(20,10),pady=10, columnspan=2)

        tk.Label(attack_frame, text="攻击点:", font=("黑体",14)).grid(row=4, column=0, padx=10, pady=(15,0), sticky="w", columnspan=2)
        tk.Label(attack_frame, text="选择指标:", ).grid(row=5, column=0, padx=15, pady=5, sticky="w")
        attack_metric_node_spinbox = ttk.Combobox(attack_frame, textvariable=self.attack_node_metric, width=10)
        attack_metric_node_spinbox['values'] = ['max_degree', 'max_betweenness', 'max_coreness', 'max_closeness']
        # attack_metric_node_spinbox.current(0)
        attack_metric_node_spinbox.grid(row=5, column=1,padx=10)

        tk.Label(attack_frame, text="攻击次数:").grid(row=6, column=0, padx=15, pady=5, sticky="w")
        tk.Entry(attack_frame, width=10, textvariable=self.attack_node_num).grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.attack_edge_button = tk.Button(attack_frame, text="开始攻击", command=self.attack_node)
        self.attack_edge_button.grid(row=7, column=0, padx=(20,10),pady=10, columnspan=2)

        tk.Button(attack_frame, text="重置", command=self.reset, width=20).grid(row=8, column=0, pady=25, padx=10, columnspan=2)


    def attack_edge(self):
        # max_betweenness, max_edge = get_max_betweenness_edge(self._g)
        # self._g = nx.Graph(self._g)
        # self._g.remove_edge(*max_edge)
        # print('attack_edge: ', self._g, max_edge, max_betweenness)
        # self.disable_attack_button(0)
        attack_num = self.attack_edge_num.get()
        attack_metric = self.attack_edge_metric.get()
        self.stop_attack = False
        for i in range(attack_num):
            if self.stop_attack:  # 如果标志为True，停止攻击
                print("Node attack stopped.")
                break
            self._g, attacked_edge, _ = edge_function_map[attack_metric](self._g)
            self.removed_elements.append(attacked_edge)
            self.update_removed_display(attacked_edge)  # 更新显示删除的节点
            self.highlight_deleted_node(attacked_edge)  # 高亮被删除的节点
            self.update_max_subgraph_label()  # 更新最大子图节点数
            self.update_line_chart()  # 更新折线图
            self.attack_method()
            self.parent_container.update()  # 刷新界面，动态显示
        # self.enable_attack_button()

    def attack_node(self):
        # self.disable_attack_button(1)
        # self._g = intentional_attack_node_betweenness(self._g)
        attack_num = self.attack_node_num.get()
        attack_metric = self.attack_node_metric.get()
        self.stop_attack = False
        for i in range(attack_num):
            if self.stop_attack:  # 如果标志为True，停止攻击
                print("Node attack stopped.")
                break
            self._g, attacked_node, _ = node_function_map[attack_metric](self._g)
            self.removed_elements.append(attacked_node)
            self.update_removed_display(attacked_node)  # 更新显示删除的节点
            self.highlight_deleted_node(attacked_node)  # 高亮被删除的节点
            self.update_max_subgraph_label()  # 更新最大子图节点数
            self.update_line_chart()  # 更新折线图
            self.attack_method()
            self.parent_container.update()  # 刷新界面，动态显示
        # self.enable_attack_button()

