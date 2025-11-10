from flask import Flask, jsonify, request
from services.bigquery_service import fetch_data, fetch_filters
import os

# Create Flask app at top level
app = Flask(__name__)

@app.route("/filters", methods=["GET"])
def get_filters():
    """Returns unique values for dropdowns"""
    try:
        filters = fetch_filters()
        return jsonify(filters), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/data", methods=["GET"])
def get_data():
    """
    Query params (all optional):
    outfall, parameter, base, unit, start_date, end_date, limit
    """
    try:
        params = {
            "outfall": request.args.get("outfall"),
            "parameter": request.args.get("parameter"),
            "base": request.args.get("base"),
            "unit": request.args.get("unit"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "limit": int(request.args.get("limit", 1000)),
        }
        results = fetch_data(params)
        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: health check
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

from services.bigquery_service import (
    fetch_weather_data, fetch_weather_filters
)

@app.route("/weather/filters", methods=["GET"])
def get_weather_filters():
    """Returns unique weather dropdown values"""
    try:
        filters = fetch_weather_filters()
        return jsonify(filters), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/weather/data", methods=["GET"])
def get_weather_data():
    """Fetch weather data based on filters"""
    try:
        params = {
            "station_id": request.args.get("station_id"),
            "parent_facility_id": request.args.get("parent_facility_id"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "limit": int(request.args.get("limit", 1000)),
        }
        results = fetch_weather_data(params)
        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    port = int(os.environ.get("BACKEND_PORT", 8080))
    app.run(host="0.0.0.0", port=port)

