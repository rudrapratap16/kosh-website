from flask import Flask, jsonify, request
from services.bigquery_service import fetch_data, fetch_filters
from flask_cors import CORS
import os

# Create Flask app at top level
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://kosh-frontend-react-569071530463.europe-west1.run.app"}})
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# @app.route("/filters", methods=["GET"])
# def get_filters():
#     """Returns unique values for dropdowns"""
#     try:
#         filters = fetch_filters()
#         return jsonify(filters), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/data", methods=["GET"])
# def get_data():
#     """
#     Query params (all optional):
#     outfall, parameter, base, unit, start_date, end_date, limit
#     """
#     try:
#         params = {
#             "outfall": request.args.get("outfall"),
#             "parameter": request.args.get("parameter"),
#             "base": request.args.get("base"),
#             "unit": request.args.get("unit"),
#             "start_date": request.args.get("start_date"),
#             "end_date": request.args.get("end_date"),
#             "limit": int(request.args.get("limit", 1000)),
#         }
#         results = fetch_data(params)
#         return jsonify({"data": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/data/by-outfall", methods=["GET"])
# def get_data_by_outfall():
#     print('sdofnsogfn')
#     """Get all data for a specific outfall (no other filters)"""
#     try:
#         outfall = request.args.get("outfall")
#         if not outfall:
#             return jsonify({"error": "outfall parameter required"}), 400
        
#         limit = int(request.args.get("limit", 10000))
#         results = fetch_data({"outfall": outfall, "limit": limit})
#         return jsonify({"data": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Optional: health check
# @app.route("/health", methods=["GET"])
# def health():
#     return "okay, this route works", 200

# from services.bigquery_service import (
#     fetch_weather_data, fetch_weather_filters
# )

# @app.route("/weather/filters", methods=["GET"])
# def get_weather_filters():
#     """Returns unique weather dropdown values"""
#     try:
#         filters = fetch_weather_filters()
#         return jsonify(filters), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/weather/data", methods=["GET"])
# def get_weather_data():
#     """Fetch weather data based on filters"""
#     try:
#         params = {
#             "station_id": request.args.get("station_id"),
#             "parent_facility_id": request.args.get("parent_facility_id"),
#             "start_date": request.args.get("start_date"),
#             "end_date": request.args.get("end_date"),
#             "limit": int(request.args.get("limit", 1000)),
#         }
#         results = fetch_weather_data(params)
#         return jsonify({"data": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# from google.cloud import bigquery
# from config import PROJECT_ID, DATASET, TABLE

# client = bigquery.Client(project=PROJECT_ID)
# table_ref = f"{PROJECT_ID}.{DATASET}.{TABLE}"

# @app.route("/api/filters/initial", methods=["GET"])
# def get_initial_filters():
#     """
#     Get all unique values for dropdowns on initial load
#     """
#     try:
#         query = f"""
#         SELECT 
#             ARRAY_AGG(DISTINCT outfall_number IGNORE NULLS ORDER BY outfall_number) as outfalls,
#             ARRAY_AGG(DISTINCT parameter_description IGNORE NULLS ORDER BY parameter_description) as parameters,
#             ARRAY_AGG(DISTINCT statistical_base IGNORE NULLS ORDER BY statistical_base) as bases,
#             ARRAY_AGG(DISTINCT dmr_value_unit IGNORE NULLS ORDER BY dmr_value_unit) as units
#         FROM `{table_ref}`
#         """
        
#         query_job = client.query(query)
#         results = list(query_job.result())
        
#         if results:
#             row = results[0]
#             return jsonify({
#                 "outfalls": row.outfalls or [],
#                 "parameters": row.parameters or [],
#                 "bases": row.bases or [],
#                 "units": row.units or []
#             }), 200
        
#         return jsonify({
#             "outfalls": [],
#             "parameters": [],
#             "bases": [],
#             "units": []
#         }), 200
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route("/api/filters/cascading", methods=["POST"])
# def get_cascading_filters():
#     """
#     Cascading filters with no lock-in:
#     - Outfalls: Always ALL
#     - Parameters: Filtered by outfall only
#     - Bases: Filtered by outfall + parameter (excluding base itself)
#     - Units: Filtered by outfall + parameter + base (excluding unit itself)
#     """
#     try:
#         data = request.get_json()
#         outfall = data.get("outfall")
#         parameter = data.get("parameter")
#         base = data.get("base")
#         unit = data.get("unit")
        
