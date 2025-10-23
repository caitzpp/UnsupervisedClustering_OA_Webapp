from dash import Dash, html, dash_table, dcc, callback, Output, Input
# import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import config
import numpy as np
import sys

from src.load_data import HDBSCAN_DataLoader
from traces.base import BaseTrace

PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH

#TODO: import this with args or env
folder = "2025-10-19_hdbscan"
run = "run27"

data_loader = HDBSCAN_DataLoader(PROCESSED_DATA_PATH, folder, run)
df, model_info, embeddings, ids = data_loader.load_pipeline_data()
mapping = data_loader.get_mapping()

klvalues = list(set(df['KL-Score'].values))

mappings_kl, embeddings_kl_d = data_loader.load_data_by_kl()
mappings_noise, embeddings_noise = data_loader.load_data_by_filter('cluster_label', -1)

# def get_palette(klvalues):
#     pal = px.colors.qualitative.Safe
#     while len(pal)<max(1, max(len(klvalues))):
#         pal = pal + pal
#     return pal
pal = px.colors.qualitative.Safe
# Initialize the app
app = Dash(__name__)

fig = go.Figure()
traces = []
base = BaseTrace(embeddings, mapping)
fig.add_trace(base.create_trace())

# print(mappings_kl['1'])
# sys.exit()
kl_color = {kl: pal[i] for i, kl in enumerate(klvalues)}
for kl in klvalues:
    embeddings_kl = embeddings_kl_d[str(int(kl))]
    mappings_kl_temp = mappings_kl[str(int(kl))]
    new_trace = BaseTrace(embeddings_kl, mappings_kl_temp, color=kl_color[kl], showlegend=True)
    fig.add_trace(new_trace.create_trace())

noise_trace = BaseTrace(embeddings_noise, mappings_noise, color='black', showlegend=True)
fig.add_trace(noise_trace.create_trace())

app.layout = [
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    #dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    #dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure=fig, id='scatter')
]

if __name__ == '__main__':
    app.run(debug=True)


