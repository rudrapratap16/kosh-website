import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.api_client import get_filters, get_data, get_weather_filters, get_weather_data
from datetime import datetime

st.set_page_config(page_title="Environmental Data Dashboard", layout="wide")

# Theme toggle in the top right
col1, col2 = st.columns([6, 1])
with col1:
    st.title("💧 Environmental Data Dashboard")
with col2:
    theme = st.toggle("🌙 Dark Mode", value=True)

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

# Data source selector
data_source = st.radio("Select Data Source", ["NPDES Data", "Precipitation Data"], horizontal=True)

if data_source == "NPDES Data":
    # st.subheader("NPDES Monitoring Data")
    
    with st.spinner("Loading filter values..."):
        filters = get_filters()

    if not filters:
        st.error("Could not load filter values from backend.")
        st.stop()

    # Sidebar filters
    st.sidebar.header("NPDES Filters")
    outfall_options = [""] + filters.get("outfall_numbers", [])
    parameter_options = [""] + filters.get("parameter_descriptions", [])
    base_options = [""] + filters.get("statistical_bases", [])
    unit_options = [""] + filters.get("dmr_value_units", [])

    selected_outfall = st.sidebar.selectbox("Outfall Number", outfall_options, index=0)
    selected_parameter = st.sidebar.selectbox("Parameter Description", parameter_options, index=0)
    selected_base = st.sidebar.selectbox("Statistical Base", base_options, index=0)
    selected_unit = st.sidebar.selectbox("DMR Value Unit", unit_options, index=0)

    # Date range inputs (optional)
    st.sidebar.markdown("### Date range")
    start_date = st.sidebar.date_input(
        "Start date", 
        value=None, 
        min_value=datetime(2000, 1, 1), 
        max_value=datetime.today(),
        key="npdes_start"
    )
    end_date = st.sidebar.date_input(
        "End date", 
        value=None, 
        min_value=datetime(2000, 1, 1), 
        max_value=datetime.today(),
        key="npdes_end"
    )

    # Convert to string format (YYYY-MM-DD) before passing to API
    start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    if st.sidebar.button("Apply NPDES Filter"):
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
            
            # Determine y-axis label
            y_label = f"DMR Value ({selected_unit})" if selected_unit else "DMR Value"
            
            # If date is parsed, use it, otherwise use index
            if "monitoring_period_date" in plot_df.columns and not plot_df["monitoring_period_date"].isnull().all():
                plot_df = plot_df.sort_values("monitoring_period_date")
                
                # Create plotly figure
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=plot_df["monitoring_period_date"],
                    y=plot_df["dmr_value"],
                    mode='lines+markers',
                    name=y_label,
                    line=dict(color='#636EFA')
                ))
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title=y_label,
                    plot_bgcolor='#1a1a1a' if theme else '#FFFFFF',
                    paper_bgcolor='#1a1a1a' if theme else '#FFFFFF',
                    font=dict(color='#FFFFFF' if theme else '#000000'),
                    xaxis=dict(
                        gridcolor='#444444' if theme else '#E0E0E0',
                        linecolor='#444444' if theme else '#CCCCCC',
                        color='#FFFFFF' if theme else '#000000'
                    ),
                    yaxis=dict(
                        gridcolor='#444444' if theme else '#E0E0E0',
                        linecolor='#444444' if theme else '#CCCCCC',
                        color='#FFFFFF' if theme else '#000000'
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Create plotly figure with index
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=plot_df["dmr_value"],
                    mode='lines+markers',
                    name=y_label,
                    line=dict(color='#636EFA')
                ))
                
                fig.update_layout(
                    xaxis_title="Index",
                    yaxis_title=y_label,
                    plot_bgcolor='#1a1a1a' if theme else '#FFFFFF',
                    paper_bgcolor='#1a1a1a' if theme else '#FFFFFF',
                    font=dict(color='#FFFFFF' if theme else '#000000'),
                    xaxis=dict(
                        gridcolor='#444444' if theme else '#E0E0E0',
                        linecolor='#444444' if theme else '#CCCCCC',
                        color='#FFFFFF' if theme else '#000000'
                    ),
                    yaxis=dict(
                        gridcolor='#444444' if theme else '#E0E0E0',
                        linecolor='#444444' if theme else '#CCCCCC',
                        color='#FFFFFF' if theme else '#000000'
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
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
        st.info("Set filters and click 'Apply NPDES Filter' to fetch data.")

else:  # Precipitation Data
    st.subheader("Precipitation Weather Data")
    
    with st.spinner("Loading precipitation filters..."):
        weather_filters = get_weather_filters()

    if not weather_filters:
        st.error("Could not load precipitation filter values from backend.")
        st.stop()

    # Sidebar filters for precipitation
    st.sidebar.header("Precipitation Filters")
    
    station_options = [""] + weather_filters.get("station_ids", [])
    facility_options = [""] + weather_filters.get("parent_facility_ids", [])

    selected_station = st.sidebar.selectbox("Station ID", station_options, index=0)
    selected_facility = st.sidebar.selectbox("Parent Facility ID", facility_options, index=0)

    # Parameter selection
    st.sidebar.markdown("### Parameters to Plot")
    plot_tavg = st.sidebar.checkbox("Average Temperature (°F)", value=True)
    plot_tmax = st.sidebar.checkbox("Max Temperature (°F)", value=False)
    plot_tmin = st.sidebar.checkbox("Min Temperature (°F)", value=False)
    plot_prcp = st.sidebar.checkbox("Precipitation (inches)", value=True)
    plot_snow = st.sidebar.checkbox("Snow (inches)", value=False)
    plot_snwd = st.sidebar.checkbox("Snow Depth (inches)", value=False)

    if st.sidebar.button("Apply Precipitation Filter"):
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
            
            # Create plotly figure for weather data
            fig = go.Figure()
            
            for col in chart_data.columns:
                fig.add_trace(go.Scatter(
                    x=chart_data.index,
                    y=chart_data[col],
                    mode='lines+markers',
                    name=col
                ))
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Value",
                plot_bgcolor='#1a1a1a' if theme else '#FFFFFF',
                paper_bgcolor='#1a1a1a' if theme else '#FFFFFF',
                font=dict(color='#FFFFFF' if theme else '#000000'),
                xaxis=dict(
                    gridcolor='#444444' if theme else '#E0E0E0',
                    linecolor='#444444' if theme else '#CCCCCC',
                    color='#FFFFFF' if theme else '#000000'
                ),
                yaxis=dict(
                    gridcolor='#444444' if theme else '#E0E0E0',
                    linecolor='#444444' if theme else '#CCCCCC',
                    color='#FFFFFF' if theme else '#000000'
                ),
                legend=dict(
                    bgcolor='#1a1a1a' if theme else '#FFFFFF',
                    bordercolor='#444444' if theme else '#CCCCCC',
                    font=dict(color='#FFFFFF' if theme else '#000000')
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least one parameter to plot.")

        # Raw data
        st.subheader("Raw Data")
        st.dataframe(df)

    else:
        st.info("Set filters and click 'Apply Precipitation Filter' to fetch data.")