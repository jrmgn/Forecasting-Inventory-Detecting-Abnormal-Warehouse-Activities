import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Warehouse Dashboard", layout="wide")
st.title("Warehouse Inventory Dashboard")

db_path = "C:/Users/JERMAGNE/warehouse.db" 
conn = sqlite3.connect(db_path)

# Load both tables
df = pd.read_sql("SELECT * FROM warehouse_data", conn)
forecast_df = pd.read_sql("SELECT * FROM forecast_data", conn)
conn.close()

# 1. KPI Section (Inventory Turnover Rate)
st.subheader("Key Performance Indicators")
# Calculation: Total Sales / Average Inventory
turnover_rate = df['sales'].sum() / df['inventory_level'].mean()
st.metric("Inventory Turnover Rate", value=f"{turnover_rate:.2f}")

# 2. Total Inventory Trends
st.subheader("Total Inventory Trends")
df['date'] = pd.to_datetime(df['date'])
st.line_chart(df.set_index('date')['inventory_level'])

# 3. Forecast Chart (Prophet Results)
st.subheader("Prophet Inventory Forecast (Next 30 Days)")
# Rename columns for streamlit's line chart (it likes a 'ds' or date index)
forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
chart_data = forecast_df.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']]
st.line_chart(chart_data)

# 4. Anomalous Activities
st.subheader("Detected Anomalies")
anomalies = df[df["anomaly"] == -1]
st.dataframe(anomalies)

# Add to app.py
st.subheader("System API Endpoints")
st.write("Live Forecast Endpoint: [http://127.0.0.1:5000/forecast](http://127.0.0.1:5000/forecast)")
st.write("Live Anomaly Endpoint: [http://127.0.0.1:5000/anomalies](http://127.0.0.1:5000/anomalies)")