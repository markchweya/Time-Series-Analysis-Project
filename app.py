import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import time

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Network Dashboard", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Documentation"])

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("network_traffic.csv")
    df['time'] = pd.to_datetime(df['time'])
    df['total_bytes'] = df['bytes_sent'] + df['bytes_received']
    df = df.set_index('time').sort_index()
    return df

# ------------------ HOME ------------------
if page == "Home":
    st.title("Network Traffic Analysis System")

    with st.container():
        st.markdown("### Welcome")
        st.write("This system analyzes network traffic and predicts future usage.")

    # Animated loading effect
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    st.success("System Ready")

# ------------------ DASHBOARD ------------------
elif page == "Dashboard":
    st.title("Interactive Network Dashboard")

    df = load_data()
    df_hourly = df['total_bytes'].resample('H').sum().ffill()

    # Filters
    st.sidebar.subheader("Filters")
    start_date = st.sidebar.date_input("Start Date", df_hourly.index.min().date())
    end_date = st.sidebar.date_input("End Date", df_hourly.index.max().date())

    df_filtered = df_hourly[(df_hourly.index.date >= start_date) & (df_hourly.index.date <= end_date)]

    if df_filtered.empty:
        st.warning("No data available for selected date range")
        st.stop()

    # Metrics with animation feel
    col1, col2, col3 = st.columns(3)
    # Handle empty/NaN safely
    avg = df_filtered.mean()
    peak = df_filtered.max()
    min_val = df_filtered.min()

    col1.metric("Average", f"{int(avg):,}" if pd.notna(avg) else "N/A")
    col2.metric("Peak", f"{int(peak):,}" if pd.notna(peak) else "N/A")
    col3.metric("Min", f"{int(min_val):,}" if pd.notna(min_val) else "N/A")

    st.divider()

    # Tabs for smooth navigation
    tab1, tab2, tab3 = st.tabs(["Traffic", "Trend", "Forecast"])

    with tab1:
        st.subheader("Traffic Over Time")
        st.line_chart(df_filtered)

    with tab2:
        st.subheader("Trend Analysis")
        rolling = df_filtered.rolling(window=5).mean()
        st.line_chart(rolling)

    with tab3:
        st.subheader("Forecast")
        model = ARIMA(df_filtered, order=(1,1,1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=24)
        forecast.index = pd.date_range(start=df_filtered.index[-1], periods=24, freq='H')

        combined = pd.concat([df_filtered, forecast])
        st.line_chart(combined)

# ------------------ DOCUMENTATION ------------------
elif page == "Documentation":
    st.title("Project Documentation")

    with st.expander("Overview"):
        st.write("Time series analysis is used to analyze and forecast network traffic.")

    with st.expander("Dataset"):
        st.write("Contains timestamps, bytes sent and received.")

    with st.expander("Methodology"):
        st.write("Includes preprocessing, resampling, trend analysis, and ARIMA forecasting.")

    with st.expander("Conclusion"):
        st.write("Network traffic can be predicted using historical data patterns.")
