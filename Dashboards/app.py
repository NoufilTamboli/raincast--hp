# dashboard/app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000/weather"  # FastAPI endpoint

st.set_page_config(page_title="RainCast HP Dashboard",
                   layout="wide",
                   page_icon="🌧")

st.title("🌧 RainCast Himachal Pradesh — Live Weather & Flood Risk Monitoring")

# Fetch data from API
@st.cache_data(ttl=300)   # caches for 5 minutes like real systems
def load_data():
    try:
        r = requests.get(API)
        return pd.DataFrame(r.json())
    except:
        return None

df = load_data()

if df is None or df.empty:
    st.error("⚠ No data found or backend not running")
    st.code("Run: python -m backend.fetch_weather")
else:
    # Show Metrics
    st.subheader("📊 Live Weather Overview")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Temperature", f"{df['temperature'].mean():.2f}°C")
    col2.metric("Avg Humidity", f"{df['humidity'].mean():.2f}%")
    col3.metric("Total Records", len(df))
    col4.metric("Rainfall Max", f"{df['rainfall_mm'].max():.2f} mm")

    st.write("---")

    # Recent data table
    st.subheader("📁 Latest Weather Records")
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    # Graphs
    st.write("### 📈 Temperature Trend")
    fig_temp = px.line(df, x="timestamp", y="temperature", color="location_name", markers=True)
    st.plotly_chart(fig_temp, use_container_width=True)

    st.write("### 🌧 Rainfall Monitoring")
    fig_rain = px.bar(df, x="location_name", y="rainfall_mm", color="rainfall_mm")
    st.plotly_chart(fig_rain, use_container_width=True)

    # Flood risk alert logic
    st.write("### ⚠ Flood Risk Prediction (Basic Rule Model)")

    df["risk"] = df["rainfall_mm"].apply(lambda x: 
        "🔴 High" if x > 40 else
        "🟡 Medium" if x > 20 else
        "🟢 Low"
    )

    st.dataframe(df[["location_name","rainfall_mm","risk","temperature","humidity","timestamp"]],
                 use_container_width=True)

    high_risk = df[df["risk"]=="🔴 High"]
    if not high_risk.empty:
        st.error("🚨 High Flood Risk Areas Detected!")
        st.table(high_risk[["location_name","rainfall_mm","timestamp"]])
    else:
        st.success("No high-risk alerts currently.")
