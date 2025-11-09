import posixpath
from loguru import logger
import os
import io
import json
import numpy as np
import pandas as pd
from azure.storage.blob import BlobServiceClient

class DataLoader:
    def __init__(self, data_path: str = None, container_client=None):
        """
        data_path: local path root (for dev mode)
        container_client: Azure Blob container client (for cloud mode)
        """
        self.data_path = data_path
        self.container_client = container_client
        mode = "Azure Blob" if container_client else "local"
        logger.info(f"DataLoader initialized in {mode} mode with path: {self.data_path}")

    # ---------- Internal helpers ----------

    def _build_path(self, filename: str) -> str:
        """Join folder/file path consistently (local uses os.path, Azure uses posixpath)."""
        if self.container_client:
            import posixpath
            return posixpath.join(self.data_path or "", filename)
        else:
            return os.path.join(self.data_path or "", filename)

    def _read_blob(self, blob_name: str) -> bytes:
        """Download blob content into memory."""
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    # ---------- Loaders ----------

    def load_csv(self, filename: str) -> pd.DataFrame:
        if self.container_client:
            blob_name = self._build_path(filename)
            data = self._read_blob(blob_name)
            df = pd.read_csv(io.BytesIO(data))
            logger.info(f"Loaded CSV blob: {blob_name}")
            return df
        else:
            df_path = self._build_path(filename)
            df = pd.read_csv(df_path)
            logger.info(f"Loaded local CSV: {df_path}")
            return df

    def load_json(self, filename: str):
        if self.container_client:
            blob_name = self._build_path(filename)
            data = self._read_blob(blob_name)
            parsed = json.loads(data.decode("utf-8"))
            logger.info(f"Loaded JSON blob: {blob_name}")
            return parsed
        else:
            json_path = self._build_path(filename)
            with open(json_path, "r") as f:
                parsed = json.load(f)
            logger.info(f"Loaded local JSON: {json_path}")
            return parsed

    def load_numpy(self, filename: str):
        if self.container_client:
            blob_name = self._build_path(filename)
            data = self._read_blob(blob_name)
            array = np.load(io.BytesIO(data))
            logger.info(f"Loaded NumPy blob: {blob_name}")
            return array
        else:
            npy_path = self._build_path(filename)
            array = np.load(npy_path)
            logger.info(f"Loaded local NumPy: {npy_path}")
            return array

