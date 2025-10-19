import os
from dotenv import load_dotenv
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
IMG_PATH = os.getenv("IMG_PATH")

RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")
PROCESSED_DATA_PATH = os.path.join(DATA_PATH, "processed")
