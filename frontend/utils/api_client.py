import requests
from dotenv import load_dotenv
import os

# Load .env from project root
BASE = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE, "..", ".env"))

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

def get_filters():
    try:
        r = requests.get(f"{BACKEND_URL}/api/filters", timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error fetching filters:", e)
        return None

def get_data(outfall=None, parameter=None, base=None, unit=None, start_date=None, end_date=None, limit=1000):
    params = {}
    if outfall:
        params["outfall"] = outfall
    if parameter:
        params["parameter"] = parameter
    if base:
        params["base"] = base
    if unit:
        params["unit"] = unit
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    params["limit"] = limit

    try:
        r = requests.get(f"{BACKEND_URL}/api/data", params=params, timeout=60)
        r.raise_for_status()
        payload = r.json()
        return payload.get("data", [])
    except Exception as e:
        print("Error fetching data:", e)
        return None