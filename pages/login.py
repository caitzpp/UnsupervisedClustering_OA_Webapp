import streamlit as st
import dotenv
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

dotenv.load_dotenv()


def login_page():
    with open('login_info.yaml') as file:
        login_info = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        login_info['credentials'],
        login_info['cookie']['name'],
        login_info['cookie']['key'],
        login_info['cookie']['expiry_days']
    )

    if not st.user.is_logged_in:
        # log_in = st.navigation("Login")
        authenticator.login()

def check_login(username, password):
    # Replace this with your actual login logic (database, API calls, etc.)
    return username == os.getenv("USERNAME") and password == os.getenv("PASSWORD")

if __name__ == "__main__":
    login_page()