import streamlit as st
from google import genai
from google.genai import types 
from app.data.db import connect_database
from app.data.tickets import get_all_tickets
from app.data.datasets import get_all_metadata
from app.data.incidents import get_all_incidents
conn=connect_database()
incidents=get_all_incidents(conn)
tickets=get_all_tickets(conn)
datasets=get_all_metadata(conn)
client=genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
with st.sidebar:
    Domains=st.selectbox("Domain", ["Cyber Incidents", "IT tickets", "MetaData"])
if Domains == "Cyber Incidents":
    st.subheader("AI Incident Analyzer")
    if not incidents.empty:
        incidents_options=[
            f"{row['date']}: {row['incident_type']} - {row['severity']}"
            for index, row in incidents.iterrows()
        ]
        selected_idx=st.selectbox(
            "Select incident to analyze: ",
            range(len(incidents)),
            format_func=lambda i:incidents_options[i]
        )
        incident =incidents.iloc[selected_idx]
        #Display incident details
        st.subheader("Incident details")
        st.write(f"**Type:** {incident['incident_type']}")
        st.write(f"**Severity:** {incident['severity']}")
        st.write(f"**Description:** {incident['description']}")
        st.write(f"**Status:** {incident['status']}")

        if st.button("Analyze with AI", type="primary"):
            with st.spinner("AI analyzing incident..."):
                analysis_prompt = f"""Analyze this cybersecurity incident:
                                    Type: {incident['incident_type']}
                                    Severity: {incident['severity']}
                                    Description: {incident['description']}
                                    Status: {incident['status']}

                                    Provide:
                                    1. Root cause analysis
                                    2.Immediate action needed
                                    3.Long term prevention measures
                                    4. Risk assessment"""
                
            response=client.models.generate_content_stream(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a cybersecurity expert. Analyze incidents, threats, and vulnerabilities. " \
                "Provide technical guidance using MITRE ATT&CK, CVE references. Prioritize actionable recommendations"
            ),
            contents={"role": "user", "parts": [{"text": analysis_prompt}]},
            )

            st.subheader("AI analysis")
            container=st.empty()
            full_reply=""
            for chunk in response:
                full_reply += chunk.text
                container.markdown(full_reply)

if Domains == "IT tickets":
    st.subheader("AI IT Ticket Analyzer")
    if not tickets.empty:
        tickets_options=[
            f"{row['id']}: {row['ticket_id']} - {row['description']}"
            for index, row in tickets.iterrows()
        ]
        selected_idx=st.selectbox(
            "Select it ticket to analyze: ",
            range(len(tickets)),
            format_func=lambda i:tickets_options[i]
        )
        ticket =tickets.iloc[selected_idx]
        #Display incident details
        st.subheader("Ticket details")
        st.write(f"**Ticket ID:** {ticket['ticket_id']}")
        st.write(f"**Priority:** {ticket['priority']}")
        st.write(f"**Status:** {ticket['status']}")
        st.write(f"**Category:** {ticket['category']}")
        st.write(f"**Subject:** {ticket['subject']}")
        st.write(f"**Description:** {ticket['description']}")

        if st.button("Analyze with AI", type="primary"):
            with st.spinner("AI analyzing it ticket..."):
                analysis_prompt = f"""Analyze this IT ticket:
                                    Ticket ID: {ticket['ticket_id']}
                                    Priority: {ticket['priority']}
                                    Status: {ticket['status']}
                                    Category: {ticket['category']}
                                    Subject: {ticket['subject']}
                                    Description: {ticket['description']}

                                    Provide:
                                    1. Root cause analysis
                                    2.Immediate action needed
                                    3.Long term prevention measures
                                    4. Risk assessment"""
                
            response=client.models.generate_content_stream(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are an IT operations expert. Help troubleshoot issues, optimize systems, manage tickets, and provide infrastructure guidance. Focus on practical solutions."
            ),
            contents={"role": "user", "parts": [{"text": analysis_prompt}]},
            )

            st.subheader("AI analysis")
            container=st.empty()
            full_reply=""
            for chunk in response:
                full_reply += chunk.text
                container.markdown(full_reply)

if Domains == "MetaData":
    st.subheader("AI Metadata Analyzer")
    if not datasets.empty:
        datasets_options=[
            f"{row['id']}: {row['dataset_name']} - {row['source']}"
            for index, row in datasets.iterrows()
        ]
        selected_idx=st.selectbox(
            "Select dataset to analyze: ",
            range(len(datasets)),
            format_func=lambda i:datasets_options[i]
        )
        dataset =datasets.iloc[selected_idx]
        #Display incident details
        st.subheader("Dataset details")
        st.write(f"**Dataset Name:** {dataset['dataset_name']}")
        st.write(f"**Category:** {dataset['category']}")
        st.write(f"**Source:** {dataset['source']}")

        if st.button("Analyze with AI", type="primary"):
            with st.spinner("AI analyzing dataset..."):
                analysis_prompt = f"""Analyze this Dataset:
                                    Dataset Name: {dataset['dataset_name']}
                                    Category: {dataset['category']}
                                    Source: {dataset['source']}

                                    Provide:
                                    1. Root cause analysis
                                    2.Immediate action needed
                                    3.Long term prevention measures
                                    4. Risk assessment"""
                
            response=client.models.generate_content_stream(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="You are a data science expert. Help with data analysis, visualization, statistical methods, and machine learning. Explain concepts clearly and suggest appropriate techniques."
            ),
            contents={"role": "user", "parts": [{"text": analysis_prompt}]},
            )

            st.subheader("AI analysis")
            container=st.empty()
            full_reply=""
            for chunk in response:
                full_reply += chunk.text
                container.markdown(full_reply)