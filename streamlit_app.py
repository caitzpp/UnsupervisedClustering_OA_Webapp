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

if __name__ == "__main__":
    if not st.user.is_logged_in:
        login.login_page()

        st.stop()
    pg = app_page.run_app()
    pg.run()