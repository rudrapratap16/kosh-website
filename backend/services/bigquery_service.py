from google.cloud import bigquery
from config import PROJECT_ID, DATASET, TABLE

CLIENT = bigquery.Client(project=PROJECT_ID)

# Fetches filters
def fetch_filters():
    """
    Returns a dict of unique values for the UI dropdowns of the ui.
    """
    table_ref = f"{PROJECT_ID}.{DATASET}.{TABLE}"

    queries = {
        "outfall_numbers": f"SELECT DISTINCT outfall_number FROM `{table_ref}` WHERE outfall_number IS NOT NULL ORDER BY outfall_number",
        "parameter_descriptions": f"SELECT DISTINCT parameter_description FROM `{table_ref}` WHERE parameter_description IS NOT NULL ORDER BY parameter_description",
        "statistical_bases": f"SELECT DISTINCT statistical_base FROM `{table_ref}` WHERE statistical_base IS NOT NULL ORDER BY statistical_base",
        "dmr_value_units": f"SELECT DISTINCT dmr_value_unit FROM `{table_ref}` WHERE dmr_value_unit IS NOT NULL ORDER BY dmr_value_unit",
    }

    result = {}
    for key, q in queries.items():
        job = CLIENT.query(q)
        rows = [row[0] for row in job.result() if row[0] is not None]
        result[key] = rows

    return result

def fetch_data(params):
    """
    Fetches NPDES data from BigQuery with dynamic filters.

    params: dict with keys
        - outfall (str)
        - parameter (str)
        - base (str)
        - unit (str)
        - start_date (YYYY-MM-DD string)
        - end_date (YYYY-MM-DD string)
        - limit (int)

    Returns:
        - List of dicts with rows
    """
    table_ref = f"{PROJECT_ID}.{DATASET}.{TABLE}"
    where_clauses = []
    query_params = []

    # Optional filters
    if params.get("outfall"):
        where_clauses.append("outfall_number = @outfall")
        query_params.append(bigquery.ScalarQueryParameter("outfall", "STRING", params["outfall"]))

    if params.get("parameter"):
        where_clauses.append("parameter_description = @parameter")
        query_params.append(bigquery.ScalarQueryParameter("parameter", "STRING", params["parameter"]))

    if params.get("base"):
        where_clauses.append("statistical_base = @base")
        query_params.append(bigquery.ScalarQueryParameter("base", "STRING", params["base"]))

    if params.get("unit"):
        where_clauses.append("dmr_value_unit = @unit")
        query_params.append(bigquery.ScalarQueryParameter("unit", "STRING", params["unit"]))

    # Date filters (convert MM/DD/YYYY to DATE for comparison)
    if params.get("start_date"):
        where_clauses.append("PARSE_DATE('%m/%d/%Y', monitoring_period_date) >= @start_date")
        query_params.append(bigquery.ScalarQueryParameter("start_date", "DATE", params["start_date"]))

    if params.get("end_date"):
        where_clauses.append("PARSE_DATE('%m/%d/%Y', monitoring_period_date) <= @end_date")
        query_params.append(bigquery.ScalarQueryParameter("end_date", "DATE", params["end_date"]))

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    # Limit
    limit = params.get("limit", 1000)
    query_params.append(bigquery.ScalarQueryParameter("limit", "INT64", limit))

    # Final SQL
    sql = f"""
    SELECT
        monitoring_period_date,
        SAFE_CAST(dmr_value AS FLOAT64) AS dmr_value,
        outfall_number,
        parameter_description,
        statistical_base,
        dmr_value_unit,
        npdes_permit_number,
        dmr_comments,
        source_file_name,
        ingestion_timestamp
    FROM `{table_ref}`
    {where_sql}
    ORDER BY PARSE_DATE('%m/%d/%Y', monitoring_period_date)
    LIMIT @limit
    """

    # Execute query
    job_config = bigquery.QueryJobConfig(query_parameters=query_params)
    query_job = CLIENT.query(sql, job_config=job_config)
    rows = []

    for row in query_job.result():
        rows.append({
            "monitoring_period_date": row.monitoring_period_date,
            "dmr_value": row.dmr_value,
            "outfall_number": row.outfall_number,
            "parameter_description": row.parameter_description,
            "statistical_base": row.statistical_base,
            "dmr_value_unit": row.dmr_value_unit,
            "npdes_permit_number": row.npdes_permit_number,
            "dmr_comments": row.dmr_comments,
            "source_file_name": row.source_file_name,
            "ingestion_timestamp": row.ingestion_timestamp.isoformat() if row.ingestion_timestamp else None
        })

    return rows

