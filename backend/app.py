from flask import Flask, jsonify, request
from config import BACKEND_PORT
from services.bigquery_service import fetch_data, fetch_filters

app = Flask(__name__)

@app.route("/filters", methods=["GET"])
def get_filters():
    """
    Returns unique values for dropdowns:
    - outfall_number
    - parameter_description
    - statistical_base
    - dmr_value_unit
    """
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


if __name__ == "__main__":
    app.run(port=BACKEND_PORT, debug=True, host='0.0.0.0')
