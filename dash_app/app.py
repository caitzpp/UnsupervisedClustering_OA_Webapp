import io
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
# import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import posixpath
import config
import numpy as np
import sys
import base64

from src.load_data import HDBSCAN_DataLoader, DataLoader
from src.azure_blob_storage import get_blob_container_client
from traces.base import BaseTrace, BaseLegend

PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH
RAW_DATA_PATH = config.RAW_DATA_PATH

container_client = get_blob_container_client("xray-img-st")
blob_name = ""

# IMG_PATH = config.IMG_PATH

#http://127.0.0.1:8050/

# example_image="IM0001_1_left.png"
# example_image_path = os.path.join('assets', example_image)

#TODO: import this with args or env
folder = config.CLUSTER_FOLDER
run = config.CLUSTER_RUN

y_legend= 1.0
t_value = 10 #topmargin


mri_file = '2025-09-25_mrismall.csv'
raw_dataloader = DataLoader(RAW_DATA_PATH, container_client=container_client)
mri_df = raw_dataloader.load_csv(mri_file)

data_loader = HDBSCAN_DataLoader(PROCESSED_DATA_PATH, folder, run)
data_loader.container_client = container_client
df, model_info, embeddings, ids = data_loader.load_pipeline_data()
df = df.merge(mri_df[['id', 'mri_bml_yn', 'mri_cart_yn', 'mri_osteo_yn', 'mri_syn_yn',
               'mri_mnsc_yn', 'mri_lig_yn']], left_on='id', right_on='id', how='left')
data_loader.df = df 
# trace_columns = ['cluster_label', 'KL-Score', 'mri_bml_yn', 'mri_cart_yn', 'mri_osteo_yn', 'mri_syn_yn',
#                'mri_mnsc_yn', 'mri_lig_yn']
trace_columns = ['cluster_label', 'KL-Score']
mapping = data_loader.get_mapping(columns=trace_columns)

trace_mappings = {k: i+1 for i, k in enumerate(trace_columns)}



klvalues = list(set(df['KL-Score'].values))
clustervalues = list(set(df['cluster_label'].values))
clustervalues2 = clustervalues.copy()
try:
    clustervalues2.remove(-1)
except ValueError:
    pass
clustervalues2 = sorted(clustervalues2)

mappings_kl, embeddings_kl_d = data_loader.load_data_by_kl(columns=trace_columns)
mappings_noise, embeddings_noise = data_loader.load_data_by_filter('cluster_label', -1)
mappings_cluster, embeddings_cluster_d = data_loader.load_data_by_cluster(columns=trace_columns)

# mappings_clusters, embeddings_clusters = data_loader.load_multiple_mappings('cluster_label')

pal = px.colors.qualitative.Safe

app = Dash(__name__)

fig = go.Figure()
traces = []
base = BaseTrace(embeddings, mapping)
fig.add_trace(base.create_trace())

legend_kl = BaseLegend(title='KL-Score', y=y_legend)
fig.update_layout(legend=legend_kl.create_legend(), margin=dict(t=t_value))

kl_color = {kl: pal[i] for i, kl in enumerate(klvalues)}
for kl in klvalues:
    embeddings_kl = embeddings_kl_d[str(int(kl))]
    mappings_kl_temp = mappings_kl[str(int(kl))]
    new_trace = BaseTrace(embeddings_kl, mappings_kl_temp, color=kl_color[kl], showlegend=True
                          , legend="legend", name =f"{kl}")
    trace_new = new_trace.create_trace(trace_columns=trace_columns, hovertemplate_mappinges=trace_mappings)
    trace_new.legendgroup = f"kl_{kl}"
    fig.add_trace(trace_new)
fig.update_layout(
    legend_groupclick = "toggleitem",
    legend_itemclick = "toggleothers",
    scene = dict(
        xaxis_title='UMAP 1',
        yaxis_title='UMAP 2',
        zaxis_title='UMAP 3',
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.8) 
        )
    )
    , scene_dragmode = 'turntable'
    # , width = 1000
    # , height=800
)

fig3 = go.Figure()
cluster_traces = []
base3 = BaseTrace(embeddings, mapping)
fig3.add_trace(base3.create_trace())

legend_cluster = BaseLegend(title='Cluster Label', y=y_legend)
fig3.update_layout(legend=legend_cluster.create_legend(), margin=dict(t=t_value))

cluster_color = {cl: pal[i] for i, cl in enumerate(clustervalues2)}
for cl in sorted(clustervalues2):
    embeddings_cluster = embeddings_cluster_d[str(int(cl))]
    mappings_cluster_temp = mappings_cluster[str(int(cl))]
    new_cluster_trace = BaseTrace(embeddings_cluster, mappings_cluster_temp, color=cluster_color[cl], showlegend=True
                          , legend="legend", name =f"Cluster {cl}")
    trace_cluster_new = new_cluster_trace.create_trace(trace_columns=trace_columns, hovertemplate_mappinges=trace_mappings)
    trace_cluster_new.legendgroup = f"cluster_{cl}"
    fig3.add_trace(trace_cluster_new)
