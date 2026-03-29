import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv("network_traffic.csv")
df['time'] = pd.to_datetime(df['time'])
df['total_bytes'] = df['bytes_sent'] + df['bytes_received']
df = df.set_index('time').sort_index()

df_hourly = df['total_bytes'].resample('H').sum().fillna(method='ffill')

st.title("📡 Network Traffic Dashboard")

st.subheader("Traffic Over Time")
st.line_chart(df_hourly)

st.subheader("Trend")
rolling = df_hourly.rolling(24).mean()
st.line_chart(rolling)

model = ARIMA(df_hourly, order=(1,1,1))
model_fit = model.fit()
forecast = model_fit.forecast(steps=24)

st.subheader("Forecast")
st.line_chart(forecast)

st.subheader("Insights")
st.write("Network usage peaks during active hours and shows predictable patterns.")