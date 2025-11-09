import os
from dotenv import load_dotenv
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
IMG_PATH = os.getenv("IMG_PATH")

# RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")
# PROCESSED_DATA_PATH = os.path.join(DATA_PATH, "processed")
RAW_DATA_PATH = "raw"
PROCESSED_DATA_PATH = "processed"

PLOTLY_URL = os.getenv("PLOTLY_URL", "http://127.0.0.1:8050/")

CLUSTER_FOLDER = os.getenv("CLUSTER_FOLDER", "2025-10-19_hdbscan")
CLUSTER_RUN = os.getenv("CLUSTER_RUN", "run27")

GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL", None)
EMBEDDING_GOOGLE_FORM_URL = os.getenv("EMBEDDING_GOOGLE_FORM_URL", None)
