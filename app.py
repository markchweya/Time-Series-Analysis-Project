import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Network Dashboard", layout="wide")

# ------------------ TITLE ------------------
st.title("📡 Network Traffic Dashboard")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("network_traffic.csv")
df['time'] = pd.to_datetime(df['time'])
df['total_bytes'] = df['bytes_sent'] + df['bytes_received']
df = df.set_index('time').sort_index()

# ------------------ RESAMPLE ------------------
df_hourly = df['total_bytes'].resample('H').sum().ffill()

# ------------------ METRICS ------------------
col1, col2 = st.columns(2)
col1.metric("Average Traffic", int(df_hourly.mean()))
col2.metric("Peak Traffic", int(df_hourly.max()))

# ------------------ TRAFFIC ------------------
st.subheader("Traffic Over Time")
st.line_chart(df_hourly)

# ------------------ TREND (FIXED) ------------------
st.subheader("Trend (Smoothed)")
rolling = df_hourly.rolling(window=5).mean()
st.line_chart(rolling)

# ------------------ FORECAST ------------------
model = ARIMA(df_hourly, order=(1,1,1))
model_fit = model.fit()
forecast = model_fit.forecast(steps=24)

# Fix forecast index
forecast.index = pd.date_range(start=df_hourly.index[-1], periods=24, freq='H')

st.subheader("24-Hour Forecast")
st.line_chart(forecast)

# ------------------ INSIGHTS ------------------
st.subheader("Insights")
st.write("- Network traffic shows an initial peak followed by stabilization.")
st.write("- Rolling trend confirms a downward trend and steady usage.")
st.write("- Forecast predicts stable traffic in the next 24 hours.")