import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Network Dashboard", layout="wide")

# ------------------ SIDEBAR NAVIGATION ------------------
page = st.sidebar.selectbox("Navigation", ["Home", "Dashboard", "Documentation"])

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("network_traffic.csv")
    df['time'] = pd.to_datetime(df['time'])
    df['total_bytes'] = df['bytes_sent'] + df['bytes_received']
    df = df.set_index('time').sort_index()
    return df

# ------------------ HOME PAGE ------------------
if page == "Home":
    st.title("Network Traffic Analysis System")
    st.subheader("Welcome")
    st.write("""
    This project focuses on analyzing network traffic data using time series techniques.

    It helps in:
    - Understanding traffic patterns
    - Identifying trends over time
    - Predicting future network usage

    Use the navigation panel to explore the dashboard and documentation.
    """)

# ------------------ DASHBOARD PAGE ------------------
elif page == "Dashboard":
    st.title("Network Traffic Dashboard")

    df = load_data()

    df_hourly = df['total_bytes'].resample('H').sum().ffill()

    # Metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Traffic", f"{int(df_hourly.mean()):,}")
    col2.metric("Peak Traffic", f"{int(df_hourly.max()):,}")
    col3.metric("Min Traffic", f"{int(df_hourly.min()):,}")

    # Charts
    colA, colB = st.columns(2)

    with colA:
        st.subheader("Traffic Over Time")
        st.line_chart(df_hourly)

    with colB:
        st.subheader("Trend (Smoothed)")
        rolling = df_hourly.rolling(window=5).mean()
        st.line_chart(rolling)

    # Forecast
    st.subheader("24-Hour Forecast")
    model = ARIMA(df_hourly, order=(1,1,1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=24)
    forecast.index = pd.date_range(start=df_hourly.index[-1], periods=24, freq='H')

    st.line_chart(forecast)

# ------------------ DOCUMENTATION PAGE ------------------
elif page == "Documentation":
    st.title("Project Documentation")

    st.subheader("Overview")
    st.write("""
    This project applies time series analysis to network traffic data.
    The goal is to understand patterns and forecast future usage.
    """)

    st.subheader("Dataset")
    st.write("""
    The dataset contains timestamps, bytes sent, and bytes received.
    A new feature called total_bytes is created for analysis.
    """)

    st.subheader("Methodology")
    st.write("""
    - Data preprocessing and cleaning
    - Time-based resampling
    - Trend analysis using rolling averages
    - Forecasting using ARIMA model
    """)

    st.subheader("Conclusion")
    st.write("""
    The analysis shows that network traffic follows identifiable patterns
    and can be predicted using time series models.
    """)
