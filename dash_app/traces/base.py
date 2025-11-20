import plotly.graph_objects as go

class BaseTrace:
    def __init__(self, embeddings, mapping, color='lightgray', size=5, showlegend=False, legend=None, name = None):
        self.embeddings = embeddings
        self.mapping = mapping
        self.color = color
        self.size = size
        self.showlegend = showlegend
        self.legend = legend
        self.name = name

    def create_trace(self, trace_columns = ['cluster_label', 'KL-Score'], hovertemplate_mappinges = {'Cluster Label':1, 'KL-Score':2}):
        trace = go.Scatter3d(
            x=self.embeddings[:, 0],
            y=self.embeddings[:, 1],
            z=self.embeddings[:, 2],
            mode='markers',
            marker=dict(
                size=self.size,
                color=self.color,
                
                # color=df['hdbscan_labels'],  
                # colorscale='Viridis',  
                # opacity=0.8
            ),
            showlegend=self.showlegend,
            name=self.name,
            legend=self.legend,
            customdata=[
                 [id_] + [v[col] for col in trace_columns]
                    for id_, v in self.mapping.items()
            ],
            hovertemplate=('<br>'.join([f"{k}=%{{customdata[{v}]}}" for k, v in hovertemplate_mappinges.items()]) + '<extra></extra>')
        )
        return trace
    

class BaseLegend:
    def __init__(self, title="Legend", y=0.65):
        self.title = title
        self.y = y

    def create_legend(self):
        legend = dict(
            title= dict(text=self.title),
            xref="container",
            yref="container",
            yanchor="top",
            xanchor="right",
            y=self.y,
            x=0.9,
            orientation="h",
        )
        return legend