import streamlit as st
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if not st.session_state.logged_in:
    st.error("You must be logged in.")
    if st.button("Go to login page"):
        st.switch_page("Home.py") # back to the first page
    st.stop()
st.title("Settings")