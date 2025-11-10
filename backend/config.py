import os
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv('.env')

# BigQuery + Backend Configs
# PROJECT_ID = os.getenv("PROJECT_ID", "koshai-475618")
PROJECT_ID = os.getenv("PROJECT_ID", "temporaty")
print(PROJECT_ID)
DATASET = os.getenv("DATASET", "raw_data")
TABLE = os.getenv("TABLE", "npdes_monitoring")
PORT = int(os.getenv("PORT", 8080))

CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
