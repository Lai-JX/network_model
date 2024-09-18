from pyecharts import options as opts
from pyecharts.charts import Line
import random
# 读取数据文件

base_dir = "221_network"

# filenames = ['betweeness', 'closs', 'eigenvector', 'maxcore', 'maxdegree', 'random']

nodes = []
degree_avepaths = []
core_avepaths = []
random_avepaths = []
betweeness_avepaths = []
clossness_avepaths = []
eigenvector_avepaths = []

with open(f'{base_dir}/betweeness_avepath.txt', "r") as file:
    index = 1
    for line in file:
        avepath = line.strip()
        nodes.append(index)
        index += 1
        betweeness_avepaths.append(float(avepath))

with open(f'{base_dir}/closs_avepath.txt', "r") as file:
    for line in file:
        avepath = line.strip()
        clossness_avepaths.append(float(avepath))

with open(f'{base_dir}/eigenvector_avepath.txt', "r") as file:
    for line in file:
        avepath = line.strip()
        eigenvector_avepaths.append(float(avepath))

with open(f'{base_dir}/maxdegree_avepath.txt', "r") as file:
    for line in file:
        avepath = line.strip()
        degree_avepaths.append(float(avepath))

with open(f'{base_dir}/maxcore_avepath.txt', "r") as file:
    for line in file:
        avepath = line.strip()
        core_avepaths.append(float(avepath))

with open(f'{base_dir}/random_avepath.txt', "r") as file:
    for line in file:
        avepath = line.strip()
        random_avepaths.append(float(avepath))

# 创建曲线图
line = (
    Line()
    .add_xaxis(nodes)
    .add_yaxis("max degree node attack", degree_avepaths, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("max core node attack", core_avepaths, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("random attack", random_avepaths, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("betweenness attack", betweeness_avepaths, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("clossness attack", clossness_avepaths, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .add_yaxis("eigenvector attack", eigenvector_avepaths, label_opts=opts.LabelOpts(is_show=False), linestyle_opts=opts.LineStyleOpts(width=2))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="intentional attack average path curve plot"),
        xaxis_opts=opts.AxisOpts(name="iteration"),
        yaxis_opts=opts.AxisOpts(name="average path"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="right", orient="vertical"),
    )
)

# 保存图表到文件或在Jupyter Notebook中显示
line.render(f'{base_dir}/avepath_curve.html')  # 保存为HTML文件
# 或者在Jupyter Notebook中显示
# line.render_notebook()
