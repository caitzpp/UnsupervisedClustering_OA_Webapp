from dash import Dash, html, dash_table, dcc, callback, Output, Input
# import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import config
import numpy as np
import sys

from src.load_data import HDBSCAN_DataLoader
from traces.base import BaseTrace, BaseLegend

PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH
IMG_PATH = config.IMG_PATH

example_image="IM0001_1_left.png"
example_image_path = os.path.join('assets', example_image)

#TODO: import this with args or env
folder = "2025-10-19_hdbscan"
run = "run27"

data_loader = HDBSCAN_DataLoader(PROCESSED_DATA_PATH, folder, run)
df, model_info, embeddings, ids = data_loader.load_pipeline_data()
mapping = data_loader.get_mapping()

klvalues = list(set(df['KL-Score'].values))

mappings_kl, embeddings_kl_d = data_loader.load_data_by_kl()
mappings_noise, embeddings_noise = data_loader.load_data_by_filter('cluster_label', -1)

pal = px.colors.qualitative.Safe

app = Dash(__name__)

fig = go.Figure()
traces = []
base = BaseTrace(embeddings, mapping)
fig.add_trace(base.create_trace())

legend_kl = BaseLegend(title='KL-Score', y=0.5)
fig.update_layout(legend=legend_kl.create_legend())

kl_color = {kl: pal[i] for i, kl in enumerate(klvalues)}
for kl in klvalues:
    embeddings_kl = embeddings_kl_d[str(int(kl))]
    mappings_kl_temp = mappings_kl[str(int(kl))]
    new_trace = BaseTrace(embeddings_kl, mappings_kl_temp, color=kl_color[kl], showlegend=True
                          , legend="legend", name =f"{kl}")
    trace_new = new_trace.create_trace()
    trace_new.legendgroup = f"kl_{kl}"
    fig.add_trace(trace_new)
fig.update_layout(
    legend_groupclick = "toggleitem",
    legend_itemclick = "toggleothers",
    scene = dict(
        xaxis_title='UMAP 1',
        yaxis_title='UMAP 2',
        zaxis_title='UMAP 3'
    )
    , scene_dragmode = 'turntable'
)

fig2 = go.Figure()
legend_noise = BaseLegend(title='Noise Points', y=0.9)
fig2.update_layout(legend2=legend_noise.create_legend())
fig2.add_trace(base.create_trace())
noise_trace = BaseTrace(embeddings_noise, mappings_noise, color='black', showlegend=True, legend="legend2",
                        name = 'Noise Points')
trace_noise = noise_trace.create_trace()
trace_noise.legendgroup = "noise"
# trace_noise.visible = 'legendonly'
fig2.add_trace(trace_noise)
fig2.update_layout(scene = dict(
        xaxis_title='UMAP 1',
        yaxis_title='UMAP 2',
        zaxis_title='UMAP 3'
    )
    , scene_dragmode = 'turntable'
)

app.layout = [
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.RadioItems(options = ['KL-Scores',  'Noise Points'],
         value='KL-Scores', id='scatter_radioitem'),
    html.Img(src=example_image_path, style={"width": "200px"}),
    #dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='scatter'),
]

@callback(
    Output('scatter', 'figure'),
    Input('scatter_radioitem', 'value')
)
# @callback(Output('other-graph', 'figure), Input('scatter', 'clickData'))
# def update_other_graph(clickData):
#     if not clickData:
#         return dash.no_update
    
#     # Get ID from the clicked point
#     selected_id = clickData['points'][0]['customdata'][0]

#     # Filter data for that ID
#     df_selected = df[df['id'] == selected_id]
    
#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=df_selected['feature'], y=df_selected['value']))
#     return fig
def update_scatter(selected_radio):
    if selected_radio == 'KL-Scores':
        return fig
    else:
        return fig2

if __name__ == '__main__':
    app.run(debug=True)


