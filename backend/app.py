from flask import Flask, jsonify, request
from services.bigquery_service import fetch_data, fetch_filters
from flask_cors import CORS
import os

# Create Flask app at top level
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://kosh-frontend-react-569071530463.europe-west1.run.app"}})
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

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

@app.route("/data/by-outfall", methods=["GET"])
def get_data_by_outfall():
    print('sdofnsogfn')
    """Get all data for a specific outfall (no other filters)"""
    try:
        outfall = request.args.get("outfall")
        if not outfall:
            return jsonify({"error": "outfall parameter required"}), 400
        
        limit = int(request.args.get("limit", 10000))
        results = fetch_data({"outfall": outfall, "limit": limit})
        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: health check
@app.route("/health", methods=["GET"])
def health():
    return "okay, this route works", 200

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

from google.cloud import bigquery
from config import PROJECT_ID, DATASET, TABLE

client = bigquery.Client(project=PROJECT_ID)
table_ref = f"{PROJECT_ID}.{DATASET}.{TABLE}"

@app.route("/api/filters/initial", methods=["GET"])
def get_initial_filters():
    """
    Get all unique values for dropdowns on initial load
    """
    try:
        query = f"""
        SELECT 
            ARRAY_AGG(DISTINCT outfall_number IGNORE NULLS ORDER BY outfall_number) as outfalls,
            ARRAY_AGG(DISTINCT parameter_description IGNORE NULLS ORDER BY parameter_description) as parameters,
            ARRAY_AGG(DISTINCT statistical_base IGNORE NULLS ORDER BY statistical_base) as bases,
            ARRAY_AGG(DISTINCT dmr_value_unit IGNORE NULLS ORDER BY dmr_value_unit) as units
        FROM `{table_ref}`
        """
        
        query_job = client.query(query)
        results = list(query_job.result())
        
        if results:
            row = results[0]
            return jsonify({
                "outfalls": row.outfalls or [],
                "parameters": row.parameters or [],
                "bases": row.bases or [],
                "units": row.units or []
            }), 200
        
        return jsonify({
            "outfalls": [],
            "parameters": [],
            "bases": [],
            "units": []
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/filters/cascading", methods=["POST"])
def get_cascading_filters():
    """
    Get filtered options based on current selections
    Request body: {outfall, parameter, base, unit} - all optional
    """
    try:
        data = request.get_json()
        outfall = data.get("outfall")
        parameter = data.get("parameter")
        base = data.get("base")
        unit = data.get("unit")
        
        # Build WHERE clause dynamically
        where_clauses = []
        if outfall:
            where_clauses.append(f"outfall_number = '{outfall}'")
        if parameter:
            where_clauses.append(f"parameter_description = '{parameter}'")
        if base:
            where_clauses.append(f"statistical_base = '{base}'")
        if unit:
            where_clauses.append(f"dmr_value_unit = '{unit}'")
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
        SELECT 
            ARRAY_AGG(DISTINCT outfall_number IGNORE NULLS ORDER BY outfall_number) as outfalls,
            ARRAY_AGG(DISTINCT parameter_description IGNORE NULLS ORDER BY parameter_description) as parameters,
            ARRAY_AGG(DISTINCT statistical_base IGNORE NULLS ORDER BY statistical_base) as bases,
            ARRAY_AGG(DISTINCT dmr_value_unit IGNORE NULLS ORDER BY dmr_value_unit) as units
        FROM `{table_ref}`
        WHERE {where_clause}
        """
        
        query_job = client.query(query)
        results = list(query_job.result())
        
        if results:
            row = results[0]
            return jsonify({
                "outfalls": row.outfalls or [],
                "parameters": row.parameters or [],
                "bases": row.bases or [],
                "units": row.units or []
            }), 200
        
        return jsonify({
            "outfalls": [],
            "parameters": [],
            "bases": [],
            "units": []
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/data/statistics", methods=["GET"])
def get_statistics():
    """
    Get statistical summary for selected filters
    Query params: outfall, parameter, base, unit, start_date, end_date
    """
    try:
        params = {
            "outfall": request.args.get("outfall"),
            "parameter": request.args.get("parameter"),
            "base": request.args.get("base"),
            "unit": request.args.get("unit"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
        }
        
        # Build WHERE clause
        where_clauses = ["dmr_value IS NOT NULL", "dmr_value != ''"]
        
        if params["outfall"]:
            where_clauses.append(f"TRIM(outfall_number) = '{params['outfall']}'")
        if params["parameter"]:
            param_escaped = params['parameter'].replace("'", "\\'")
            where_clauses.append(f"TRIM(parameter_description) = '{param_escaped}'")
        if params["base"]:
            where_clauses.append(f"TRIM(statistical_base) = '{params['base']}'")
        if params["unit"]:
            where_clauses.append(f"TRIM(dmr_value_unit) = '{params['unit']}'")
        if params["start_date"]:
            # Parse STRING date with MM/DD/YYYY format
            where_clauses.append(f"PARSE_DATE('%m/%d/%Y', monitoring_period_date) >= PARSE_DATE('%Y-%m-%d', '{params['start_date']}')")
        if params["end_date"]:
            where_clauses.append(f"PARSE_DATE('%m/%d/%Y', monitoring_period_date) <= PARSE_DATE('%Y-%m-%d', '{params['end_date']}')")
        
        where_clause = " AND ".join(where_clauses)
        
        query = f"""
        WITH stats_data AS (
            SELECT 
                SAFE_CAST(dmr_value AS FLOAT64) as value
            FROM `{table_ref}`
            WHERE {where_clause}
                AND SAFE_CAST(dmr_value AS FLOAT64) IS NOT NULL
        ),
        basic_stats AS (
            SELECT 
                COUNT(*) as count,
                AVG(value) as mean,
                STDDEV(value) as std_dev,
                VAR_POP(value) as variance,
                MIN(value) as min_value,
                MAX(value) as max_value,
                APPROX_QUANTILES(value, 4)[OFFSET(2)] as median
            FROM stats_data
        ),
        moment_stats AS (
            SELECT
                AVG(POW((value - (SELECT mean FROM basic_stats)) / NULLIF((SELECT std_dev FROM basic_stats), 0), 3)) as skewness,
                AVG(POW((value - (SELECT mean FROM basic_stats)) / NULLIF((SELECT std_dev FROM basic_stats), 0), 4)) - 3 as kurtosis
            FROM stats_data
            WHERE (SELECT std_dev FROM basic_stats) > 0
        )
        SELECT 
            b.*,
            m.skewness,
            m.kurtosis
        FROM basic_stats b
        CROSS JOIN moment_stats m
        """
        
        print(f"Executing query with WHERE: {where_clause}")
        query_job = client.query(query)
        results = list(query_job.result())
        print(f"Results: {results}")
        
        if results and results[0].count > 0:
            row = results[0]
            return jsonify({
                "count": row.count,
                "mean": row.mean,
                "std_dev": row.std_dev,
                "variance": row.variance,
                "min": row.min_value,
                "max": row.max_value,
                "median": row.median,
                "skewness": row.skewness,
                "kurtosis": row.kurtosis
            }), 200
        
        return jsonify({"error": "No data found for the specified filters"}), 404
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("BACKEND_PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

