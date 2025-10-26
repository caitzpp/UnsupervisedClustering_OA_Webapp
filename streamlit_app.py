import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
from streamlit.components.v1 import iframe
import config

from pages import plotly_page, cluster_page, home, about


# selected = option_menu(
#     menu_title = "Main Menu",
#     options = ["Home","Embedding Explorer", "Cluster Gallery", "About"],
#     icons = [":material/Home:","microscope","art", "info-circle"],
#     menu_icon = "cast",
#     default_index = 0,
#     #orientation = "horizontal",
# )
    
home_page = st.Page(home.main, title = "Home", icon=":material/home:")
graph_page = st.Page(plotly_page.main, title = "Embedding Explorer")
as_page = st.Page(cluster_page.main, title = "Cluster Gallery")
about_page = st.Page(about.main, title = "About")


pg = st.navigation([home_page, graph_page, as_page, about_page])
st.set_page_config(layout="wide") #page_title="Cluster Dashboard", page_icon=":material/dashboard:", 

# if selected == "Home":
#     st.header('xxx')

#     with open("content/home.md", "r", encoding="utf-8") as f:
#         markdown_text = f.read()
#     st.markdown(markdown_text, unsafe_allow_html=True)
#     # Load markdown file
#     # with open("README.md", "r", encoding="utf-8") as f:
#     #     markdown_text = f.read()

#     # # Display it in the app
#     # st.markdown(markdown_text, unsafe_allow_html=True)
   
        
    
# if selected == "Embedding Explorer":
#     st.header('Embedding Explorer')
#     iframe(config.PLOTLY_URL, width=1800, height=1000)
  

    
# # if selected == "Cluster Gallery":

# if selected == "About":
#     st.header('About')
#     with open("content/about.md", "r", encoding="utf-8") as f:
#         markdown_text = f.read()
#     st.markdown(markdown_text, unsafe_allow_html=True)
 

if __name__ == "__main__":
    pg.run()