#         # Build WHERE clauses for each dropdown
#         # Parameters: use only outfall
#         where_parameters = f"outfall_number = '{outfall}'" if outfall else "1=1"
        
#         # Bases: use outfall + parameter (but not base itself)
#         clauses_bases = []
#         if outfall:
#             clauses_bases.append(f"outfall_number = '{outfall}'")
#         if parameter:
#             clauses_bases.append(f"parameter_description = '{parameter}'")
#         where_bases = " AND ".join(clauses_bases) if clauses_bases else "1=1"
        
#         # Units: use outfall + parameter + base (but not unit itself)
#         clauses_units = []
#         if outfall:
#             clauses_units.append(f"outfall_number = '{outfall}'")
#         if parameter:
#             clauses_units.append(f"parameter_description = '{parameter}'")
#         if base:
#             clauses_units.append(f"statistical_base = '{base}'")
#         where_units = " AND ".join(clauses_units) if clauses_units else "1=1"
        
#         query = f"""
#         SELECT 
#             (SELECT ARRAY_AGG(DISTINCT outfall_number IGNORE NULLS ORDER BY outfall_number) 
#              FROM `{table_ref}`) as outfalls,
#             (SELECT ARRAY_AGG(DISTINCT parameter_description IGNORE NULLS ORDER BY parameter_description) 
#              FROM `{table_ref}` WHERE {where_parameters}) as parameters,
#             (SELECT ARRAY_AGG(DISTINCT statistical_base IGNORE NULLS ORDER BY statistical_base) 
#              FROM `{table_ref}` WHERE {where_bases}) as bases,
#             (SELECT ARRAY_AGG(DISTINCT dmr_value_unit IGNORE NULLS ORDER BY dmr_value_unit) 
#              FROM `{table_ref}` WHERE {where_units}) as units
#         """
        
#         query_job = client.query(query)
#         results = list(query_job.result())
        
#         if results:
#             row = results[0]
#             return jsonify({
#                 "outfalls": row.outfalls or [],
#                 "parameters": row.parameters or [],
#                 "bases": row.bases or [],
#                 "units": row.units or []
#             }), 200
        
#         return jsonify({
#             "outfalls": [],
#             "parameters": [],
#             "bases": [],
#             "units": []
#         }), 200
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route("/api/data/statistics", methods=["GET"])
# def get_statistics():
#     """
#     Get statistical summary for selected filters
#     Query params: outfall, parameter, base, unit, start_date, end_date
#     """
#     try:
#         params = {
#             "outfall": request.args.get("outfall"),
#             "parameter": request.args.get("parameter"),
#             "base": request.args.get("base"),
#             "unit": request.args.get("unit"),
#             "start_date": request.args.get("start_date"),
#             "end_date": request.args.get("end_date"),
#         }
        
#         # Build WHERE clause
#         where_clauses = ["dmr_value IS NOT NULL", "dmr_value != ''"]
        
#         if params["outfall"]:
#             where_clauses.append(f"TRIM(outfall_number) = '{params['outfall']}'")
#         if params["parameter"]:
#             param_escaped = params['parameter'].replace("'", "\\'")
#             where_clauses.append(f"TRIM(parameter_description) = '{param_escaped}'")
#         if params["base"]:
#             where_clauses.append(f"TRIM(statistical_base) = '{params['base']}'")
#         if params["unit"]:
#             where_clauses.append(f"TRIM(dmr_value_unit) = '{params['unit']}'")
#         if params["start_date"]:
#             # Parse STRING date with MM/DD/YYYY format
#             where_clauses.append(f"PARSE_DATE('%m/%d/%Y', monitoring_period_date) >= PARSE_DATE('%Y-%m-%d', '{params['start_date']}')")
#         if params["end_date"]:
#             where_clauses.append(f"PARSE_DATE('%m/%d/%Y', monitoring_period_date) <= PARSE_DATE('%Y-%m-%d', '{params['end_date']}')")
        
#         where_clause = " AND ".join(where_clauses)
        