class HDBSCAN_DataLoader(DataLoader):
    def __init__(self, base_path: str, folder: str, run: str, modality: str = 'pipeline'):
        if getattr(self, "container_client", None):
            import posixpath
            file_path = posixpath.join(base_path, folder, modality, run)
        else:
            file_path = os.path.join(base_path, folder, modality, run)
        self.base_path = base_path
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
    
    def get_mapping(self, columns: list = ['cluster_label', 'KL-Score']):
        if self.df is None:
            df, _, _, ids = self.load_pipeline_data()
        else:
            df = self.df
            # embeddings = self.embeddings
            ids = self.ids
        
        base_mapping = {
            i: {
                col: df.loc[df['id'] == i, col].values[0]
                for col in columns
            }
            for i in ids
        }
        return base_mapping
    
    def load_data_by_kl(self, columns: list = ['cluster_label', 'KL-Score']):
        if self.df is None:
            df, _, embeddings, ids = self.load_pipeline_data()
        else:
            df = self.df
            embeddings = self.embeddings
            ids = self.ids
        
        kl_values = df['KL-Score'].unique()
        
        result = {}
        embeddings_kl_d = {}
        for kl in kl_values:
            df_kl = df[df['KL-Score'] == kl]
            #embeddings_kl = embeddings[df_kl.index, :]
            ids_kl = df_kl['id'].values

            #get index in ids for ids in ids_kl
            idx_kl = [np.where(ids == np.array(id_))[0][0] for id_ in ids_kl]

            mapping_kl = {
                i: {
                    col: df_kl.loc[df_kl['id'] == i, col].values[0]
                    for col in columns
                }
                for i in ids_kl
            }

            embeddings_kl = embeddings[idx_kl, :]
            embeddings_kl_d[str(int(kl))] = embeddings_kl
            result[str(int(kl))] = mapping_kl

        return result, embeddings_kl_d
    
    def load_data_by_cluster(self, columns: list = ['cluster_label', 'KL-Score']):
        if self.df is None:
            df, _, embeddings, ids = self.load_pipeline_data()
        else:
            df = self.df
            embeddings = self.embeddings
            ids = self.ids

        cluster_values = list(df['cluster_label'].unique())

        try:
            cluster_values.remove(-1)
        except ValueError:
            print("No noise cluster to remove")
            pass

        result = {}
        embeddings_cluster_d = {}
        for cluster in cluster_values:
            df_cluster = df[df['cluster_label'] == cluster]
            #embeddings_kl = embeddings[df_kl.index, :]
            ids_cluster = df_cluster['id'].values

            #get index in ids for ids in ids_cluster
            idx_cluster = [np.where(ids == np.array(id_))[0][0] for id_ in ids_cluster]

            mapping_cluster = {
                i: {
                    col: df_cluster.loc[df_cluster['id'] == i, col].values[0]
                    for col in columns
                }
                for i in ids_cluster
            }

            embeddings_cluster = embeddings[idx_cluster, :]
            embeddings_cluster_d[str(int(cluster))] = embeddings_cluster
            result[str(int(cluster))] = mapping_cluster

        return result, embeddings_cluster_d

    def load_data_by_filter(self, filter_column: str, filter_value):
        if self.df is None:
            df, _, embeddings, ids = self.load_pipeline_data()
        else:
            df = self.df
            embeddings = self.embeddings
            ids = self.ids
        
        df_filt = df[df[filter_column] == filter_value]
        ids_filt = df_filt['id'].values

        #get index in ids for ids in ids_filt
        idx_filt = [np.where(ids == np.array(id_))[0][0] for id_ in ids_filt]

        mapping_filt = {
            i: {
                "cluster_label": df_filt.loc[df_filt['id'] == i, 'cluster_label'].values[0],
                "KL-Score": df_filt.loc[df_filt['id'] == i, 'KL-Score'].values[0]
            }
            for i in ids_filt
        }

        embeddings_filt = embeddings[idx_filt, :]

        return mapping_filt, embeddings_filt
    
    def load_multiple_mappings(self, filter_column: str):
        if self.df is None:
            df, _, embeddings, ids = self.load_pipeline_data()
        else:
            df = self.df
            embeddings = self.embeddings
            ids = self.ids
        
        filter_values = df[filter_column].unique()
        filter_values = filter_values.sort()

        try:
            filter_values.remove(-1)
        except ValueError:
            pass
        
        result = {}
        idx_result = {}
        for val in filter_values:
            df_filt = df[df[filter_column] == val]
            ids_filt = df_filt['id'].values

            idx_filt = [np.where(ids == np.array(id_))[0][0] for id_ in ids_filt]

            mapping_filt = {
                i: {
                    "cluster_label": df_filt.loc[df_filt['id'] == i, 'cluster_label'].values[0],
                    "KL-Score": df_filt.loc[df_filt['id'] == i, 'KL-Score'].values[0]
                }
                for i in ids_filt
            }

            result[str(val)] = mapping_filt
            idx_result[str(val)] = idx_filt

        return result, idx_result

    def load_data_by_binaryfilter(self, filter_column: str, filter_values: int):
        if self.df is None:
            df, _, embeddings, ids = self.load_pipeline_data()
        else:
            df = self.df
            embeddings = self.embeddings
            ids = self.ids

        df['filter_temp'] = df[filter_column].apply(lambda x: 'other' if x != filter_values else "noise")

        mapping_filt = {
            i: {
                "cluster_label": df.loc[df['id'] == i, 'cluster_label'].values[0],
                "KL-Score": df.loc[df['id'] == i, 'KL-Score'].values[0],
                "noise_label": df.loc[df['id'] == i, 'filter_temp'].values[0],
            }
            for i in ids
        }

        return mapping_filt

class ExtendedDataLoader(HDBSCAN_DataLoader):
    def __init__(self, raw_data_path: str, base_path: str, folder: str, run: str, modality: str = 'pipeline'):
        super().__init__(base_path, folder, run, modality)
        self.raw_data_path = raw_data_path
        self.as_df =None
        logger.info("ExtendedDataLoader initialized")

    def merge_mri_data(self, mri_filename: str):
        if self.df is None:
            raise ValueError("Call load_pipeline_data() before merging MRI data.")
        
        if self.container_client:
            import posixpath
            mri_path = posixpath.join(self.raw_data_path, mri_filename)
        else:
            mri_path = os.path.join(self.raw_data_path, mri_filename)
        mri_df = self.load_csv(mri_path)

        merge_cols = [
            'mri_bml_yn', 'mri_cart_yn', 'mri_osteo_yn',
            'mri_syn_yn', 'mri_mnsc_yn', 'mri_lig_yn'
        ]

        self.df = self.df.merge(
            mri_df[['id'] + merge_cols],
            on='id',
            how='left',
            validate='one_to_one'
        )

        return self.df
    
    def clean_id(self, id_column: str = 'id', split_char: str = '.'):
        self.as_df[id_column] = self.as_df[id_column].apply(lambda x: os.path.basename(x).split(split_char)[0])
        logger.info(f"Cleaned IDs in column: {id_column}")
        return self.as_df
    
    def load_anomaly_scores(self, as_folder: str, as_file: str):
        if self.container_client:
            import posixpath
            as_path = posixpath.join(self.base_path, as_folder)
        else:
            as_path = os.path.join(self.base_path, as_folder)
        as_dataloader = DataLoader(as_path)
        self.as_df = as_dataloader.load_csv(as_file)
        self.as_df = self.clean_id(id_column='id', split_char='.')
        logger.info(f"Anomaly scores loaded from: {as_file}")
        return self.as_df
    
    def merge_anomaly_scores(self):
        if self.as_df is None:
            raise ValueError("Call load_anomaly_scores() before merging anomaly scores.")
        
        self.df = self.df.merge(
            self.as_df,
            on='id',
            how='left',
            validate='one_to_one'
        )
        logger.info("Merged anomaly scores into main dataframe")
        return self.df
