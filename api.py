from flask import Flask, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_db_data(table_name):
    db_path = "C:/Users/JERMAGNE/warehouse.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

@app.route("/forecast", methods=["GET"])
def get_forecast():
    forecast_df = get_db_data("forecast_data")
    forecast_data = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10)
    return jsonify(forecast_data.to_dict(orient="records"))

@app.route("/anomalies", methods=["GET"])
def get_anomalies():
    df = get_db_data("warehouse_data")
    anomalies = df[df["anomaly"] == -1]
    return jsonify(anomalies.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
