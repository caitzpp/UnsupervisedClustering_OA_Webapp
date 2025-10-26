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

from pages import app_page, login

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login.login_page()

        if st.session_state.get('authentication_status'):
            st.session_state.logged_in = True
        elif st.session_state.get('authentication_status') is False:
            st.error("Username/password is incorrect")
            st.stop()
        elif st.session_state.get('authentication_status') is None:
            st.warning("Please enter your username and password")
            st.stop()
    
    if st.session_state.logged_in:
        pg = app_page.run_app()
        pg.run()