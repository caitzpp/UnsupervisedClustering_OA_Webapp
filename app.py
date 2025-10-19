from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import config
import json
import numpy as np

PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH

#TODO: import this with args or env
folder = "2025-10-19_hdbscan"
run = "run27"

file_path = os.path.join(PROCESSED_DATA_PATH, folder, 'pipeline', run)
df_filepath = os.path.join(file_path, f'pipeline_{run}_umap_hdbscan_scaled_allpoints_wKL.csv')
embeddings_path = os.path.join(file_path, 'X_umap_embeddings.npy')
json_path = os.path.join(file_path, f'pipeline_{run}_umap_hdbscan_scaled_model_info.json')

df = pd.read_csv(df_filepath)

with open(json_path, 'r') as f:
    model_info = json.load(f)
    ids = model_info['files']['ids']

def get_data():
    X = np.load(embeddings_path)
    return X

# Initialize the app
app = Dash(__name__)

fig = px.scatter(get_data())

app.layout = [
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    #dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    #dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure=fig, id='scatter')
]

if __name__ == '__main__':
    app.run(debug=True)


