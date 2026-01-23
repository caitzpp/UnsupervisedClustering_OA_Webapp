import os
from dotenv import load_dotenv
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
IMG_PATH = os.getenv("IMG_PATH")


USE_LOCAL_ASSETS = os.getenv("USE_LOCAL_ASSETS", True)
if USE_LOCAL_ASSETS == 'True':
    USE_LOCAL_ASSETS=True
else:
    USE_LOCAL_ASSETS=False

if USE_LOCAL_ASSETS:
    RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")
    PROCESSED_DATA_PATH = os.path.join(DATA_PATH, "processed")
else:
    RAW_DATA_PATH = "raw"
    PROCESSED_DATA_PATH = "processed"
CONTENT_PATH = "content"

PLOTLY_URL = os.getenv("PLOTLY_URL", "http://127.0.0.1:8050/")

MODALITY=os.getenv("MODALITY", "pipeline")
CLUSTER_FOLDER = os.getenv("CLUSTER_FOLDER", "2025-10-19_hdbscan")
CLUSTER_RUN = os.getenv("CLUSTER_RUN", "run27")

SECRET_KEY = os.environ["SECRET_KEY"]
PASSWORD_USER1 = os.environ["PASSWORD_USER1"]
PASSWORD_USER2 = os.environ["PASSWORD_USER2"]
