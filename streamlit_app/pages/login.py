import streamlit as st
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader



def login_page():
    # hide_sidebar_style = """
    #     <style>
    #     [data-testid="stSidebar"] {visibility: hidden; width: 0px;}
    #     </style>
    # """
    # st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    with open('login_info.yaml') as file:
        login_info = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        credentials=login_info['credentials'],
        cookie_name=login_info['cookie']['name'],
        cookie_key=login_info['cookie']['key'],
        cookie_expiry_days=login_info['cookie']['expiry_days'],

    )

    authenticator.login()

# if __name__ == "__main__":
#     login_page()