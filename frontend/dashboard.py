import streamlit as st
import pandas as pd
import numpy as np
from utils.api_client import get_filters, get_data
from datetime import datetime

st.set_page_config(page_title="NPDES Dashboard", layout="wide")
st.title("💧 NPDES Monitoring Dashboard")

with st.spinner("Loading filter values..."):
    filters = get_filters()

if not filters:
    st.error("Could not load filter values from backend.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
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
    max_value=datetime.today()
)
end_date = st.sidebar.date_input(
    "End date", 
    value=None, 
    min_value=datetime(2000, 1, 1), 
    max_value=datetime.today()
)

# Convert to string format (YYYY-MM-DD) before passing to API
start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None
end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

if st.sidebar.button("Apply"):
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
            st.line_chart(plot_df.set_index("monitoring_period_date")["dmr_value"])
        else:
            st.line_chart(plot_df["dmr_value"])
    else:
        st.info("No numeric dmr_value to plot.")
    
    # Raw data
    st.subheader("Raw Data")
    st.dataframe(df)

    # Statistical Analysis Table
    if "dmr_value" in df.columns and df["dmr_value"].notnull().any():
        st.subheader("📊 Statistical Analysis")

        numeric_series = pd.to_numeric(df["dmr_value"], errors="coerce").dropna()

        if len(numeric_series) > 0:
            stats = {
                "Minimum": numeric_series.min(),
                "Average": numeric_series.mean(),
                "Median": numeric_series.median(),
                "Maximum": numeric_series.max(),
                "Standard Deviation": numeric_series.std(),
                "Variance": numeric_series.var(),
                "Kurtosis": numeric_series.kurtosis(),
                "Skewness": numeric_series.skew(),
            }

            stats_df = pd.DataFrame(stats, index=["Value"]).T  # Transposed for neat layout
            st.table(stats_df)
        else:
            st.info("No numeric values available for statistical analysis.")
    else:
        st.info("No numeric dmr_value column found for statistical analysis.")

else:
    st.info("Set filters and click Apply to fetch data.")