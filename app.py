import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Network Dashboard", layout="wide")

# ------------------ NAVBAR ------------------
st.markdown("""
    <style>
    .nav {
        display: flex;
        gap: 20px;
        background-color: #111827;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .nav a {
        color: #E5E7EB;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

menu = st.radio("", ["Home", "Dashboard", "Documentation"], horizontal=True)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("network_traffic.csv")
    df['time'] = pd.to_datetime(df['time'])
    df['total_bytes'] = df['bytes_sent'] + df['bytes_received']
    df = df.set_index('time').sort_index()
    return df

# ------------------ HOME PAGE ------------------
if menu == "Home":
    st.title("Network Traffic Analysis System")

    st.markdown("""
    ### Overview
    This project analyzes network traffic using time series techniques.

    ### What it does:
    - Understand traffic patterns over time
    - Identify trends and behavior
    - Predict future network usage using ARIMA model

    ### Why it matters:
    Helps in network planning, monitoring, and optimization.
    """)

# ------------------ DASHBOARD ------------------
elif menu == "Dashboard":
    st.title("Network Traffic Dashboard")

    df = load_data()
    df_hourly = df['total_bytes'].resample('H').sum().ffill()

    # Metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average", f"{int(df_hourly.mean()):,}")
    col2.metric("Peak", f"{int(df_hourly.max()):,}")
    col3.metric("Min", f"{int(df_hourly.min()):,}")

    # Charts
    colA, colB = st.columns(2)

    with colA:
        st.subheader("Traffic Over Time")
        st.line_chart(df_hourly)

    with colB:
        st.subheader("Trend")
        rolling = df_hourly.rolling(window=5).mean()
        st.line_chart(rolling)

    # Forecast
    st.subheader("24-Hour Forecast")
    model = ARIMA(df_hourly, order=(1,1,1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=24)
    forecast.index = pd.date_range(start=df_hourly.index[-1], periods=24, freq='H')

    st.line_chart(forecast)

# ------------------ DOCUMENTATION ------------------
elif menu == "Documentation":
    st.title("Documentation")

    st.markdown("""
    ### Project Description
    This project applies time series analysis to network traffic data.

    ### Methodology
    - Data preprocessing
    - Time resampling
    - Trend analysis
    - ARIMA forecasting

    ### Outcome
    The system predicts future network traffic based on historical patterns.
    """)
