import streamlit as st
import config
import pandas as pd
import os

from src.load_data import DataLoader, HDBSCAN_DataLoader

RAW_DATA_PATH = config.RAW_DATA_PATH
PROCESSED_DATA_PATH = config.PROCESSED_DATA_PATH
folder = "2025-10-19_hdbscan"
run = "run27"

#TODO: get anomaly score
#data/processed/outputs/dfs/ss/mod_smallimg3_ss_aggregated_scores.csv
as_file = "mod_smallimg3_ss_aggregated_scores.csv"
as_folder = os.path.join("outputs", "dfs", "ss")

mri_file = '2025-09-25_mrismall.csv'
trace_columns = ['cluster_label', 'KL-Score', 'mri_bml_yn', 'mri_cart_yn', 'mri_osteo_yn', 'mri_syn_yn',
               'mri_mnsc_yn', 'mri_lig_yn']

def show_clusterpage():
    st.header('Cluster Gallery')

    raw_dataloader = DataLoader(RAW_DATA_PATH)
    mri_df = raw_dataloader.load_csv(mri_file)

    data_loader = HDBSCAN_DataLoader(PROCESSED_DATA_PATH, folder, run)
    df, model_info, embeddings, ids = data_loader.load_pipeline_data()
    df = df.merge(mri_df[['id', 'mri_bml_yn', 'mri_cart_yn', 'mri_osteo_yn', 'mri_syn_yn',
                'mri_mnsc_yn', 'mri_lig_yn']], left_on='id', right_on='id', how='left')
    data_loader.df = df 

    as_dataloader = DataLoader(os.path.join(PROCESSED_DATA_PATH, as_folder))
    as_df = as_dataloader.load_csv(as_file)
    print(as_df.columns)
    
    # df = df.merge()

    # expected_cols = {'cluster_label', 'id'}
    # if not expected_cols.issubset(set(df.columns)):
    #     st.error(f"Dataframe is missing expected columns: {expected_cols - set(df.columns)}")
    #     return
    
    # # Dropdown
    # cluster_list = sorted(df['cluster_label'].unique().tolist())
    # selected_cluster = st.selectbox('Select Cluster Label', cluster_list)

    # max_n = st.slider('Number of images to display', min_value=1, max_value=100, value=20)

if __name__ == "__main__":
    show_clusterpage()