fig3.update_layout(
    legend_groupclick = "toggleitem",
    legend_itemclick = "toggleothers",
    scene = dict(
        xaxis_title='UMAP 1',
        yaxis_title='UMAP 2',
        zaxis_title='UMAP 3',
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.8) 
        )
    )
    , scene_dragmode = 'turntable'
    # , width = 1000
    # , height=800
)

fig2 = go.Figure()
legend_noise = BaseLegend(title='Noise Points', y=y_legend)
fig2.update_layout(legend2=legend_noise.create_legend(), margin=dict(t=t_value))
fig2.add_trace(base.create_trace())
noise_trace = BaseTrace(embeddings_noise, mappings_noise, color='black', showlegend=True, legend="legend2",
                        name = 'Noise Points')
trace_noise = noise_trace.create_trace()
trace_noise.legendgroup = "noise"
fig2.add_trace(trace_noise)
fig2.update_layout(scene = dict(
        xaxis_title='UMAP 1',
        yaxis_title='UMAP 2',
        zaxis_title='UMAP 3'
    )
    , scene_dragmode = 'turntable'
)


if len(mappings_noise) == 0:
    app.layout = html.Div([
        html.Div([
            dcc.Dropdown(options = ['Clusters', 'KL-Scores'],
                value='Clusters', id='scatter_radioitem', clearable=False
                ,style={'width': '200px', 'marginBottom': '10px'}),
        ]),
        html.Div([
                dcc.Graph(figure={}, id='scatter' 
                , style={'width': '80%', 'height': '80vh'}),
                html.Img(src="", id='image-display',
                        style={'display': 'none'}),

        ], style={
            'display': 'flex',     
            'flexDirection': 'row',  
            'justify-content': 'center',
            'align-items': 'center',
            'gap': '1px'
        })
    ])
else:
    app.layout = html.Div([
        html.Div([
            dcc.Dropdown(options = ['Clusters', 'KL-Scores', 'Noise Points'],
                value='Clusters', id='scatter_radioitem', clearable=False
                ,style={'width': '200px', 'marginBottom': '10px'}),
        ]),
        html.Div([
                dcc.Graph(figure={}, id='scatter' 
                , style={'width': '80%', 'height': '80vh'
                            # , 'marginTop': '50px'
                            }),
                html.Img(src="", id='image-display',
                        style={'display': 'none'}),

        ], style={
            'display': 'flex',     
            'flexDirection': 'row',  
            'justify-content': 'center',
            'align-items': 'center',
            'gap': '1px'
        })
    ])

@callback(
    Output('scatter', 'figure'),
    Input('scatter_radioitem', 'value')
)
def update_scatter(selected_radio):
    if selected_radio == 'KL-Scores':
        return fig
    elif selected_radio == 'Clusters':
        return fig3
    else:
        return fig2


def blob_exists(container_client, blob_name):
    """Check if a blob exists in the container."""
    try:
        container_client.get_blob_client(blob_name).get_blob_properties()
        return True
    except Exception:
        return False
@callback(
    Output('image-display', 'src'),
    Output('image-display', 'style'),
    Input('scatter', 'clickData')
    )
def show_image(clickData, container_client = container_client):
    if not clickData:
        return dash.no_update, {'display': 'none'}
    if clickData:
        point = clickData["points"][0]
        id_ = point["customdata"][0]
        cluster = point["customdata"][1]
        kl = point["customdata"][2]

    test_name = posixpath.join(f"{id_}.png")
    if container_client is not None:
        if blob_exists(container_client=container_client, blob_name=test_name):
            blob_client = container_client.get_blob_client(test_name)
            blob_bytes = blob_client.download_blob().readall()

            encoded = base64.b64encode(blob_bytes).decode("utf-8")
            image_src = f"data:image/png;base64,{encoded}"

            return image_src, {
                'width': '25%',
                'height': 'auto',
                'object-fit': 'contain',
                'margin-left': '0.5%',
                'display': 'block'
            }

        else:
            return dash.no_update, {'display': 'none'}
    else:
        test = os.path.exists(os.path.join('assets', test_name))
        if test:
            return os.path.join('assets', test_name), {'width': '25%',
                        'height': 'auto',
                        'object-fit': 'contain', 
                        'margin-left': '2%',
                        'display': 'block'
                    }
        else:
            return dash.no_update, {'display': 'none'}


if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=8050, debug=True)


