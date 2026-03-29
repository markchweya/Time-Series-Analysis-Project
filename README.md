# 📡 Network Traffic Time Series Analysis & Forecasting

## 📌 Project Overview
This project analyzes network traffic data using time series techniques and builds an interactive dashboard to visualize trends and forecasts.

Time series analysis helps identify patterns such as trends, seasonality, and anomalies in data collected over time. In this project, network traffic (bytes sent and received) is analyzed to understand usage behavior and predict future demand.

---

## 📊 Dataset
The dataset (`network_traffic.csv`) contains:
- `time` → timestamp of network activity
- `bytes_sent` → data sent
- `bytes_received` → data received

A new feature `total_bytes` is created to represent total traffic.

---

## ⚙️ Methodology
1. Data preprocessing (datetime conversion, cleaning)
2. Feature engineering (`total_bytes`)
3. Time-based resampling (hourly aggregation)
4. Visualization of traffic trends
5. Rolling average to identify patterns
6. ARIMA model for forecasting

---

## 📈 Insights
- Network traffic shows clear fluctuations over time.
- Peak usage occurs during active hours.
- Rolling averages reveal underlying trends.
- Forecasting suggests predictable short-term behavior.

---

## 💻 Interactive Dashboard
Built using **Streamlit**, the dashboard includes:
- Traffic over time visualization
- Trend (rolling average)
- Forecasting (ARIMA model)

### ▶️ Run the app
```bash
python -m streamlit run app.py
```

---

## 📦 Requirements
Install dependencies:
```bash
pip install pandas numpy matplotlib statsmodels streamlit
```

---

## 🎯 Conclusion
This project demonstrates how time series analysis can be applied to real-world problems like network monitoring. It enables better planning, anomaly detection, and forecasting of future usage.

---

## 🚀 Future Improvements
- Hyperparameter tuning for ARIMA
- Anomaly detection system
- Advanced models (Prophet, LSTM)
- Enhanced dashboard UI
