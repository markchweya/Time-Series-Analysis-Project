# 📄 Time Series Analysis and Forecasting of Network Traffic

Time series analysis is a statistical method used to analyze data collected over time. It is widely applied in fields such as finance, weather forecasting, healthcare, and network monitoring. In this project, time series analysis is applied to network traffic data to understand usage patterns and predict future behavior.

The dataset used in this project contains timestamps along with the number of bytes sent and received over a network. A new variable, total_bytes, was created by combining both sent and received data to represent total network activity. The time column was converted into a datetime format and set as the index to enable time-based operations.

To better understand trends, the data was resampled into hourly intervals. This helped reduce noise and provided a clearer view of how network traffic changes over time. Visualization of the hourly data revealed fluctuations in usage, indicating periods of high and low activity.

A rolling average was applied to smooth out short-term variations and highlight longer-term trends. This made it easier to observe consistent patterns in network behavior, such as peak usage periods during active hours.

For forecasting, the ARIMA (AutoRegressive Integrated Moving Average) model was used. This model is commonly used in time series analysis to predict future values based on past observations. Using ARIMA, future network traffic for the next 24 hours was predicted. The forecast showed that network usage follows a somewhat predictable pattern, making it possible to anticipate future demand.

An interactive dashboard was developed using Streamlit to present the results. The dashboard includes visualizations of network traffic over time, trend analysis using rolling averages, and future forecasts. This allows users to explore the data dynamically and gain insights quickly.

From the analysis, it can be concluded that network traffic exhibits identifiable patterns and trends. Peak usage occurs during active periods, and forecasting models can be used to predict short-term future behavior. This has practical applications in network management, capacity planning, and anomaly detection.

Overall, this project demonstrates how time series analysis and forecasting techniques can be applied to real-world data to extract meaningful insights and support decision-making.