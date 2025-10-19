import plotly.graph_objects as go

class BaseTrace:
    def __init__(self, embeddings, mapping, color='lightgray', size=5, showlegend=False):
        self.embeddings = embeddings
        self.mapping = mapping
        self.color = color
        self.size = size
        self.showlegend = showlegend

    def create_trace(self):
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
            customdata=[
                [v['cluster_label'], v['KL-Score']] for v in self.mapping.values()
            ],
            hovertemplate='Cluster Label=%{customdata[0]}'
        )
        return trace