#         query = f"""
#         WITH stats_data AS (
#             SELECT 
#                 SAFE_CAST(dmr_value AS FLOAT64) as value
#             FROM `{table_ref}`
#             WHERE {where_clause}
#                 AND SAFE_CAST(dmr_value AS FLOAT64) IS NOT NULL
#         ),
#         basic_stats AS (
#             SELECT 
#                 COUNT(*) as count,
#                 AVG(value) as mean,
#                 STDDEV(value) as std_dev,
#                 VAR_POP(value) as variance,
#                 MIN(value) as min_value,
#                 MAX(value) as max_value,
#                 APPROX_QUANTILES(value, 4)[OFFSET(2)] as median
#             FROM stats_data
#         ),
#         moment_stats AS (
#             SELECT
#                 AVG(POW((value - (SELECT mean FROM basic_stats)) / NULLIF((SELECT std_dev FROM basic_stats), 0), 3)) as skewness,
#                 AVG(POW((value - (SELECT mean FROM basic_stats)) / NULLIF((SELECT std_dev FROM basic_stats), 0), 4)) - 3 as kurtosis
#             FROM stats_data
#             WHERE (SELECT std_dev FROM basic_stats) > 0
#         )
#         SELECT 
#             b.*,
#             m.skewness,
#             m.kurtosis
#         FROM basic_stats b
#         CROSS JOIN moment_stats m
#         """
        
#         print(f"Executing query with WHERE: {where_clause}")
#         query_job = client.query(query)
#         results = list(query_job.result())
#         print(f"Results: {results}")
        
#         if results and results[0].count > 0:
#             row = results[0]
#             return jsonify({
#                 "count": row.count,
#                 "mean": row.mean,
#                 "std_dev": row.std_dev,
#                 "variance": row.variance,
#                 "min": row.min_value,
#                 "max": row.max_value,
#                 "median": row.median,
#                 "skewness": row.skewness,
#                 "kurtosis": row.kurtosis
#             }), 200
        
#         return jsonify({"error": "No data found for the specified filters"}), 404
        
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"error": str(e)}), 500

from google.cloud import bigquery
from flask import request, jsonify
from config import PROJECT_ID, DATASET

client = bigquery.Client(project=PROJECT_ID)
npdes_table_ref = f"{PROJECT_ID}.{DATASET}.npdes"  # Update with your actual NPDES table name
weather_table_ref = f"{PROJECT_ID}.{DATASET}.prep_temp_snow"


@app.route("/api/filters/initial", methods=["GET"])
def get_initial_filters():
    """
    Get all unique values for dropdowns on initial load
    Combines NPDES and Weather data
    """
    try:
        query = f"""
        SELECT 
            -- Station Names from NPDES only (combined with permit number)
            (SELECT ARRAY_AGG(combined_name ORDER BY combined_name) 
             FROM (
                SELECT DISTINCT CONCAT(station_name, '_', npdes_permit_number) as combined_name
                FROM `{npdes_table_ref}` 
                WHERE station_name IS NOT NULL AND npdes_permit_number IS NOT NULL
             )) as permit_numbers,
            
            -- Outfalls from NPDES only
            (SELECT ARRAY_AGG(outfall ORDER BY outfall) 
             FROM (
                SELECT DISTINCT outfall_number as outfall
                FROM `{npdes_table_ref}`
                WHERE outfall_number IS NOT NULL
             )) as outfalls,
            
            -- Parameters from both tables
            (SELECT ARRAY_AGG(param ORDER BY param)
             FROM (
                SELECT DISTINCT parameter_description as param
                FROM (
                    SELECT parameter_description FROM `{npdes_table_ref}`
                    UNION DISTINCT
                    SELECT parameter_description FROM `{weather_table_ref}`
                )
                WHERE parameter_description IS NOT NULL
             )) as parameters,
            
            -- Bases from both tables
            (SELECT ARRAY_AGG(base_val ORDER BY base_val)
             FROM (
                SELECT DISTINCT statistical_base as base_val
                FROM (
                    SELECT statistical_base FROM `{npdes_table_ref}`
                    UNION DISTINCT
                    SELECT statistical_base FROM `{weather_table_ref}`
                )
                WHERE statistical_base IS NOT NULL
             )) as bases,
            
            -- Units from both tables
            (SELECT ARRAY_AGG(unit_val ORDER BY unit_val)
             FROM (
                SELECT DISTINCT dmr_value_unit as unit_val
                FROM (
                    SELECT dmr_value_unit FROM `{npdes_table_ref}`
                    UNION DISTINCT
                    SELECT dmr_value_unit FROM `{weather_table_ref}`
                )
                WHERE dmr_value_unit IS NOT NULL
             )) as units
        """
        
        query_job = client.query(query)
        results = list(query_job.result())
        
        if results:
            row = results[0]
            return jsonify({
                "permit_numbers": row.permit_numbers or [],
                "outfalls": row.outfalls or [],
                "parameters": row.parameters or [],
                "bases": row.bases or [],
                "units": row.units or []
            }), 200
        
        return jsonify({
            "permit_numbers": [],
            "outfalls": [],
            "parameters": [],
            "bases": [],
            "units": []
        }), 200
        
    except Exception as e:
        print(f"Error in get_initial_filters: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/filters/cascading", methods=["POST"])
