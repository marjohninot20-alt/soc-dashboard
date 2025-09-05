import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import json
import sqlite3

def load_incidents_from_db():
    conn = sqlite3.connect("reports/incidents.db")
    df = pd.read_sql_query("SELECT * FROM incidents", conn)
    conn.close()
    return df

# Load from database
db_df = load_incidents_from_db()
db_df.rename(columns={"Timestamp": "timestamp"}, inplace=True)

# 🏆 Load milestone data
with open("reports/milestones.json", 'r') as f:
    milestones = json.load(f)

st.title("🛡️ SOC Threat Dashboard")
st.subheader("Incident Overview")

# 🏆 Milestone Section
st.markdown("### 🏆 Analyst Milestones")
col1, col2, col3 = st.columns(3)
col1.metric("Total Detections", milestones["total_detections"])
col2.metric("IP Detections", milestones["ip_detections"])
col3.metric("Phishing Alerts", milestones["phishing_detections"])
st.markdown(f"**First Detection:** {milestones['first_detection']}")
st.markdown(f"**Last Detection:** {milestones['last_detection']}")

if db_df.empty:
    st.info("No incidents logged yet.")
else:
    # 🔢 Severity Summary
    st.markdown("### 🔢 Severity Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Low", len(db_df[db_df["severity"] == "Low"]))
    col2.metric("Medium", len(db_df[db_df["severity"] == "Medium"]))
    col3.metric("High", len(db_df[db_df["severity"] == "High"]))

    # 🔍 Search Indicator
    keyword = st.text_input("🔍 Search Indicator")
    if keyword:
        db_df = db_df[db_df["indicator"].str.contains(keyword, case=False)]

    # 🎯 Severity Filter
    severity_filter = st.selectbox("Filter by Severity", ["All", "Low", "Medium", "High"])
    if severity_filter != "All":
        db_df = db_df[db_df["severity"] == severity_filter]

    # 🗺️ Zone Filter
    zone_filter = st.selectbox("Filter by Zone", ["All"] + sorted(db_df["zone"].unique()))
    if zone_filter != "All":
        db_df = db_df[db_df["zone"] == zone_filter]

    # 📋 Table View
    st.markdown("### 📋 Recent Alerts")
    st.dataframe(db_df.sort_values("timestamp", ascending=False), width='stretch')

    # 📊 Severity Distribution
    st.markdown("### 📊 Severity Distribution")
    severity_counts = db_df["severity"].value_counts()
    st.bar_chart(severity_counts)

    # 🌍 Zone Distribution
    st.markdown("### 🌍 Zone Distribution")
    zone_counts = db_df["zone"].value_counts()
    st.bar_chart(zone_counts)

    # 🧬 Data Schema
    st.markdown("**🧬 Data Schema:**")
    st.write(db_df.columns.tolist())
