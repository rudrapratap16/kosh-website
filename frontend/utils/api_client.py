import requests
from dotenv import load_dotenv
import os

# Load .env from project root
BASE = os.path.dirname(os.path.dirname(__file__))
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8080")

def get_filters():
    try:
        r = requests.get(f"{BACKEND_URL}/filters", timeout=30)
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
        r = requests.get(f"{BACKEND_URL}/data", params=params, timeout=60)
        r.raise_for_status()
        payload = r.json()
        return payload.get("data", [])
    except Exception as e:
        print("Error fetching data:", e)
        return None

def get_data_by_outfall(outfall, limit=10000):
    """Get all data for a specific outfall"""
    params = {
        "outfall": outfall,
        "limit": limit
    }
    
    try:
        r = requests.get(f"{BACKEND_URL}/data/by-outfall", params=params, timeout=60)
        r.raise_for_status()
        payload = r.json()
        return payload.get("data", [])
    except Exception as e:
        print("Error fetching outfall data:", e)
        return None

def get_weather_filters():
    """Get precipitation weather dropdown filters"""
    try:
        r = requests.get(f"{BACKEND_URL}/weather/filters", timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error fetching weather filters:", e)
        return None

def get_weather_data(station_id=None, parent_facility_id=None, limit=1000):
    """Get precipitation weather data"""
    params = {}
    if station_id:
        params["station_id"] = station_id
    if parent_facility_id:
        params["parent_facility_id"] = parent_facility_id
    params["limit"] = limit

    try:
        r = requests.get(f"{BACKEND_URL}/weather/data", params=params, timeout=60)
        r.raise_for_status()
        payload = r.json()
        return payload.get("data", [])
    except Exception as e:
        print("Error fetching weather data:", e)
        return None