def get_cascading_filters():
    """
    Cascading filters that include both NPDES and Weather data
    Weather parameters are always available regardless of outfall/permit selection
    """
    try:
        data = request.get_json()
        permit_number = data.get("permit_number")  # This is now "station_name_npdes_permit_number"
        outfall = data.get("outfall")
        parameter = data.get("parameter")
        base = data.get("base")
        
        # Extract just the station_name part if permit_number contains underscore
        station_name_for_query = None
        if permit_number and '_' in permit_number:
            station_name_for_query = permit_number.rsplit('_', 1)[0]  # Get everything before last underscore
        elif permit_number:
            station_name_for_query = permit_number
        
        # Build NPDES filters (using station_name)
        npdes_filters = []
        if station_name_for_query:
            npdes_filters.append(f"station_name = '{station_name_for_query}'")
        if outfall:
            npdes_filters.append(f"outfall_number = '{outfall}'")
        
        npdes_filter_sql = " AND ".join(npdes_filters) if npdes_filters else "1=1"
        
        # Station Names: Always all from NPDES (combined format)
        permit_numbers_query = f"""
        SELECT ARRAY_AGG(combined_name ORDER BY combined_name) as permit_numbers
        FROM (
            SELECT DISTINCT CONCAT(station_name, '_', npdes_permit_number) as combined_name
            FROM `{npdes_table_ref}`
            WHERE station_name IS NOT NULL AND npdes_permit_number IS NOT NULL
        )
        """
        
        # Outfalls: Filtered by station name if selected
        outfalls_filter = f"station_name = '{station_name_for_query}'" if station_name_for_query else "1=1"
        outfalls_query = f"""
        SELECT ARRAY_AGG(outfall ORDER BY outfall) as outfalls
        FROM (
            SELECT DISTINCT outfall_number as outfall
            FROM `{npdes_table_ref}`
            WHERE {outfalls_filter} AND outfall_number IS NOT NULL
        )
        """
        
        # Parameters: NPDES (filtered by station/outfall) + Weather (always included)
        parameters_query = f"""
        SELECT ARRAY_AGG(param ORDER BY param) as parameters
        FROM (
            SELECT DISTINCT parameter_description as param
            FROM (
                SELECT parameter_description FROM `{npdes_table_ref}` WHERE {npdes_filter_sql}
                UNION DISTINCT
                SELECT parameter_description FROM `{weather_table_ref}`
            )
            WHERE parameter_description IS NOT NULL
        )
        """
        
        # Bases: Filtered by parameter (from both tables)
        if parameter:
            bases_query = f"""
            SELECT ARRAY_AGG(base_val ORDER BY base_val) as bases
            FROM (
                SELECT DISTINCT statistical_base as base_val
                FROM (
                    SELECT statistical_base FROM `{npdes_table_ref}` 
                    WHERE parameter_description = '{parameter}' AND {npdes_filter_sql}
                    UNION DISTINCT
                    SELECT statistical_base FROM `{weather_table_ref}` 
                    WHERE parameter_description = '{parameter}'
                )
                WHERE statistical_base IS NOT NULL
            )
            """
        else:
            bases_query = f"""
            SELECT ARRAY_AGG(base_val ORDER BY base_val) as bases
            FROM (
                SELECT DISTINCT statistical_base as base_val
                FROM (
                    SELECT statistical_base FROM `{npdes_table_ref}` WHERE {npdes_filter_sql}
                    UNION DISTINCT
                    SELECT statistical_base FROM `{weather_table_ref}`
                )
                WHERE statistical_base IS NOT NULL
            )
            """
        
        # Units: Filtered by parameter + base (from both tables)
        unit_filters = []
        if parameter:
            unit_filters.append(f"parameter_description = '{parameter}'")
        if base:
            unit_filters.append(f"statistical_base = '{base}'")
        
        unit_where = " AND ".join(unit_filters) if unit_filters else "1=1"
        npdes_unit_where = f"{unit_where} AND {npdes_filter_sql}"
        
        units_query = f"""
        SELECT ARRAY_AGG(unit_val ORDER BY unit_val) as units
        FROM (
            SELECT DISTINCT dmr_value_unit as unit_val
            FROM (
                SELECT dmr_value_unit FROM `{npdes_table_ref}` WHERE {npdes_unit_where}
                UNION DISTINCT
                SELECT dmr_value_unit FROM `{weather_table_ref}` WHERE {unit_where}
            )
            WHERE dmr_value_unit IS NOT NULL
        )
        """
        
        # Combine all queries
        combined_query = f"""
        SELECT 
            ({permit_numbers_query}) as permit_numbers,
            ({outfalls_query}) as outfalls,
            ({parameters_query}) as parameters,
            ({bases_query}) as bases,
            ({units_query}) as units
        """
        
        query_job = client.query(combined_query)
        results = list(query_job.result())
        
        if results:
            row = results[0]
            return jsonify({
                "permit_numbers": row.permit_numbers or [],
                "outfalls": row.outfalls or [],
                "parameters": row.parameters or [],
                "bases": row.bases or [],
                "units": row.units or []
            }), 200
        
        return jsonify({
            "permit_numbers": [],
            "outfalls": [],
            "parameters": [],
            "bases": [],
            "units": []
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/data/combined", methods=["GET"])
def get_combined_data():
    """
    Fetches data from both NPDES and Weather tables
    Weather data appears regardless of permit/outfall selection
    """
    try:
        params = {
            "permit_number": request.args.get("permit_number"),  # This is now "station_name_npdes_permit_number"
            "outfall": request.args.get("outfall"),
            "parameter": request.args.get("parameter"),
            "base": request.args.get("base"),
            "unit": request.args.get("unit"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "limit": int(request.args.get("limit", 1000)),
        }
        
        # Extract station_name from combined format
        permit_number_param = params.get("permit_number")
        station_name_for_query = None
        if permit_number_param and '_' in permit_number_param:
            station_name_for_query = permit_number_param.rsplit('_', 1)[0]  # Get everything before last underscore
        elif permit_number_param:
            station_name_for_query = permit_number_param
        
        # Build NPDES filters (using station_name)
        npdes_where = []
        weather_where = []
        query_params = []
        
        # NPDES filters
        if station_name_for_query:
            npdes_where.append("station_name = @permit_number")
            query_params.append(bigquery.ScalarQueryParameter("permit_number", "STRING", station_name_for_query))
        
        if params.get("outfall"):
            npdes_where.append("outfall_number = @outfall")
            query_params.append(bigquery.ScalarQueryParameter("outfall", "STRING", params["outfall"]))
        
        if params.get("parameter"):
            npdes_where.append("parameter_description = @parameter")
            weather_where.append("parameter_description = @parameter")
            query_params.append(bigquery.ScalarQueryParameter("parameter", "STRING", params["parameter"]))
        
        if params.get("base"):
            npdes_where.append("statistical_base = @base")
            weather_where.append("statistical_base = @base")
            query_params.append(bigquery.ScalarQueryParameter("base", "STRING", params["base"]))
        
        if params.get("unit"):
            npdes_where.append("dmr_value_unit = @unit")
            weather_where.append("dmr_value_unit = @unit")
            query_params.append(bigquery.ScalarQueryParameter("unit", "STRING", params["unit"]))
        
        # Date filters
        if params.get("start_date"):
            npdes_where.append("PARSE_DATE('%m/%d/%Y', monitoring_period_date) >= @start_date")
            weather_where.append("date >= @start_date")
            query_params.append(bigquery.ScalarQueryParameter("start_date", "DATE", params["start_date"]))
        
        if params.get("end_date"):
            npdes_where.append("PARSE_DATE('%m/%d/%Y', monitoring_period_date) <= @end_date")
            weather_where.append("date <= @end_date")
            query_params.append(bigquery.ScalarQueryParameter("end_date", "DATE", params["end_date"]))
        
        npdes_where_sql = "WHERE " + " AND ".join(npdes_where) if npdes_where else ""
        weather_where_sql = "WHERE " + " AND ".join(weather_where) if weather_where else ""
        
        limit = params.get("limit", 1000)
        
        # Combined query
        sql = f"""
        WITH combined AS (
            -- NPDES data
            SELECT
                PARSE_DATE('%m/%d/%Y', monitoring_period_date) as date,
                SAFE_CAST(dmr_value AS FLOAT64) AS value,
                station_name,
                npdes_permit_number,
                outfall_number,
                monitoring_location_code,
                limit_set_designator,
                parameter_code,
                parameter_description,
                limit_value,
                limit_value_unit,
                dmr_value_type,
                statistical_base,
                limit_type_code,
                dmr_value_unit,
                dmr_comments,
                source_file_name,
                ingestion_timestamp,
                'NPDES' as data_source
            FROM `{npdes_table_ref}`
            {npdes_where_sql}
            
            UNION ALL
            
            -- Weather data
            SELECT
                date,
                value,
                NULL as station_name,
                NULL as npdes_permit_number,
                NULL as outfall_number,
                NULL as monitoring_location_code,
                NULL as limit_set_designator,
                NULL as parameter_code,
                parameter_description,
                NULL as limit_value,
                NULL as limit_value_unit,
                NULL as dmr_value_type,
                statistical_base,
                NULL as limit_type_code,
                dmr_value_unit,
                NULL as dmr_comments,
                source_file_name,
                ingestion_timestamp,
                'Weather' as data_source
            FROM `{weather_table_ref}`
            {weather_where_sql}
        )
        SELECT * FROM combined
        ORDER BY date
        LIMIT {limit}
        """
        
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        query_job = client.query(sql, job_config=job_config)
        
        rows = []
        for row in query_job.result():
            rows.append({
                "date": row.date.isoformat() if row.date else None,
                "value": row.value,
                "station_name": row.station_name,
                "npdes_permit_number": row.npdes_permit_number,
                "outfall_number": row.outfall_number,
                "monitoring_location_code": row.monitoring_location_code,
                "limit_set_designator": row.limit_set_designator,
                "parameter_code": row.parameter_code,
                "parameter_description": row.parameter_description,
                "limit_value": row.limit_value,
                "limit_value_unit": row.limit_value_unit,
                "dmr_value_type": row.dmr_value_type,
                "statistical_base": row.statistical_base,
                "limit_type_code": row.limit_type_code,
                "dmr_value_unit": row.dmr_value_unit,
                "dmr_comments": row.dmr_comments,
                "source_file_name": row.source_file_name,
                "ingestion_timestamp": row.ingestion_timestamp.isoformat() if row.ingestion_timestamp else None,
                "data_source": row.data_source
            })
        
        return jsonify({"data": rows}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/data/statistics/combined", methods=["GET"])
def get_combined_statistics():
    """
    Get statistics for combined NPDES and Weather data
    """
    try:
        params = {
            "permit_number": request.args.get("permit_number"),  # This is now "station_name_npdes_permit_number"
            "outfall": request.args.get("outfall"),
            "parameter": request.args.get("parameter"),
            "base": request.args.get("base"),
            "unit": request.args.get("unit"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
        }
        
        # Extract station_name from combined format
        permit_number_param = params.get("permit_number")
        station_name_for_query = None
        if permit_number_param and '_' in permit_number_param:
            station_name_for_query = permit_number_param.rsplit('_', 1)[0]  # Get everything before last underscore
        elif permit_number_param:
            station_name_for_query = permit_number_param
        
        # Build filters (same logic as combined data, using station_name)
        npdes_where = []
        weather_where = []
        query_params = []
        
        if station_name_for_query:
            npdes_where.append("station_name = @permit_number")
            query_params.append(bigquery.ScalarQueryParameter("permit_number", "STRING", station_name_for_query))
        
        if params.get("outfall"):
            npdes_where.append("outfall_number = @outfall")
            query_params.append(bigquery.ScalarQueryParameter("outfall", "STRING", params["outfall"]))
        
        if params.get("parameter"):
            npdes_where.append("parameter_description = @parameter")
            weather_where.append("parameter_description = @parameter")
            query_params.append(bigquery.ScalarQueryParameter("parameter", "STRING", params["parameter"]))
        
        if params.get("base"):
            npdes_where.append("statistical_base = @base")
            weather_where.append("statistical_base = @base")
            query_params.append(bigquery.ScalarQueryParameter("base", "STRING", params["base"]))
        
        if params.get("unit"):
            npdes_where.append("dmr_value_unit = @unit")
            weather_where.append("dmr_value_unit = @unit")
            query_params.append(bigquery.ScalarQueryParameter("unit", "STRING", params["unit"]))
        
        if params.get("start_date"):
            npdes_where.append("PARSE_DATE('%m/%d/%Y', monitoring_period_date) >= @start_date")
            weather_where.append("date >= @start_date")
            query_params.append(bigquery.ScalarQueryParameter("start_date", "DATE", params["start_date"]))
        
        if params.get("end_date"):
            npdes_where.append("PARSE_DATE('%m/%d/%Y', monitoring_period_date) <= @end_date")
            weather_where.append("date <= @end_date")
            query_params.append(bigquery.ScalarQueryParameter("end_date", "DATE", params["end_date"]))
        
        npdes_where_sql = "WHERE " + " AND ".join(npdes_where) if npdes_where else ""
        weather_where_sql = "WHERE " + " AND ".join(weather_where) if weather_where else ""
        
        sql = f"""
        WITH combined AS (
            SELECT SAFE_CAST(dmr_value AS FLOAT64) AS value
            FROM `{npdes_table_ref}`
            {npdes_where_sql}
            
            UNION ALL
            
            SELECT value
            FROM `{weather_table_ref}`
            {weather_where_sql}
        ),
        basic_stats AS (
            SELECT 
                COUNT(*) as count,
                AVG(value) as mean,
                STDDEV(value) as std_dev,
                VAR_POP(value) as variance,
                MIN(value) as min_value,
                MAX(value) as max_value,
                APPROX_QUANTILES(value, 100)[OFFSET(25)] as q25,
                APPROX_QUANTILES(value, 100)[OFFSET(50)] as median,
                APPROX_QUANTILES(value, 100)[OFFSET(75)] as q75
            FROM combined
            WHERE value IS NOT NULL
        ),
        moment_stats AS (
            SELECT
                AVG(POW((value - (SELECT mean FROM basic_stats)) / NULLIF((SELECT std_dev FROM basic_stats), 0), 3)) as skewness,
                AVG(POW((value - (SELECT mean FROM basic_stats)) / NULLIF((SELECT std_dev FROM basic_stats), 0), 4)) - 3 as kurtosis
            FROM combined
            WHERE value IS NOT NULL AND (SELECT std_dev FROM basic_stats) > 0
        )
        SELECT 
            b.*,
            m.skewness,
            m.kurtosis
        FROM basic_stats b
        CROSS JOIN moment_stats m
        """
        
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        query_job = client.query(sql, job_config=job_config)
        results = list(query_job.result())
        
        if results and results[0].count > 0:
            row = results[0]
            return jsonify({
                "count": row.count,
                "mean": row.mean,
                "std_dev": row.std_dev,
                "variance": row.variance,
                "min": row.min_value,
                "max": row.max_value,
                "q25": row.q25,
                "median": row.median,
                "q75": row.q75,
                "skewness": row.skewness,
                "kurtosis": row.kurtosis
            }), 200
        
        return jsonify({
            "count": 0,
            "mean": None,
            "std_dev": None,
            "variance": None,
            "min": None,
            "max": None,
            "q25": None,
            "median": None,
            "q75": None,
            "skewness": None,
            "kurtosis": None
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("BACKEND_PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)