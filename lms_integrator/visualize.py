import plotly.graph_objects as go

def plot_misses(ns, misses):
    fig = go.Figure(data=go.Bar(x=ns, y=misses))
    fig.update_layout(title='Cache Misses by Matrix Size', xaxis_title='N', yaxis_title='Misses')
    return fig
