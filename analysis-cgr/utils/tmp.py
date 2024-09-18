import networkx as nx
import plotly.graph_objects as go

# 创建一个简单的网络图
G = nx.Graph()
with open('/Users/azurestar/Desktop/tmp/processed_email-Eu-core_del_800.txt', 'r') as file:
    for line in file:
        from_node, to_node = map(int, line.strip().split())
        if from_node == to_node:
            continue
        G.add_edge(from_node, to_node)
        # G1.add_edge(from_node, to_node)

# 创建Plotly图表
pos = nx.spring_layout(G)  # 定义节点的位置
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
    )
)

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
    )
)

fig.show()