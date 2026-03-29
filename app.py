import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Network Dashboard", layout="wide")

# ------------------ CUSTOM STYLING ------------------
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #FFFFFF;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("Network Traffic Dashboard")
st.caption("Real-time analysis and forecasting of network usage")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("network_traffic.csv")
df['time'] = pd.to_datetime(df['time'])
df['total_bytes'] = df['bytes_sent'] + df['bytes_received']
df = df.set_index('time').sort_index()

# ------------------ RESAMPLE ------------------
df_hourly = df['total_bytes'].resample('H').sum().ffill()

# ------------------ METRICS ------------------
st.markdown("## Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Traffic", f"{int(df_hourly.mean()):,}")
col2.metric("Peak Traffic", f"{int(df_hourly.max()):,}")
col3.metric("Min Traffic", f"{int(df_hourly.min()):,}")

# ------------------ CHARTS ------------------
colA, colB = st.columns(2)

with colA:
    st.markdown("### Traffic Over Time")
    st.line_chart(df_hourly)

with colB:
    st.markdown("### Trend (Smoothed)")
    rolling = df_hourly.rolling(window=5).mean()
    st.line_chart(rolling)

# ------------------ FORECAST ------------------
st.markdown("## 24-Hour Forecast")
model = ARIMA(df_hourly, order=(1,1,1))
model_fit = model.fit()
forecast = model_fit.forecast(steps=24)
forecast.index = pd.date_range(start=df_hourly.index[-1], periods=24, freq='H')

st.line_chart(forecast)

# ------------------ INSIGHTS ------------------
st.markdown("## Insights")
st.info("""
- Network traffic initially peaks and then stabilizes.
- Trend analysis shows a smooth downward pattern followed by steady usage.
- Forecast indicates stable traffic with no major spikes expected.
""")
