import tkinter as tk
from tkinter import Canvas, Frame, Label
import networkx as nx
import random
from utils import build_graph


class GraphVisualizer:
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

        # Initialize bounds
        self.update_bounds()

        self.create_window()
        self.update_statistics()

    def create_window(self):
        self.root.title("动态攻击图")
        self.root.geometry("800x600")

        main_frame = Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        self.canvas_frame = Frame(main_frame)
        self.canvas_frame.pack(side='left', fill='both', expand=True)

        self.operation_frame = Frame(main_frame, width=200)
        self.operation_frame.pack(side='right', fill='y')

        self.info_frame = Frame(self.operation_frame)
        self.info_frame.pack(pady=20)

        self.canvas = Canvas(self.canvas_frame, bg='white')
        self.canvas.pack(fill='both', expand=True)

        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<Configure>", self.on_resize)

        self.set_control_buttons(self.operation_frame)

        self.draw_graph()

    def set_control_buttons(self, attack_frame):
        tk.Label(attack_frame, text="动态攻击:", font=("黑体", 14)).pack(pady=20)
        tk.Button(attack_frame, text="动态边攻击", command=self.start_edge_attack).pack(pady=10)
        tk.Button(attack_frame, text="动态节点攻击", command=self.start_node_attack).pack(pady=10)
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

    def highlight_edge(self, u, v, times=5):
        x1, y1 = self.transform_coordinates(*self.pos[u])
        x2, y2 = self.transform_coordinates(*self.pos[v])
        edge = self.canvas.create_line(x1, y1, x2, y2, fill="yellow", width=3)

        for i in range(times):
            self.root.after(300 * i, lambda i=i: self.canvas.itemconfig(edge, fill="black" if i % 2 == 0 else "yellow"))

    def highlight_node(self, node, times=5):
        x, y = self.transform_coordinates(*self.pos[node])
        node_circle = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="yellow", outline="yellow")

        for i in range(times):
            self.root.after(300 * i, lambda i=i: self.canvas.itemconfig(node_circle, fill="red" if i % 2 == 0 else "yellow"))

    def transform_coordinates(self, x, y):
        width = self.canvas.winfo_width() - 20
        height = self.canvas.winfo_height() - 20
        x_transformed = (x * self.scale + self.offset_x) * width / (self.x_max - self.x_min) + 10
        y_transformed = (y * self.scale + self.offset_y) * height / (self.y_max - self.y_min) + 10
        return x_transformed, y_transformed

    def update_bounds(self):
        x_values = [pos[0] for pos in self.pos.values()]
        y_values = [pos[1] for pos in self.pos.values()]
        self.x_min, self.x_max = min(x_values), max(x_values)
        self.y_min, self.y_max = min(y_values), max(y_values)

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
            dx = (event.x - self.last_x) / self.canvas.winfo_width() * (self.x_max - self.x_min)
            dy = (event.y - self.last_y) / self.canvas.winfo_height() * (self.y_max - self.y_min)
            self.offset_x += dx
            self.offset_y += dy
            self.last_x, self.last_y = event.x, event.y
            self.draw_graph()

    def on_resize(self, event):
        self.draw_graph()

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

    def reset_graph(self):
        self.G = self.G_original.copy()
        self.pos = nx.spring_layout(self.G, seed=self.graph_seed)
        self.update_bounds()
        self.draw_graph()
        self.update_statistics()

    def stop_attacks(self):
        if hasattr(self, 'attacker'):
            self.attacker.stop()

    def start_edge_attack(self):
        self.attacker = EdgeAttacker(self)
        self.attacker.start()

    def start_node_attack(self):
        self.attacker = NodeAttacker(self)
        self.attacker.start()

    def update_canvas(self):
        self.draw_graph()


class EdgeAttacker:
    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.attacking = False
        self.stop_attack = False

    def start(self):
        if self.attacking:
            return
        self.attacking = True
        self.stop_attack = False
        self._dynamic_edge_attack_step()

    def _dynamic_edge_attack_step(self):
        if len(self.visualizer.G.edges()) > 0 and not self.stop_attack:
            u, v = random.choice(list(self.visualizer.G.edges()))
            self.visualizer.highlight_edge(u, v, times=5)
            self.visualizer.root.after(300 * 5, lambda: self.remove_edge(u, v))
        else:
            self.attacking = False

    def remove_edge(self, u, v):
        self.visualizer.G.remove_edge(u, v)
        print(f"移除边: {(u, v)}")
        self.visualizer.update_canvas()
        self.visualizer.root.after(500, self._dynamic_edge_attack_step)

    def stop(self):
        self.stop_attack = True
        self.attacking = False


class NodeAttacker:
    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.attacking = False
        self.stop_attack = False

    def start(self):
        if self.attacking:
            return
        self.attacking = True
        self.stop_attack = False
        self._dynamic_node_attack_step()

    def _dynamic_node_attack_step(self):
        if len(self.visualizer.G.nodes()) > 0 and not self.stop_attack:
            node = random.choice(list(self.visualizer.G.nodes()))
            self.visualizer.highlight_node(node, times=5)
            self.visualizer.root.after(300 * 5, lambda: self.remove_node(node))
        else:
            self.attacking = False

    def remove_node(self, node):
        self.visualizer.G.remove_node(node)
        print(f"移除节点: {node}")
        self.visualizer.update_canvas()
        self.visualizer.root.after(500, self._dynamic_node_attack_step)

    def stop(self):
        self.stop_attack = True
        self.attacking = False


if __name__ == '__main__':
    root = tk.Tk()
    G, nodes = build_graph('./data/git_web_ml/musae_git_edges.csv')
    G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    G = nx.Graph(G)

    app = GraphVisualizer(root, graph_seed=42, G_original=G)
    root.mainloop()
