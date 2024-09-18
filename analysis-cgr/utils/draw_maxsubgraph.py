from pyecharts import options as opts
from pyecharts.charts import Line
import random
# 读取数据文件

base_dir = "221_network"

# filenames = ['betweeness', 'closs', 'eigenvector', 'maxcore', 'maxdegree', 'random']

nodes = []
degree_maxsubgraph = []
core_maxsubgraph = []
random_maxsubgraph = []
betweeness_maxsubgraph = []
clossness_maxsubgraph = []
eigenvector_maxsubgraph = []

with open(f'{base_dir}/betweeness_maxsubgraph.txt', "r") as file:
    index = 1
    for line in file:
        maxsubgraph = line.strip()
        nodes.append(index)
        index += 1
        betweeness_maxsubgraph.append(float(maxsubgraph))

with open(f'{base_dir}/closs_maxsubgraph.txt', "r") as file:
    for line in file:
        maxsubgraph = line.strip()
        clossness_maxsubgraph.append(float(maxsubgraph))

with open(f'{base_dir}/eigenvector_maxsubgraph.txt', "r") as file:
    for line in file:
        maxsubgraph = line.strip()
        eigenvector_maxsubgraph.append(float(maxsubgraph))

with open(f'{base_dir}/maxdegree_maxsubgraph.txt', "r") as file:
    for line in file:
        maxsubgraph = line.strip()
        degree_maxsubgraph.append(float(maxsubgraph))

with open(f'{base_dir}/maxcore_maxsubgraph.txt', "r") as file:
    for line in file:
        maxsubgraph = line.strip()
        core_maxsubgraph.append(float(maxsubgraph))

with open(f'{base_dir}/random_maxsubgraph.txt', "r") as file:
    for line in file:
        maxsubgraph = line.strip()
        random_maxsubgraph.append(float(maxsubgraph))

# 创建曲线图
line = (
    Line()
    .add_xaxis(nodes)
    .add_yaxis("max degree node attack", degree_maxsubgraph, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("max core node attack", core_maxsubgraph, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("random attack", random_maxsubgraph, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("betweenness attack", betweeness_maxsubgraph, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("clossness attack", clossness_maxsubgraph, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("eigenvector attack", eigenvector_maxsubgraph, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="intentional attack max subgraph curve plot"),
        xaxis_opts=opts.AxisOpts(name="iteration"),
        yaxis_opts=opts.AxisOpts(name="max subgraph"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="right", orient="vertical"),
    )
)

# 保存图表到文件或在Jupyter Notebook中显示
line.render(f'{base_dir}/maxsubgraph_curve.html')  # 保存为HTML文件
# 或者在Jupyter Notebook中显示
# line.render_notebook()
