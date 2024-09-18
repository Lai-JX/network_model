from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
import random  # 用于生成暖色系颜色
# 读取数据文件

base_dir = "252_network"

data_file = f'{base_dir}/degree.txt'
degrees = dict()
with open(data_file, "r") as file:
    index = 1
    for line in file:
        node_degree = int(line.strip())
        if node_degree in degrees.keys():
            degrees[node_degree] += 1
        else:
            degrees[node_degree] = 1

degrees = sorted(degrees.items(),key = lambda x:x[0],reverse=False)
print(degrees)
x_axis_degree = []
y_axis_num = []
for degree in degrees:
    x_axis_degree.append(degree[0])
    y_axis_num.append(degree[1])
# 生成暖色系颜色
colors = ['#FF6B61', '#BEB8DC']

# 创建直方图
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
    .add_xaxis(x_axis_degree)
    .add_yaxis("degree distribution", y_axis_num, label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="degree-vertices-number diagram"),
        xaxis_opts=opts.AxisOpts(name="degree"),
        yaxis_opts=opts.AxisOpts(name="number"),
        visualmap_opts=opts.VisualMapOpts(
            max_=max(y_axis_num),
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
bar.render(f'{base_dir}/node_degree_histogram.html')  # 保存为HTML文件
# 或者在Jupyter Notebook中显示
# bar.render_notebook()
