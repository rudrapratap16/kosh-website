import streamlit as st
import pandas as pd
import numpy as np
from utils.api_client import get_filters, get_data, get_weather_filters, get_weather_data
from datetime import datetime

st.set_page_config(page_title="Environmental Data Dashboard", layout="wide")

# Theme toggle in the top right
col1, col2 = st.columns([6, 1])
with col2:
    # Use a button with just an icon
    if 'theme' not in st.session_state:
        st.session_state.theme = True  # Default to dark mode
    
    # Display icon based on current theme
    icon = "🌙" if st.session_state.theme else "☀️"
    
    # Custom CSS for subtle icon button
    st.markdown("""
        <style>
        .theme-button button {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            font-size: 20px !important;
            opacity: 0.5 !important;
        }
        .theme-button button:hover {
            opacity: 1 !important;
            background-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Use markdown container for custom styling
    with st.container():
        st.markdown('<div class="theme-button">', unsafe_allow_html=True)
        if st.button(icon, key="theme_toggle"):
            st.session_state.theme = not st.session_state.theme
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    theme = st.session_state.theme

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
        /* Dataframe styling */
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
        /* Dataframe styling */
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

# Load filters
with st.spinner("Loading filter values..."):
    filters = get_filters()

if not filters:
    st.error("Could not load filter values from backend.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
outfall_options = [""] + filters.get("outfall_numbers", [])

# Add Precipitation and Temperature to parameter options
parameter_options = [""] + filters.get("parameter_descriptions", []) + ["Precipitation", "Temperature"]

selected_outfall = st.sidebar.selectbox("Outfall", outfall_options, index=0)
selected_parameter = st.sidebar.selectbox("Parameter", parameter_options, index=0)

# Dynamically adjust Statistical Base and Unit based on parameter selection
if selected_parameter == "Precipitation":
    # For Precipitation
    selected_base = "Daily Total"
    st.sidebar.text_input("Base", value=selected_base, disabled=True)
    selected_unit = "inches"
    st.sidebar.text_input("Unit", value=selected_unit, disabled=True)
elif selected_parameter == "Temperature":
    # For Temperature
    temp_base_options = ["Daily Max", "Daily Min", "Daily Avg"]
    selected_base = st.sidebar.selectbox("Base", temp_base_options, index=0)
    selected_unit = "Fahrenheit"
    st.sidebar.text_input("Unit", value=selected_unit, disabled=True)
else:
    # For regular NPDES parameters
    base_options = [""] + filters.get("statistical_bases", [])
    unit_options = [""] + filters.get("dmr_value_units", [])
    selected_base = st.sidebar.selectbox("Base", base_options, index=0)
    selected_unit = st.sidebar.selectbox("Unit", unit_options, index=0)

# Date range inputs (optional)
st.sidebar.markdown("### Date range")
start_date = st.sidebar.date_input(
    "Start date", 
    value=None, 
    min_value=datetime(2000, 1, 1), 
    max_value=datetime.today(),
    key="start_date"
)
end_date = st.sidebar.date_input(
    "End date", 
    value=None, 
    min_value=datetime(2000, 1, 1), 
    max_value=datetime.today(),
    key="end_date"
)

# Convert to string format (YYYY-MM-DD) before passing to API
start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None
end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

if st.sidebar.button("Apply Filter"):
    # Determine which API to call based on parameter selection
    if selected_parameter in ["Precipitation", "Temperature"]:
        # Fetch weather data
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(
                station_id="USC00467342",  # Hardcoded station ID
                parent_facility_id=None,
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
                df = df.sort_values("date")
            except Exception:
                pass

        # Convert numeric columns
        numeric_cols = ["tavg_fahrenheit", "tmax_fahrenheit", "tmin_fahrenheit", "prcp_inches", "snow_inches", "snwd_inches"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Apply date filter if provided
        if start_date and "date" in df.columns:
            df = df[df["date"] >= pd.Timestamp(start_date)]
        if end_date and "date" in df.columns:
            df = df[df["date"] <= pd.Timestamp(end_date)]

        if selected_parameter == "Precipitation":
            # Plot Precipitation
            st.subheader("Precipitation over Time")
            if "prcp_inches" in df.columns and df["prcp_inches"].notnull().any():
                plot_df = df.dropna(subset=["prcp_inches"])
                
                if "date" in plot_df.columns and not plot_df["date"].isnull().all():
                    chart_data = plot_df.set_index("date")[["prcp_inches"]]
                    chart_data.columns = ["Precipitation (inches)"]
                    st.line_chart(chart_data)
                else:
                    st.line_chart(plot_df["prcp_inches"])
            else:
                st.info("No precipitation data available to plot.")

            # Statistical Analysis for Precipitation
            if "prcp_inches" in df.columns and df["prcp_inches"].notnull().any():
                st.subheader("Statistical Analysis")
                numeric_series = pd.to_numeric(df["prcp_inches"], errors="coerce").dropna()

                if len(numeric_series) > 0:
                    stats = {
                        "Minimum (inches)": numeric_series.min(),
                        "Average (inches)": numeric_series.mean(),
                        "Median (inches)": numeric_series.median(),
                        "Maximum (inches)": numeric_series.max(),
                        "Standard Deviation (inches)": numeric_series.std(),
                        "Variance (inches)": numeric_series.var(),
                        "Kurtosis": numeric_series.kurtosis(),
                        "Skewness": numeric_series.skew(),
                    }

                    stats_df = pd.DataFrame(stats, index=["Value"]).T
                    st.table(stats_df)
                else:
                    st.info("No numeric values available for statistical analysis.")

        elif selected_parameter == "Temperature":
            # Plot Temperature based on selected base (Tmax, Tmin, Tavg)
            st.subheader(f"Temperature ({selected_base}) over Time")
            
            temp_col_map = {
                "Daily Max": "tmax_fahrenheit",
                "Daily Min": "tmin_fahrenheit",
                "Daily Avg": "tavg_fahrenheit"
            }
            
            temp_col = temp_col_map.get(selected_base)
            
            if temp_col in df.columns and df[temp_col].notnull().any():
                plot_df = df.dropna(subset=[temp_col])
                
                if "date" in plot_df.columns and not plot_df["date"].isnull().all():
                    chart_data = plot_df.set_index("date")[[temp_col]]
                    chart_data.columns = [f"{selected_base} (°F)"]
                    st.line_chart(chart_data)
                else:
                    st.line_chart(plot_df[temp_col])
            else:
                st.info(f"No {selected_base} temperature data available to plot.")

            # Statistical Analysis for Temperature
            if temp_col in df.columns and df[temp_col].notnull().any():
                st.subheader("Statistical Analysis")
                numeric_series = pd.to_numeric(df[temp_col], errors="coerce").dropna()

                if len(numeric_series) > 0:
                    stats = {
                        "Minimum (°F)": numeric_series.min(),
                        "Average (°F)": numeric_series.mean(),
                        "Median (°F)": numeric_series.median(),
                        "Maximum (°F)": numeric_series.max(),
                        "Standard Deviation (°F)": numeric_series.std(),
                        "Variance (°F)": numeric_series.var(),
                        "Kurtosis": numeric_series.kurtosis(),
                        "Skewness": numeric_series.skew(),
                    }

                    stats_df = pd.DataFrame(stats, index=["Value"]).T
                    st.table(stats_df)
                else:
                    st.info("No numeric values available for statistical analysis.")

        # Raw data
        st.subheader("Raw Data")
        st.dataframe(df)

    else:
        # Regular NPDES data
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
                chart_data = plot_df.set_index("monitoring_period_date")[["dmr_value"]]
                
                # Rename column with unit if available
                if selected_unit:
                    chart_data.columns = [f"DMR Value ({selected_unit})"]
                else:
                    chart_data.columns = ["DMR Value"]
                
                st.line_chart(chart_data)
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
                    f"Minimum{unit_str}": numeric_series.min(),
                    f"Average{unit_str}": numeric_series.mean(),
                    f"Median{unit_str}": numeric_series.median(),
                    f"Maximum{unit_str}": numeric_series.max(),
                    f"Standard Deviation{unit_str}": numeric_series.std(),
                    f"Variance{unit_str}": numeric_series.var(),
                    "Kurtosis": numeric_series.kurtosis(),
                    "Skewness": numeric_series.skew(),
                }

                stats_df = pd.DataFrame(stats, index=["Value"]).T
                st.table(stats_df)
            else:
                st.info("No numeric values available for statistical analysis.")
        else:
            st.info("No numeric dmr_value column found for statistical analysis.")

else:
    st.info("Set filters and click 'Apply Filter' to fetch data.")