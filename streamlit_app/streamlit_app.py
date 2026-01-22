import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
from streamlit.components.v1 import iframe
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import config
import os
from loguru import logger

from pages import app_page, login
#localhost:8501

def hide_sidebar():
    """Hide sidebar via CSS."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {visibility: hidden; width: 0;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_sidebar():
    """Restore sidebar (undo hiding)."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {visibility: visible; width: auto;}
        </style>
        """,
        unsafe_allow_html=True,
    )

@st.cache_resource
def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger.remove()

    logger.add(
        "logs/streamlit.log",
        level="INFO",
        rotation="5 MB",
        enqueue=False,  # critical
        backtrace=True,
        diagnose=False,
    )

    logger.info("Logger initialized")

    return logger


if __name__ == "__main__":
    hide_sidebar()
    login.login_page()
        
    if st.session_state.get('authentication_status') is False:
        hide_sidebar()
        st.error("Username/password is incorrect")
        st.stop()
    elif st.session_state.get('authentication_status') is None:
        hide_sidebar()
        st.warning("Please enter your username and password")
        st.stop()
    else:
        show_sidebar()
    pg = app_page.run_app()
    pg.run()