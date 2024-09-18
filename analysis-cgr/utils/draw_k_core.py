import networkx as nx
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

# 生成暖色系颜色
colors = ['#FF6B61', '#BEB8DC']

# 1. 从txt文件中加载网络
base_dir = "221_network"
nodes = set()
G = nx.Graph()

index = 1
mapping_dict = {}
with open('data/processed_email-Eu-core-750.txt', 'r') as f:
    for line in f:
        from_node, to_node = map(int, line.strip().split())
        nodes.add(from_node)
        nodes.add(to_node)

node_list = sorted(list(nodes))

for i in range(len(node_list)):
    mapping_dict[node_list[i]] = i + 1

with open('data/processed_email-Eu-core-750.txt', 'r') as f:
    for line in f:
        from_node, to_node = map(int, line.strip().split())
        G.add_edge(mapping_dict[from_node],mapping_dict[to_node])

G.remove_edges_from(nx.selfloop_edges(G))

x_axis_k_core = []
y_axis_vertices_num = []

for k in range(len(node_list)):
    tmp = nx.k_core(G, k)
    num_of_node = tmp.number_of_nodes()
    if num_of_node == 0:
        break
    x_axis_k_core.append(k)
    y_axis_vertices_num.append(num_of_node)
    # num_of_edge = tmp.number_of_edges()
    # print(f"{k}-core: {tmp}")
for i in range(len(y_axis_vertices_num)):
    if i + 1 < len(y_axis_vertices_num):
        y_axis_vertices_num[i] = y_axis_vertices_num[i] - y_axis_vertices_num[i + 1]
# # 创建直方图
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
    .add_xaxis(x_axis_k_core[1:])
    .add_yaxis("k-core vertices number", y_axis_vertices_num[1:], label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="k-core-vertices-number diagram"),
        xaxis_opts=opts.AxisOpts(name="k-core"),
        yaxis_opts=opts.AxisOpts(name="number"),
        visualmap_opts=opts.VisualMapOpts(
            max_=max(y_axis_vertices_num[1:]),
            is_piecewise=True,
            # pieces=[
            #     {"min": 0, "max": 30},
            #     {"min": 31, "max": max(degrees)}
            # ],
            orient="vertical",
            pos_top="middle",
            pos_right="10",
            range_color=colors
        ),
    )
)

# 保存图表到文件或在Jupyter Notebook中显示
bar.render(f'{base_dir}/k-core.html')  # 保存为HTML文件