def fetch_weather_filters():
    """
    Returns unique values for dropdowns in the precipitation_weather table.
    """
    table_ref = f"{PROJECT_ID}.{DATASET}.precipitation_weather"

    queries = {
        "station_ids": f"SELECT DISTINCT station_id FROM `{table_ref}` WHERE station_id IS NOT NULL ORDER BY station_id",
        "parent_facility_ids": f"SELECT DISTINCT parent_facility_id FROM `{table_ref}` WHERE parent_facility_id IS NOT NULL ORDER BY parent_facility_id",
    }

    result = {}
    for key, q in queries.items():
        job = CLIENT.query(q)
        rows = [row[0] for row in job.result() if row[0] is not None]
        result[key] = rows

    return result


def fetch_weather_data(params):
    """
    Fetches weather data from BigQuery with dynamic filters.

    params: dict with keys
        - station_id (str)
        - parent_facility_id (str)
        - start_date (YYYY-MM-DD string)
        - end_date (YYYY-MM-DD string)
        - limit (int)
    """
    table_ref = f"{PROJECT_ID}.{DATASET}.precipitation_weather"
    where_clauses = []
    query_params = []

    # Optional filters
    if params.get("station_id"):
        where_clauses.append("station_id = @station_id")
        query_params.append(bigquery.ScalarQueryParameter("station_id", "STRING", params["station_id"]))

    if params.get("parent_facility_id"):
        where_clauses.append("parent_facility_id = @parent_facility_id")
        query_params.append(bigquery.ScalarQueryParameter("parent_facility_id", "STRING", params["parent_facility_id"]))

    # Date filters
    if params.get("start_date"):
        where_clauses.append("PARSE_DATE('%m/%d/%Y', date) >= @start_date")

    if params.get("start_date"):
        where_clauses.append("PARSE_DATE('%Y-%m-%d', date) >= @start_date")


    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    # Limit
    limit = params.get("limit", 1000)
    query_params.append(bigquery.ScalarQueryParameter("limit", "INT64", limit))

    sql = f"""
    SELECT
        date,
        SAFE_CAST(tavg_fahrenheit AS FLOAT64) AS tavg_fahrenheit,
        SAFE_CAST(tmax_fahrenheit AS FLOAT64) AS tmax_fahrenheit,
        SAFE_CAST(tmin_fahrenheit AS FLOAT64) AS tmin_fahrenheit,
        SAFE_CAST(prcp_inches AS FLOAT64) AS prcp_inches,
        SAFE_CAST(snow_inches AS FLOAT64) AS snow_inches,
        SAFE_CAST(snwd_inches AS FLOAT64) AS snwd_inches,
        station_id,
        parent_facility_id,
        source_file_name,
        ingestion_timestamp
    FROM `{table_ref}`
    {where_sql}
    ORDER BY PARSE_DATE('%Y-%m-%d', date)
    LIMIT @limit
    """

    job_config = bigquery.QueryJobConfig(query_parameters=query_params)
    query_job = CLIENT.query(sql, job_config=job_config)
    rows = []

    for row in query_job.result():
        rows.append({
            "date": row.date,
            "tavg_fahrenheit": row.tavg_fahrenheit,
            "tmax_fahrenheit": row.tmax_fahrenheit,
            "tmin_fahrenheit": row.tmin_fahrenheit,
            "prcp_inches": row.prcp_inches,
            "snow_inches": row.snow_inches,
            "snwd_inches": row.snwd_inches,
            "station_id": row.station_id,
            "parent_facility_id": row.parent_facility_id,
            "source_file_name": row.source_file_name,
            "ingestion_timestamp": row.ingestion_timestamp.isoformat() if row.ingestion_timestamp else None
        })

    return rows
