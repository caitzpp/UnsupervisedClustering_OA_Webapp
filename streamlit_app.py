import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
from streamlit.components.v1 import iframe
import config

# from pages import plotly_page, cluster_page, home, about

st.set_page_config(page_title="Cluster Dashboard", page_icon=":material/dashboard:", layout="wide")



selected = option_menu(
    menu_title = "Main Menu",
    options = ["Home","Embedding Explorer", "Cluster Gallery", "About"],
    icons = [":material/Home:","microscope","art", "info-circle"],
    menu_icon = "cast",
    default_index = 0,
    #orientation = "horizontal",
)
    
# home_page = st.Page(home, title = "Home")
# plotly_page = st.Page(plotly_page, title = "Embedding Explorer")
# # cluster_page = st.Page(cluster_page, title = "Cluster Gallery")
# about_page = st.Page(about, title = "About")

if selected == "Home":
    st.header('xxx')

    with open("content/home.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()
    st.markdown(markdown_text, unsafe_allow_html=True)
    # Load markdown file
    # with open("README.md", "r", encoding="utf-8") as f:
    #     markdown_text = f.read()

    # # Display it in the app
    # st.markdown(markdown_text, unsafe_allow_html=True)
   
        
    
if selected == "Embedding Explorer":
    st.header('Embedding Explorer')
    iframe(config.PLOTLY_URL, width=1800, height=1000)
  

    
# if selected == "Cluster Gallery":

if selected == "About":
    st.header('About')
    with open("content/about.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()
    st.markdown(markdown_text, unsafe_allow_html=True)
 
