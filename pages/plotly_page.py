import streamlit as st
import config
from streamlit.components.v1 import iframe

def main():
    st.header('Embedding Explorer')
    iframe(config.PLOTLY_URL, width=700, height=600)