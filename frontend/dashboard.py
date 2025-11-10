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
st.sidebar.markdown("### Date range (YYYY-MM-DD)")
start_date = st.sidebar.text_input("Start date (YYYY-MM-DD)", value="")
end_date = st.sidebar.text_input("End date (YYYY-MM-DD)", value="")

limit = st.sidebar.number_input("Rows to fetch", min_value=10, max_value=5000, value=1000, step=10)

if st.sidebar.button("Apply"):
    with st.spinner("Fetching data..."):
        data = get_data(
            outfall=selected_outfall or None,
            parameter=selected_parameter or None,
            base=selected_base or None,
            unit=selected_unit or None,
            start_date=start_date or None,
            end_date=end_date or None,
            limit=limit
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

    # Raw data

    # Plot DMR Value vs Date
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
    st.subheader("Raw Data")
    st.dataframe(df)
else:
    st.info("Set filters and click Apply to fetch data.")