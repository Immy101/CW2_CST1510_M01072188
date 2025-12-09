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

if Domains== "IT Tickets":
    df_tickets=get_all_tickets(conn)
    st.dataframe(df_tickets, use_container_width=True)
    col1, col2, col3= st.columns(3)
    with col1:
       st.metric("Threats Detected", 247, delta="+12")
    with col2:
       st.metric("Vulnerabilities", 8, delta="-3")
    with col3:
       st.metric("Incidents", 3, delta="+1")
    threat_data={ "Malware":89, "Phishing":67, "DDoS":45, "Intrusion":46}
    st.bar_chart(threat_data)

if Domains== "MetaData":
    df_metadat=get_all_metadata(conn)
    st.dataframe(df_tickets, use_container_width=True)
    col1, col2, col3= st.columns(3)
    with col1:
       st.metric("Threats Detected", 247, delta="+12")
    with col2:
       st.metric("Vulnerabilities", 8, delta="-3")
    with col3:
       st.metric("Incidents", 3, delta="+1")
    threat_data={ "Malware":89, "Phishing":67, "DDoS":45, "Intrusion":46}
    st.bar_chart(threat_data)
    
if st.button("Log out"):
 st.session_state.logged_in = False
 st.session_state.username = ""
 st.info("You have been logged out.")
 st.switch_page("Home.py")
if not st.session_state.logged_in:
 st.error("You must be logged in...")
 st.switch_page("Home.py")
 st.stop()