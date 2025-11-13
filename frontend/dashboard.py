import streamlit as st
import pandas as pd
import numpy as np
from utils.api_client import get_filters, get_data, get_weather_filters, get_weather_data
from datetime import datetime

st.set_page_config(page_title="Environmental Data Dashboard", layout="wide")

# Theme toggle icon at the top
col1, col2 = st.columns([20, 1])
with col2:
    if st.session_state.get('theme', True):
        if st.button("☀️", key="theme_toggle"):
            st.session_state['theme'] = False
            st.rerun()
        theme = True
    else:
        if st.button("🌙", key="theme_toggle"):
            st.session_state['theme'] = True
            st.rerun()
        theme = False

# Apply custom CSS based on theme
if theme:
    # Dark theme
    st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
        }
        .stSidebar {
            background-color: #1a1a1a;
        }
        header[data-testid="stHeader"] {
            background-color: #000000;
        }
        .stMarkdown, .stText, p, span, label {
            color: #FFFFFF !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }
        .stSelectbox label, .stRadio label, .stCheckbox label {
            color: #FFFFFF !important;
        }
        /* Dropdown styling */
        div[data-baseweb="select"] {
            background-color: #1a1a1a !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
            border-color: #444444 !important;
        }
        /* Dropdown menu */
        div[role="listbox"] {
            background-color: #1a1a1a !important;
        }
        div[role="option"] {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
        }
        div[role="option"]:hover {
            background-color: #333333 !important;
        }
        /* Date input styling */
        .stDateInput label {
            color: #FFFFFF !important;
        }
        .stDateInput input {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
            border-color: #444444 !important;
        }
        /* Button styling */
        .stButton button {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
            border: 1px solid #444444 !important;
        }
        .stButton button:hover {
            background-color: #333333 !important;
            border-color: #666666 !important;
        }
        # Dataframe styling */
        .stDataFrame {
            background-color: #1a1a1a !important;
        }
        .stDataFrame [data-testid="stDataFrameResizable"] {
            background-color: #1a1a1a !important;
        }
        .stDataFrame div[data-testid="stDataFrameResizable"] > div {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
        }
        .stDataFrame table {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
        }
        /* Chart/Graph styling */
        .stLineChart, .stAreaChart, .stBarChart {
            background-color: #1a1a1a !important;
        }
        canvas {
            background-color: #1a1a1a !important;
        }
        /* Table styling */
        table {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
            border: 1px solid #444444 !important;
        }
        thead tr th {
            background-color: #2a2a2a !important;
            color: #FFFFFF !important;
            border: 1px solid #444444 !important;
        }
        tbody tr td {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
            border: 1px solid #444444 !important;
        }
        /* Toggle styling */
        .stCheckbox, label[data-baseweb="checkbox"] {
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    # Light theme
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        .stSidebar {
            background-color: #F0F2F6;
        }
        header[data-testid="stHeader"] {
            background-color: #FFFFFF;
        }
        .stMarkdown, .stText, p, span, label {
            color: #000000 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
        }
        .stSelectbox label, .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }
        /* Dropdown styling */
        div[data-baseweb="select"] {
            background-color: #FFFFFF !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-color: #CCCCCC !important;
        }
        /* Dropdown menu */
        div[role="listbox"] {
            background-color: #FFFFFF !important;
        }
        div[role="option"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        div[role="option"]:hover {
            background-color: #F0F0F0 !important;
        }
        /* Date input styling */
        .stDateInput label {
            color: #000000 !important;
        }
        .stDateInput input {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border-color: #CCCCCC !important;
        }
        /* Button styling */
        .stButton button {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #CCCCCC !important;
        }
        .stButton button:hover {
            background-color: #F0F0F0 !important;
            border-color: #999999 !important;
        }
        # Dataframe styling */
        .stDataFrame {
            background-color: #FFFFFF !important;
        }
        .stDataFrame [data-testid="stDataFrameResizable"] {
            background-color: #FFFFFF !important;
        }
        .stDataFrame div[data-testid="stDataFrameResizable"] > div {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        .stDataFrame table {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        /* Chart/Graph styling */
        .stLineChart, .stAreaChart, .stBarChart {
            background-color: #FFFFFF !important;
        }
        canvas {
            background-color: #FFFFFF !important;
        }
        /* Table styling */
        table {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #CCCCCC !important;
        }
        thead tr th {
            background-color: #F0F0F0 !important;
            color: #000000 !important;
            border: 1px solid #CCCCCC !important;
        }
        tbody tr td {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #CCCCCC !important;
        }
        /* Toggle styling */
        .stCheckbox, label[data-baseweb="checkbox"] {
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Load filter values
with st.spinner("Loading filter values..."):
    filters = get_filters()
    weather_filters = get_weather_filters()

if not filters:
    st.error("Could not load filter values from backend.")
    st.stop()

# Sidebar filters
st.sidebar.header("Data Filters")

# Parameter Description dropdown with Precipitation Data option
parameter_options = ["", "Precipitation Data"] + filters.get("parameter_descriptions", [])
selected_parameter = st.sidebar.selectbox("Parameter", parameter_options, index=0)

# Determine if precipitation data is selected
is_precipitation = (selected_parameter == "Precipitation Data")

if is_precipitation:
    # Show precipitation-specific filters
    if not weather_filters:
        st.error("Could not load precipitation filter values from backend.")
        st.stop()
    
    station_options = [""] + weather_filters.get("station_ids", [])
    facility_options = [""] + weather_filters.get("parent_facility_ids", [])

    selected_station = st.sidebar.selectbox("Station ID", station_options, index=0)
    selected_facility = st.sidebar.selectbox("Parent Facility ID", facility_options, index=0)

    # Parameter selection for plotting
    st.sidebar.markdown("### Parameters to Plot")
    plot_tavg = st.sidebar.checkbox("Average Temperature (°F)", value=True)
    plot_tmax = st.sidebar.checkbox("Max Temperature (°F)", value=False)
    plot_tmin = st.sidebar.checkbox("Min Temperature (°F)", value=False)
    plot_prcp = st.sidebar.checkbox("Precipitation (inches)", value=True)
    plot_snow = st.sidebar.checkbox("Snow (inches)", value=False)
    plot_snwd = st.sidebar.checkbox("Snow Depth (inches)", value=False)

else:
    # Show NPDES-specific filters
    outfall_options = [""] + filters.get("outfall_numbers", [])
    base_options = [""] + filters.get("statistical_bases", [])
    unit_options = [""] + filters.get("dmr_value_units", [])

    selected_outfall = st.sidebar.selectbox("Outfall", outfall_options, index=0)
    selected_base = st.sidebar.selectbox("Base", base_options, index=0)
    selected_unit = st.sidebar.selectbox("Unit", unit_options, index=0)

    # Date range inputs (optional)
    st.sidebar.markdown("### Date range")
    start_date = st.sidebar.date_input(
        "Start date", 
        value=None, 
        min_value=datetime(2000, 1, 1), 
        max_value=datetime.today(),
        format="DD/MM/YYYY",
        key="npdes_start"
    )
    end_date = st.sidebar.date_input(
        "End date", 
        value=None, 
        min_value=datetime(2000, 1, 1), 
        max_value=datetime.today(),
        format="DD/MM/YYYY",
        key="npdes_end"
    )

# Apply Filter button
if st.sidebar.button("Apply Filter"):
    if is_precipitation:
        # Handle Precipitation Data
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(
                station_id=selected_station or None,
                parent_facility_id=selected_facility or None,
                limit=5000
            )

        if weather_data is None:
            st.error("Failed to fetch weather data.")
            st.stop()

        if len(weather_data) == 0:
            st.info("No rows match the selected filters.")
            st.stop()

        df = pd.DataFrame(weather_data)

        # Parse date column
        if "date" in df.columns:
            try:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
            except Exception:
                pass

        # Convert numeric columns
        numeric_cols = ["tavg_fahrenheit", "tmax_fahrenheit", "tmin_fahrenheit", "prcp_inches", "snow_inches", "snwd_inches"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Plot selected parameters
        st.subheader("Weather Parameters Over Time")
        
        chart_data = df[["date"]].copy() if "date" in df.columns else df.copy()
        
        if plot_tavg and "tavg_fahrenheit" in df.columns:
            chart_data["Avg Temp (°F)"] = df["tavg_fahrenheit"]
        if plot_tmax and "tmax_fahrenheit" in df.columns:
            chart_data["Max Temp (°F)"] = df["tmax_fahrenheit"]
        if plot_tmin and "tmin_fahrenheit" in df.columns:
            chart_data["Min Temp (°F)"] = df["tmin_fahrenheit"]
        if plot_prcp and "prcp_inches" in df.columns:
            chart_data["Precipitation (in)"] = df["prcp_inches"]
        if plot_snow and "snow_inches" in df.columns:
            chart_data["Snow (in)"] = df["snow_inches"]
        if plot_snwd and "snwd_inches" in df.columns:
            chart_data["Snow Depth (in)"] = df["snwd_inches"]

        if "date" in chart_data.columns and len(chart_data.columns) > 1:
            chart_data = chart_data.set_index("date").sort_index()
            st.line_chart(chart_data)
        else:
            st.info("Select at least one parameter to plot.")

        # Raw data
        st.subheader("Raw Data")
        st.dataframe(df)

    else:
        # Handle NPDES Data
        # Convert to string format (YYYY-MM-DD) before passing to API
        start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None
        end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

        with st.spinner("Fetching data..."):
            data = get_data(
                outfall=selected_outfall or None,
                parameter=selected_parameter or None,
                base=selected_base or None,
                unit=selected_unit or None,
                start_date=start_date_str,
                end_date=end_date_str,
                limit=5000
            )

        if data is None:
            st.error("Failed to fetch data.")
            st.stop()

        if len(data) == 0:
            st.info("No rows match the selected filters.")
            st.stop()

        df = pd.DataFrame(data)

        # Try parsing monitoring_period_date to datetime
        if "monitoring_period_date" in df.columns:
            try:
                df["monitoring_period_date"] = pd.to_datetime(df["monitoring_period_date"], errors="coerce")
            except Exception:
                pass

        # Plot DMR Value vs Date
        if selected_parameter:
            st.subheader(f"{selected_parameter} over Time")
        else:
            st.subheader("DMR Value over Time")
        if "dmr_value" in df.columns and df["dmr_value"].notnull().any():
            plot_df = df.dropna(subset=["dmr_value"])
            
            # If date is parsed, use it, otherwise use index
            if "monitoring_period_date" in plot_df.columns and not plot_df["monitoring_period_date"].isnull().all():
                plot_df = plot_df.sort_values("monitoring_period_date")
                plot_df = plot_df.set_index("monitoring_period_date")
                st.line_chart(plot_df["dmr_value"])
            else:
                st.line_chart(plot_df["dmr_value"])
        else:
            st.info("No numeric dmr_value to plot.")
        
        # Raw data
        st.subheader("Raw Data")
        st.dataframe(df)

        # Statistical Analysis Table
        if "dmr_value" in df.columns and df["dmr_value"].notnull().any():
            st.subheader("Statistical Analysis")

            numeric_series = pd.to_numeric(df["dmr_value"], errors="coerce").dropna()

            if len(numeric_series) > 0:
                # Get the unit for display
                unit_str = f" ({selected_unit})" if selected_unit else ""
                
                stats = {
                    "Metric": [
                        f"Minimum{unit_str}",
                        f"Average{unit_str}",
                        f"Median{unit_str}",
                        f"Maximum{unit_str}",
                        f"Standard Deviation{unit_str}",
                        f"Variance{unit_str}",
                        "Kurtosis",
                        "Skewness"
                    ],
                    "Value": [
                        numeric_series.min(),
                        numeric_series.mean(),
                        numeric_series.median(),
                        numeric_series.max(),
                        numeric_series.std(),
                        numeric_series.var(),
                        numeric_series.kurtosis(),
                        numeric_series.skew()
                    ]
                }

                stats_df = pd.DataFrame(stats)
                st.dataframe(stats_df, hide_index=True)
            else:
                st.info("No numeric values available for statistical analysis.")
        else:
            st.info("No dmr_value column found for statistical analysis.")
else:
    st.info("Set filters and click 'Apply Filter' to fetch data.")