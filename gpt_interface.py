import tkinter as tk
from tkinter import Canvas, Frame, Label
import networkx as nx
import random
from main import build_graph


class Dynamic_Attack:
    def __init__(self, root, graph_seed, G_original):
        self.root = root
        self.graph_seed = graph_seed
        self.G_original = G_original
        self.G = G_original.copy()
        self.pos = nx.spring_layout(self.G, seed=self.graph_seed)
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.stop_attack = False
        self.attacking = False

        # 获取节点的最小和最大坐标
        self.x_values = [pos[0] for pos in self.pos.values()]
        self.y_values = [pos[1] for pos in self.pos.values()]
        self.x_min, self.x_max = min(self.x_values), max(self.x_values)
        self.y_min, self.y_max = min(self.y_values), max(self.y_values)

        self.canvas_size = 800
        self.padding = 50

        self.offset_x = -(self.x_max + self.x_min) / 2
        self.offset_y = -(self.y_max + self.y_min) / 2

        self.create_window()
        self.update_statistics()

    def create_window(self):
        self.root.title("动态攻击图")

        # 创建展示图的区域
        self.canvas_frame = Frame(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas_frame.pack(side='left')

        # 操作按钮区域
        self.operation_frame = Frame(self.root, width=200, height=self.canvas_size)
        self.operation_frame.pack(side='right')

        # 信息展示区域
        self.info_frame = Frame(self.operation_frame)
        self.info_frame.pack(pady=20)

        # 初始化画布
        self.canvas = Canvas(self.canvas_frame, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack()

        # 绑定缩放和平移事件
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # 设置攻击按钮
        self.set_control_buttons(self.operation_frame)

        # 初始化绘制图形
        self.draw_graph()

    def set_control_buttons(self, attack_frame):
        tk.Label(attack_frame, text="动态攻击:", font=("黑体", 14)).pack(pady=20)
        tk.Button(attack_frame, text="动态边攻击", command=self.dynamic_edge_attack).pack(pady=10)
        tk.Button(attack_frame, text="动态节点攻击", command=self.dynamic_node_attack).pack(pady=10)
        self.stop_button = tk.Button(attack_frame, text="停止", command=self.stop_attacks)
        self.stop_button.pack(pady=10)
        tk.Button(attack_frame, text="重置", command=self.reset_graph).pack(pady=10)

    def draw_graph(self):
        self.canvas.delete("all")

        for u, v in self.G.edges():
            x1, y1 = self.transform_coordinates(*self.pos[u])
            x2, y2 = self.transform_coordinates(*self.pos[v])
            self.canvas.create_line(x1, y1, x2, y2, fill="black")

        for node in self.G.nodes():
            x, y = self.transform_coordinates(*self.pos[node])
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")

    def transform_coordinates(self, x, y):
        x_transformed = (x * self.scale + self.offset_x) * self.canvas_size / (self.x_max - self.x_min) + self.padding
        y_transformed = (y * self.scale + self.offset_y) * self.canvas_size / (self.y_max - self.y_min) + self.padding
        return x_transformed, y_transformed

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.scale *= 1.1
        elif event.delta < 0:
            self.scale /= 1.1
        self.draw_graph()

    def on_press(self, event):
        self.dragging = True
        self.last_x, self.last_y = event.x, event.y

    def on_drag(self, event):
        if self.dragging:
            dx = (event.x - self.last_x) / self.canvas_size * (self.x_max - self.x_min)
            dy = (event.y - self.last_y) / self.canvas_size * (self.y_max - self.y_min)
            self.offset_x += dx
            self.offset_y += dy
            self.last_x, self.last_y = event.x, event.y
            self.draw_graph()

    def update_canvas(self):
        self.draw_graph()
        self.update_statistics()
        self.root.update_idletasks()

    def update_statistics(self):
        num_nodes = len(self.G.nodes())
        num_edges = len(self.G.edges())
        avg_degree = sum(dict(self.G.degree()).values()) / num_nodes if num_nodes > 0 else 0
        avg_cluster_coeff = nx.average_clustering(self.G)
        avg_coreness = sum(nx.core_number(self.G).values()) / num_nodes if num_nodes > 0 else 0
        avg_betweenness = sum(nx.betweenness_centrality(self.G).values()) / num_nodes if num_nodes > 0 else 0

        for widget in self.info_frame.winfo_children():
            widget.destroy()

        Label(self.info_frame, text=f"节点数: {num_nodes}").pack()
        Label(self.info_frame, text=f"边数: {num_edges}").pack()
        Label(self.info_frame, text=f"平均度数: {avg_degree:.2f}").pack()
        Label(self.info_frame, text=f"平均聚类系数: {avg_cluster_coeff:.2f}").pack()
        Label(self.info_frame, text=f"平均中心性: {avg_coreness:.2f}").pack()
        Label(self.info_frame, text=f"平均介数: {avg_betweenness:.2f}").pack()

    def dynamic_edge_attack(self):
        if self.attacking:
            return
        self.attacking = True
        self.stop_attack = False
        self._dynamic_edge_attack_step()

    def _dynamic_edge_attack_step(self):
        if len(self.G.edges()) > 0 and not self.stop_attack:
            u, v = random.choice(list(self.G.edges()))
            self.G.remove_edge(u, v)
            print(f"移除边: {(u, v)}")
            self.update_canvas()
            self.root.after(500, self._dynamic_edge_attack_step)
        else:
            self.attacking = False

    def dynamic_node_attack(self):
        if self.attacking:
            return
        self.attacking = True
        self.stop_attack = False
        self._dynamic_node_attack_step()

    def _dynamic_node_attack_step(self):
        if len(self.G.nodes()) > 0 and not self.stop_attack:
            node = random.choice(list(self.G.nodes()))
            self.G.remove_node(node)
            print(f"移除节点: {node}")
            self.update_canvas()
            self.root.after(500, self._dynamic_node_attack_step)
        else:
            self.attacking = False

    def stop_attacks(self):
        self.stop_attack = True
        self.attacking = False

    def reset_graph(self):
        self.stop_attacks()
        self.G = self.G_original.copy()
        self.pos = nx.spring_layout(self.G, seed=self.graph_seed)
        self.x_values = [pos[0] for pos in self.pos.values()]
        self.y_values = [pos[1] for pos in self.pos.values()]
        self.x_min, self.x_max = min(self.x_values), max(self.x_values)
        self.y_min, self.y_max = min(self.y_values), max(self.y_values)
        self.draw_graph()
        self.update_statistics()


# 主程序入口
if __name__ == '__main__':
    root = tk.Tk()

    G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
    G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    G = nx.Graph(G)

    app = Dynamic_Attack(root, graph_seed=42, G_original=G)
    root.mainloop()
