import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_metadata
st.set_page_config(  
    page_title="Analytics",
    page_icon="💻",
    layout="wide")

if "logged_in" not in st.session_state:
# Ensure state keys exist (in case user opens this page first)
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the analytics.")
    if st.button("Go to login page"):
        st.switch_page("Home.py") # back to the first page
    st.stop()

conn=connect_database()
with st.sidebar:
    Domains=st.selectbox("Domain", ["Cyber Incidents", "IT tickets", "MetaData"])
st.sidebar.success("Select a page.")
if Domains== "Cyber Incidents":
    st.subheader("Cybersecurity data visualisation")
    df_incidents=get_all_incidents(conn)
    st.dataframe(df_incidents, use_container_width=True)
    col1, col2, col3= st.columns(3)
    with col1:
       st.metric("Threats Detected", 247, delta="+12")
    with col2:
       st.metric("Vulnerabilities", 8, delta="-3")
    with col3:
       st.metric("Incidents", 3, delta="+1")
    threat_data={ "Malware":89, "Phishing":67, "DDoS":45, "Intrusion":46}
    st.bar_chart(threat_data)

if Domains== "IT tickets":
    st.subheader("IT tickets data visualisation")
    df_tickets=get_all_tickets(conn)
    st.dataframe(df_tickets, use_container_width=True)
    col1, col2, col3= st.columns(3)
    with col1:
        st.metric("CPU Usage", "67%", delta="+5%")

    with col2:
        st.metric("Memory", "8.2 GB", delta="+0.3 GB")

    with col3:
        st.metric("Uptime", "99.8%", delta="+0.1%")
    if "status" in df_tickets.columns:
        fig = px.bar(df_tickets, x="status", title="Status of tickets")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Column 'status' not found in table.")

   

if Domains== "MetaData":
    st.subheader("Metadata datasets visualisation")
    df_metadata=get_all_metadata(conn)
    st.dataframe(df_metadata, use_container_width=True)
    col1, col2, col3= st.columns(3)
    with col1:
        st.metric("Accuracy", "94.2%")
    with col2:
        st.metric("Precision", "91.8%")
    with col3:
        st.metric("Recall", "89.5%")
    if "record_count" in df_metadata.columns:
        fig = px.bar(df_metadata, x="record_count", title="Record counts of datasets")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Column 'record_count' not found in table.")
    
if st.button("Log out"):
 st.session_state.logged_in = False
 st.session_state.username = ""
 st.info("You have been logged out.")
 st.switch_page("Home.py")
if not st.session_state.logged_in:
 st.error("You must be logged in...")
 st.switch_page("Home.py")
 st.stop()