import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
from streamlit.components.v1 import iframe
import config

from pages import plotly_page, cluster_page, home, about


home_page = st.Page(home.show_home, title = "Home", icon=":material/home:")
graph_page = st.Page(plotly_page.show_graph, title = "Embedding Explorer")
as_page = st.Page(cluster_page.show_clusterpage, title = "Cluster Gallery")
about_page = st.Page(about.show_about, title = "About")


pg = st.navigation([home_page, graph_page, as_page, about_page])
st.set_page_config(layout="wide") #page_title="Cluster Dashboard", page_icon=":material/dashboard:", 
 

if __name__ == "__main__":
    pg.run()