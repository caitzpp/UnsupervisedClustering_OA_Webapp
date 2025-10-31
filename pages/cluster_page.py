from loguru import logger
import streamlit as st
import config
import pandas as pd
import os

from src.load_data import DataLoader, HDBSCAN_DataLoader, ExtendedDataLoader

RAW_DATA_PATH = config.RAW_DATA_PATH
PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH
folder = config.CLUSTER_FOLDER
run = config.CLUSTER_RUN

#TODO: get anomaly score
#data/processed/outputs/dfs/ss/mod_smallimg3_ss_aggregated_scores.csv
as_file = "mod_smallimg3_ss_aggregated_scores.csv"
as_folder = os.path.join("outputs", "dfs", "ss")

mri_file = '2025-09-25_mrismall.csv'
trace_columns = ['cluster_label', 'KL-Score', 'mri_bml_yn', 'mri_cart_yn', 'mri_osteo_yn', 'mri_syn_yn',
               'mri_mnsc_yn', 'mri_lig_yn']

def show_clusterpage():
    st.header('Cluster Gallery')
    st.markdown(f"[Link to Feedback Form]({config.GOOGLE_FORM_URL})")

    data_loader = ExtendedDataLoader(RAW_DATA_PATH, PROCESSED_DATA_PATH, folder, run)
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

    cols = st.columns(5)

    for i, (_, row) in enumerate(df_cluster.head(max_n).iterrows()):
        img_path = os.path.join(config.IMG_PATH, row['id'] + '.png')
        if os.path.exists(img_path):
            print(f"ImgPath exists {img_path}")
            with cols[i % 5]:
                st.image(str(img_path), use_container_width=True)
        else:
            with cols[i % 5]:
                st.caption(f"Missing: {img_path.name}")


if __name__ == "__main__":
    show_clusterpage()