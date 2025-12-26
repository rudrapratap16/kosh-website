from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import bigquery
from google.cloud import firestore
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt
import datetime
from functools import wraps
from config import PROJECT_ID, DATASET, FRONTEND_URL
import os

# Create Flask app at top level
app = Flask(__name__)

CORS(app, 
     origins=[
         FRONTEND_URL,
         "http://localhost:5173",
         "http://127.0.0.1:5173",
         "http://localhost:8080",
         "http://127.0.0.1:8080",
     ],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE"],
     supports_credentials=True,
     max_age=3600)


JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
JWT_EXP_HOURS = 24

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
FIRESTORE_DATABASE = os.environ.get('FIRESTORE_DATABASE')
db = firestore.Client(project=PROJECT_ID, database=FIRESTORE_DATABASE)

client = bigquery.Client(project=PROJECT_ID)
npdes_table_ref = f"{PROJECT_ID}.{DATASET}.npdes"
weather_table_ref = f"{PROJECT_ID}.{DATASET}.prep_temp_snow"

def save_user_to_firestore(user_info):
    """Save or update user information in Firestore"""
    try:
        users_ref = db.collection('users')
        user_doc_ref = users_ref.document(user_info['sub'])
        user_doc = user_doc_ref.get()
        
        if user_doc.exists:
            user_doc_ref.update({
                'email': user_info['email'],
                'name': user_info['name'],
                'picture': user_info['picture'],
                'last_login': firestore.SERVER_TIMESTAMP
            })
            print(f"✓ Updated existing user: {user_info['email']}")
        else:
            user_doc_ref.set({
                'email': user_info['email'],
                'name': user_info['name'],
                'picture': user_info['picture'],
                'google_id': user_info['sub'],
                'created_at': firestore.SERVER_TIMESTAMP,
                'last_login': firestore.SERVER_TIMESTAMP
            })
            print(f"✓ Created new user: {user_info['email']}")
            
    except Exception as e:
        print(f"⚠ Warning: Could not save user to Firestore: {str(e)}")
        pass

def create_jwt_token(user_info):
    """Create JWT token with user information"""
    payload = {
        'email': user_info['email'],
        'name': user_info.get('name', ''),
        'picture': user_info.get('picture', ''),
        'sub': user_info['sub'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXP_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token):
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            token = auth_header.split(' ')[1]
            payload = verify_jwt_token(token)
            
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            request.user = payload
            return f(*args, **kwargs)
            
        except IndexError:
            return jsonify({'error': 'Invalid authorization header format'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    
    return decorated_function

# ============= AUTH ROUTES =============

@app.route("/api/auth/google", methods=["POST"])
def google_auth():
    """
    Verify Google OAuth token and return JWT
    Expects: { "token": "google_id_token" }
    Returns: { "token": "jwt_token", "user": {...} }
    """
    # Handle preflight
    if request.method == "OPTIONS":
        return '', 204
    
    try:
        data = request.get_json()
        google_token = data.get('token')
        
        if not google_token:
            return jsonify({'error': 'No token provided'}), 400
        
        print(f"Received token: {google_token[:50]}...")
        print(f"Using Client ID: {GOOGLE_CLIENT_ID}")
        
        # Verify Google token
        idinfo = id_token.verify_oauth2_token(
            google_token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        print(f"Token verified successfully for: {idinfo.get('email')}")
        
        user_info = {
            'email': idinfo['email'],
            'name': idinfo.get('name', ''),
            'picture': idinfo.get('picture', ''),
            'sub': idinfo['sub']
        }
        
        save_user_to_firestore(user_info)
        jwt_token = create_jwt_token(user_info)
        
        return jsonify({
            'token': jwt_token,
            'user': user_info
        }), 200
        
    except ValueError as e:
        print(f"ValueError in google_auth: {str(e)}")
        return jsonify({'error': f'Invalid Google token: {str(e)}'}), 401
    except Exception as e:
        print(f"Exception in google_auth: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Authentication failed: {str(e)}'}), 500

@app.route("/api/auth/verify", methods=["GET"])
@require_auth
def verify_token():
    """Verify if current JWT token is valid"""
    if request.method == "OPTIONS":
        return '', 204
    
    return jsonify({
        'valid': True,
        'user': request.user
    }), 200

@app.route("/api/admin/users", methods=["GET"])
@require_auth
def get_all_users():
    """Get all users from Firestore"""
    if request.method == "OPTIONS":
        return '', 204
    
    try:
        users_ref = db.collection('users')
        users = users_ref.stream()
        
        user_list = []
        for user in users:
            user_data = user.to_dict()
            if 'created_at' in user_data and user_data['created_at']:
                user_data['created_at'] = user_data['created_at'].isoformat()
            if 'last_login' in user_data and user_data['last_login']:
                user_data['last_login'] = user_data['last_login'].isoformat()
            user_list.append(user_data)
        
        return jsonify({
            'users': user_list,
            'total': len(user_list)
        }), 200
        
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/api/filters/initial", methods=["GET"])
@require_auth
def get_initial_filters():
    """
    Get all unique values for dropdowns on initial load
    Combines NPDES and Weather data
    """
    if request.method == "OPTIONS":
        return '', 204
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
@require_auth
def get_cascading_filters():
    """
    Cascading filters that include both NPDES and Weather data
    Weather parameters are always available regardless of outfall/permit selection
    """
    if request.method == "OPTIONS":
        return '', 204
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
@require_auth
def get_combined_data():
    """
    Fetches data from both NPDES and Weather tables
    Weather data appears regardless of permit/outfall selection
    """
    if request.method == "OPTIONS":
        return '', 204
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
@require_auth
def get_combined_statistics():
    """
    Get statistics for combined NPDES and Weather data
    """
    if request.method == "OPTIONS":
        return '', 204
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