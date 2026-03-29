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
    st.title("Project Documentation")

    st.markdown("""
    ## Overview
    This project focuses on analyzing network traffic using time series analysis and forecasting techniques. The goal is to understand how network usage changes over time and to predict future traffic patterns.

    ## Problem Statement
    Network systems generate large amounts of data continuously. Understanding this data is important for:
    - Capacity planning
    - Performance monitoring
    - Detecting unusual behavior

    This project uses historical traffic data to extract patterns and make predictions.

    ## Dataset Description
    The dataset contains the following columns:
    - **time**: Timestamp of network activity
    - **bytes_sent**: Amount of data sent
    - **bytes_received**: Amount of data received

    A new feature called **total_bytes** is created by combining sent and received data to represent total network usage.

    ## Data Preprocessing
    - Converted time column to datetime format
    - Sorted data by time
    - Set time as index for time series analysis
    - Resampled data into hourly intervals
    - Handled missing values using forward fill

    ## Time Series Analysis
    Time series analysis involves studying data points collected over time. In this project:
    - Traffic patterns are visualized over time
    - Trends are identified using rolling averages
    - Noise is reduced to reveal underlying behavior

    ## Trend Analysis
    A rolling mean (moving average) is applied to smooth short-term fluctuations. This helps in identifying long-term trends in network usage.

    ## Forecasting with ARIMA
    The ARIMA (AutoRegressive Integrated Moving Average) model is used for forecasting.

    - **AR (AutoRegressive):** Uses past values
    - **I (Integrated):** Removes trends to stabilize data
    - **MA (Moving Average):** Uses past errors to improve predictions

    The model is trained on historical data and used to predict the next 24 hours of network traffic.

    ## Dashboard Features
    - Interactive charts for traffic visualization
    - Trend analysis using rolling averages
    - Forecast visualization
    - Key metrics (average, peak, minimum)

    ## Key Insights
    - Network traffic shows an initial peak followed by stabilization
    - Trends indicate consistent usage patterns after fluctuations
    - Forecast suggests stable future traffic with minimal variation

    ## Limitations
    - Small dataset may reduce model accuracy
    - ARIMA model parameters are not optimized
    - Does not capture sudden unexpected spikes

    ## Future Improvements
    - Use larger datasets for better accuracy
    - Tune ARIMA parameters
    - Implement anomaly detection
    - Use advanced models like Prophet or LSTM

    ## Conclusion
    This project demonstrates how time series analysis can be applied to real-world data to understand patterns and predict future behavior. It provides a foundation for building intelligent monitoring systems.
    """)
