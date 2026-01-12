import base64
from loguru import logger
import streamlit as st
from streamlit.components.v1 import html, iframe
import config
import pandas as pd
import os
import posixpath

from src.load_data import DataLoader, HDBSCAN_DataLoader, ExtendedDataLoader
from src.azure_blob_storage import get_blob_container_client, blob_exists

RAW_DATA_PATH = config.RAW_DATA_PATH
PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH
# CONTENT_PATH = config.CONTENT_PATH
folder = config.CLUSTER_FOLDER
run = config.CLUSTER_RUN

#TODO: get anomaly score
#data/processed/outputs/dfs/ss/mod_smallimg3_ss_aggregated_scores.csv
as_file = "mod_smallimg3_ss_aggregated_scores.csv"
as_folder = posixpath.join("outputs", "dfs", "ss")

mri_file = '2025-09-25_mrismall.csv'
trace_columns = ['cluster_label', 'KL-Score', 
            #      'mri_bml_yn', 'mri_cart_yn', 'mri_osteo_yn', 'mri_syn_yn',
            #    'mri_mnsc_yn', 'mri_lig_yn'
               ]

container_client = get_blob_container_client("xray-img-st")

def show_clusterpage():
    st.header('Cluster Gallery')
    
    # md_path = posixpath.join(CONTENT_PATH, "cluster_page.md")
    with open("streamlit_app/content/cluster_page.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()
    st.markdown(markdown_text, unsafe_allow_html=True)
    #st.markdown(f"[Link to Feedback Form]({config.GOOGLE_FORM_URL})")

    data_loader = ExtendedDataLoader(RAW_DATA_PATH, PROCESSED_DATA_PATH, folder, run)
    data_loader.container_client = container_client
    df, model_info, embeddings, ids = data_loader.load_pipeline_data()
    data_loader.merge_mri_data(mri_file)
    data_loader.load_anomaly_scores(as_folder, as_file)
    data_loader.merge_anomaly_scores()
    df = data_loader.df

    expected_cols = {'cluster_label', 'id', 'mean'}
    if not expected_cols.issubset(set(df.columns)):
        st.error(f"Dataframe is missing expected columns: {expected_cols - set(df.columns)}")
        return
    
    cluster_list = sorted(df['cluster_label'].unique().tolist())

    # for i in range(len(cluster_list)):
    #     if cluster_list[i] == -1:
    #         #replace with "noise point"
    #         cluster_list[i] = "Noise Points"
 

    selected_cluster = st.selectbox('Select Cluster Label', cluster_list)

    max_n = st.slider('Number of images to display', min_value=1, max_value=100, value=20)

    df_cluster = df[df['cluster_label'] == selected_cluster]

    if "sort_ascending" not in st.session_state:
        st.session_state.sort_ascending = False
  
    clicked = st.button(f"Sort")

    if clicked:
        st.session_state.sort_ascending = not st.session_state.sort_ascending

    button_icon = "⬆️" if st.session_state.sort_ascending else "⬇️"
 
    st.write(f"Currently sorting {button_icon}")
    
    df_cluster = df_cluster.sort_values(by='mean', ascending=st.session_state.sort_ascending)
            
    st.markdown(f"### Showing {len(df_cluster[:max_n])} images for Cluster {selected_cluster}")

    cols1, cols2 = st.columns([3, 1])
    n_cols = 3
    

    with cols1:
        cols = st.columns(n_cols)
        for i, (_, row) in enumerate(df_cluster.head(max_n).iterrows()):
            img_path = row['id'] + '.png'
            if blob_exists(container_client, img_path):
                blob_client = container_client.get_blob_client(img_path)
                blob_data = blob_client.download_blob().readall()
                encoded = base64.b64encode(blob_data).decode("utf-8")
                img_path = f"data:image/png;base64,{encoded}"
                print(f"ImgPath exists {img_path}")
                with cols[i % n_cols]:
                    st.image(str(img_path), use_container_width=True)
            # else:
            #     with cols[i % 5]:
            #         st.caption(f"Missing: {img_path}")

    with cols2:
        iframe("https://tally.so/embed/XxlEkL?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1", height=1000, width=400, scrolling=True)
        # html("""
        # <script async src="https://tally.so/widgets/embed.js"></script>
        # <button 
        #     data-tally-open="XxlEkL" 
        #     data-tally-width="1000" 
        #     data-tally-emoji-text="👋" 
        #     data-tally-emoji-animation="wave"
        #     style="
        #         background-color: #4CAF50;
        #         color: white;
        #         padding: 10px 20px;
        #         font-size: 16px;
        #         border: none;
        #         border-radius: 8px;
        #         cursor: pointer;
        #     "
        #     >
        #     Open Feedback Form
        #     </button>
        # """, height = 1000)


if __name__ == "__main__":
    show_clusterpage()