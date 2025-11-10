import os
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# BigQuery + Backend Configs
PROJECT_ID = os.getenv("PROJECT_ID", "koshai-475618")
DATASET = os.getenv("DATASET", "raw_data")
TABLE = os.getenv("TABLE", "npdes_monitoring")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 5000))

CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
