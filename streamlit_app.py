import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
from streamlit.components.v1 import iframe
import config
import os

from pages import plotly_page, cluster_page, home, about

st.set_page_config(layout="wide", initial_sidebar_state = "collapsed", menu_items=None) #page_title="Cluster Dashboard", page_icon=":material/dashboard:", 

USERNAME=os.getenv("USERNAME", "admin")
PASSWORD=os.getenv("PASSWORD", "mypassword")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Please log in to access the dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.experimental_rerun() #Forced rerun to load app view
        else:
            st.error("Invalid username or password")
    st.stop()

home_page = st.Page(home.show_home, title = "Home", icon=":material/home:")
graph_page = st.Page(plotly_page.show_graph, title = "Embedding Explorer", icon=":material/biotech:")
as_page = st.Page(cluster_page.show_clusterpage, title = "Cluster Gallery", icon=":material/imagesmode:")
about_page = st.Page(about.show_about, title = "About", icon=":material/info:")


pg = st.navigation([home_page, graph_page, as_page, about_page])

 
 #icon logout


if __name__ == "__main__":
    pg.run()