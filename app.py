from dash import Dash, html, dash_table, dcc, callback, Output, Input
# import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import config
import numpy as np

from src.load_data import HDBSCAN_DataLoader

PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH

#TODO: import this with args or env
folder = "2025-10-19_hdbscan"
run = "run27"

data_loader = HDBSCAN_DataLoader(PROCESSED_DATA_PATH, folder, run)
df, model_info, embeddings, ids = data_loader.load_pipeline_data()




# Initialize the app
app = Dash(__name__)

fig = px.scatter(embeddings)

app.layout = [
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    #dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    #dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure=fig, id='scatter')
]

if __name__ == '__main__':
    app.run(debug=True)


