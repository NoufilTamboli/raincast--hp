import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from backend.database import SessionLocal
from backend.models import WeatherData

st.set_page_config(
    page_title="RainCast HP Dashboard",
    layout="wide",
    page_icon="🌧"
)

st.title("🌧 RainCast Himachal Pradesh — Live Weather & Flood Monitoring")

# -------------------------------
# Load Data From Database
# -------------------------------

def load_data():
    db = SessionLocal()
    records = db.query(WeatherData).all()
    db.close()

    if not records:
        return pd.DataFrame()

    data = [{
        "id": r.id,
        "location_name": r.location_name,
        "temperature": r.temperature,
        "humidity": r.humidity,
        "rainfall_mm": r.rainfall_mm,
        "timestamp": r.timestamp
    } for r in records]

    return pd.DataFrame(data)

df = load_data()

# -------------------------------
# UI Logic
# -------------------------------

if df.empty:
    st.warning("⚠ No weather records found in database.")
else:
    st.subheader("📊 Weather Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Temperature", f"{df['temperature'].mean():.2f}°C")
    col2.metric("Avg Humidity", f"{df['humidity'].mean():.2f}%")
    col3.metric("Total Records", len(df))
    col4.metric("Max Rainfall", f"{df['rainfall_mm'].max():.2f} mm")

    st.write("---")

    st.subheader("📁 Latest Records")
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    st.write("### 📈 Temperature Trend")
    fig_temp = px.line(
        df,
        x="timestamp",
        y="temperature",
        color="location_name",
        markers=True
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    st.write("### 🌧 Rainfall Monitoring")
    fig_rain = px.bar(
        df,
        x="location_name",
        y="rainfall_mm",
        color="rainfall_mm"
    )
    st.plotly_chart(fig_rain, use_container_width=True)

    # Flood Risk Logic
    st.write("### ⚠ Flood Risk Prediction")

    df["risk"] = df["rainfall_mm"].apply(
        lambda x: "🔴 High" if x > 40
        else "🟡 Medium" if x > 20
        else "🟢 Low"
    )

    st.dataframe(
        df[["location_name", "rainfall_mm", "risk",
            "temperature", "humidity", "timestamp"]],
        use_container_width=True
    )

    high_risk = df[df["risk"] == "🔴 High"]

    if not high_risk.empty:
        st.error("🚨 High Flood Risk Areas Detected!")
        st.table(high_risk[["location_name", "rainfall_mm", "timestamp"]])
    else:
        st.success("✅ No high-risk alerts currently.")
