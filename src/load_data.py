from loguru import logger
import os
import pandas as pd
import json
import numpy as np


class DataLoader:
    def __init__(self, data_path: str):
        self.data_path = data_path
        logger.info(f"DataLoader initialized with data path: {self.data_path}")
    
    def load_csv(self, filename: str):
        df_path = os.path.join(self.data_path, filename)
        df = pd.read_csv(df_path)
        logger.info(f"Loaded CSV file: {df_path}")
        return df
    
    def load_json(self, filename: str):
        json_path = os.path.join(self.data_path, filename)
        with open(json_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON file: {json_path}")
        return data
    
    def load_numpy(self, filename: str):
        npy_path = os.path.join(self.data_path, filename)
        data = np.load(npy_path)
        logger.info(f"Loaded Numpy file: {npy_path}")
        return data

class HDBSCAN_DataLoader(DataLoader):
    def __init__(self, base_path: str, folder: str, run: str, modality: str = 'pipeline'):
        file_path = os.path.join(base_path, folder, modality, run)
        super().__init__(file_path)
        self.run = run
        self.modality = modality
        self.df = None
        self.embeddings = None
        self.ids = None
        logger.info(f"HDBSCAN_DataLoader initialized for run: {self.run} and modality: {self.modality}")

    def load_pipeline_data(self):
        df_filename = f'pipeline_{self.run}_umap_hdbscan_scaled_allpoints_wKL.csv'
        json_filename = f'pipeline_{self.run}_umap_hdbscan_scaled_model_info.json'
        embeddings_filename = 'X_umap_embeddings.npy'
        
        df = self.load_csv(df_filename)
        model_info = self.load_json(json_filename)
        ids = model_info['files']['ids']
        embeddings = self.load_numpy(embeddings_filename)

        self.df = df
        self.embeddings = embeddings
        self.ids = ids
        
        return df, model_info, embeddings, ids
    
    def get_mapping(self):
        if self.df is None:
            df, _, _, ids = self.load_pipeline_data()
        else:
            df = self.df
            # embeddings = self.embeddings
            ids = self.ids
        
        base_mapping = {
            i: {
                "cluster_label": df.loc[df['id'] == i, 'cluster_label'].values[0],
                "KL-Score": df.loc[df['id'] == i, 'KL-Score'].values[0],
            }
            for i in ids
        }
        return base_mapping
    
    def load_data_by_kl(self):
        if self.df is None:
            df, _, embeddings, ids = self.load_pipeline_data()
        else:
            df = self.df
            embeddings = self.embeddings
            ids = self.ids
        
        kl_values = df['KL-Score'].unique()
        
        result = {}
        for kl in kl_values:
            df_kl = df[df['KL-Score'] == kl]
            #embeddings_kl = embeddings[df_kl.index, :]
            ids_kl = df_kl['id'].values

            #get index in ids for ids in ids_kl
            idx_kl = [np.where(ids == id_)[0][0] for id_ in ids_kl]

            mapping_kl = {
                i: {
                    "cluster_label": df_kl.loc[df_kl['id'] == i, 'cluster_label'].values[0],
                    "KL-Score": df_kl.loc[df_kl['id'] == i, 'KL-Score'].values[0]
                }
                for i in ids_kl
            }

            embeddings_kl = embeddings[idx_kl, :]
            result[kl] = mapping_kl

        return result, embeddings_kl
