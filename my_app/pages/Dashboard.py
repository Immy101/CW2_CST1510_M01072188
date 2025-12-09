import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, update_incident_status, insert_incident, delete_incident
from app.data.tickets import get_all_tickets, update_ticket_status, insert_ticket, delete_ticket
from app.data.datasets import get_all_metadata, update_metadata, insert_metadata, delete_metadata
conn=connect_database()
st.set_page_config(  
    page_title="Dashboard",
    page_icon="🔗",
    layout="wide")

if "logged_in" not in st.session_state:
# Ensure state keys exist (in case user opens this page first)
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py") # back to the first page
    st.stop()
# If logged in, show dashboard content
st.title("📊 Dashboard")
st.write("Welcome to the Main Dashboard.")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
with st.sidebar:
    Domains=st.selectbox("Domain", ["Cyber Incidents", "IT tickets", "MetaData"])
st.sidebar.success("Select a page.")

if Domains== "Cyber Incidents":
   st.title("Cyber Incidents")
   df_incidents=get_all_incidents(conn)
   st.dataframe(df_incidents, use_container_width=True)
   with st.sidebar:
        data=st.selectbox("", ["Insert Incident","Update Incident" , "Delete Incident"])
   if data == "Insert Incident":
        with st.form("New Incident"):
            date=st.date_input("Date", format="YYYY-MM-DD")
            incident_type=st.text_input("Incident type")
            severity=st.selectbox("Severity",["Low", "Medium", "High", "Critical"])
            status=st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            description=st.text_input("Description")
            reported_by=st.text_input("Reported by")
            submitted=st.form_submit_button("Add Incident")
        if submitted and incident_type:
                insert_incident(conn, date, incident_type, severity, status, description, reported_by)
                st.success("Incident added.")
                st.rerun
   if data == "Update Incident":
        with st.form("Update Incident"):
            id=st.text_input("ID")
            status=st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            submitted=st.form_submit_button("Update Incident")
        if submitted and incident_type:
                update_incident_status(conn, status, id)
                st.success("Incident updated.")
                st.rerun
   if data == "Delete Incident":
        with st.form("Delete Incident"):
            id=st.text_input("ID")
            submitted=st.form_submit_button("Delete Incident")
        if submitted and incident_type:
                delete_incident(conn, id)
                st.success("Incident deleted.")
                st.rerun
    

if Domains== "IT tickets":
   st.title("IT tickets")
   df_tickets=get_all_tickets(conn)
   st.dataframe(df_tickets, use_container_width=True)
   with st.sidebar:
        data=st.selectbox("", ["Insert Ticket","Update Ticket" , "Delete Ticket"])
   if data == "Insert Ticket":
        with st.form("New Ticket"):
            ticket_id=st.text_input("Ticket id")
            priority=st.selectbox("Priorty",["Low","Medium", "High"])
            status=st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            category=st.selectbox("Category", ["Hardware", "Software", "Network"])
            subject=st.text_input("Subject")
            description=st.text_input("Ticket description")
            created_date=st.date_input("Date Created", format="YYYY-MM-DD")
            assigned_to=st.text_input("Assigned to")
            submitted=st.form_submit_button("Add Ticket")
        if submitted and ticket_id:
                insert_ticket(conn, ticket_id, priority, status, category, subject, description, created_date, assigned_to)
                st.success("Ticket added.")
                st.rerun
   if data == "Update Ticket":
        with st.form("Update Ticket"):
            resolved_date=st.date_input("Date resolved", format="YYYY-MM-DD")
            status=st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            ticket_id=st.text_input("Ticket id")
            submitted=st.form_submit_button("Update Ticket")
        if submitted and ticket_id:
                update_ticket_status(conn, resolved_date, status, ticket_id)
                st.success("Ticket added.")
                st.rerun
   if data == "Delete Ticket":
        with st.form("Delete Ticket"):
            ticket_id=st.text_input("Ticket id")
            submitted=st.form_submit_button("Delete Ticket")
        if submitted and ticket_id:
                delete_ticket(conn, ticket_id)
                st.success("Ticket deleted.")
                st.rerun

if Domains== "MetaData":
   st.title("MetaData")
   df_metadata=get_all_metadata(conn)
   st.dataframe(df_metadata, use_container_width=True)
   with st.sidebar:
        data=st.selectbox("", ["Insert Dataset", "Update Dataset" , "Delete Dataset"])
   if data == "Insert Dataset":
        with st.form("New DataSet"):
            dataset_name=st.text_input("DataSet name")
            category=st.text_input("Category")
            record_count=st.text_input("Record count")
            source=st.text_input("Source")
            last_updated=st.date_input("Last updated", format="YYYY-MM-DD")
            file_size_mb=st.number_input("File size", min_value=None, max_value=None)
            submitted=st.form_submit_button("Add New Dataset")
        if submitted and dataset_name:
                insert_metadata(conn, dataset_name, severity, status)
                st.success("DataSet added.")
                st.rerun

   if data == "Update Dataset":
        with st.form("Update Dataset"):
            last_updated=st.date_input("Last updated", format="YYYY-MM-DD")
            dataset_name=st.text_input("DataSet Name")
            submitted=st.form_submit_button("Update Dataset")
        if submitted and dataset_name:
                update_metadata(conn, last_updated, dataset_name)
                st.success("Dataset updated.")
                st.rerun

   if data == "Delete Dataset":
        with st.form("Delete Ticket"):
            dataset_name=st.text_input("DataSet Name")
            submitted=st.form_submit_button("Delete Dataset")
        if submitted and ticket_id:
                insert_ticket(conn, dataset_name)
                st.success("Dataset deleted.")
                st.rerun
   

st.divider()
if st.button("Log out"):
 st.session_state.logged_in = False
 st.session_state.username = ""
 st.info("You have been logged out.")
 st.switch_page("Home.py")
if not st.session_state.logged_in:
 st.error("You must be logged in...")
 st.switch_page("Home.py")
 st.stop()