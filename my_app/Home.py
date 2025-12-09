import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.db import connect_database
from app.services.user_service import hash_password,login,verify,pw_strength
from app.data.users import insert_user, get_user_by_username
conn=connect_database()
st.set_page_config(
    page_title="Intelligence Domain Platform",
    page_icon="🔭",
    layout="wide")
st.title("MULTI-DOMAIN PLATFORM")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
st.title(" Welcome")
# If already logged in, go straight to dashboard (optional)
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"): # Use the official navigation API to switch pages
        st.switch_page("pages/Dashboard.py") # path isrelative to Home.py :contentReference[oaicite:1]{index=1}
    st.stop() # Don’t show login/register again

tab_login, tab_register = st.tabs(["Login", "Register"])
#LOGIN TAB
with tab_login:
    st.subheader("Login")
    username = st.text_input("Username",key="login_username")
    password = st.text_input("Password", type="password",key="login_password")
    role=st.text_input("Role",key="login_role")
    if st.button("Log in", type="primary"):
        users = get_user_by_username(username)
        if users is None:
            st.error("User not found.")
        else:
            if username == users[1]:
                verify(username, password)
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}! 🎉 ")
                # Redirect to dashboard page
                st.switch_page("pages/Dashboard.py")
            else:
                st.error("Invalid username or password.")

#REGISTER tab
with tab_register:
    st.subheader("Register")
    username = st.text_input("Enter in username",key="register_username")
    password = st.text_input("Enter in password",type="password", key="register_password")
    confirm_password = st.text_input("Confirm password",type="password", key="register_confirm")
    role= st.text_input("Enter your role",key="register_role")
    if st.button("Create account"):# Basic checks
        if not username or not password:
            st.warning("Please fill in all fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                users = get_user_by_username(username)
                if users is not None:
                    st.error("Username already exists. Choose another one.")
                else:# "Save" user in table
                    checker=pw_strength(password)
                    password_hash=hash_password(password)
                    success=insert_user(username, password_hash, role)
                    st.success("Account created! You can now log in from the Login tab.")
                    st.info("Tip: go to the Login tab and sign in with your new account.")
            except Exception as e:
                st.error(f"Error during registration: {str(e)}")

 