import streamlit as st
import config
from streamlit.components.v1 import iframe

def show_graph():
    st.header('Embedding Explorer')
    iframe(config.PLOTLY_URL, width=1400, height=1200)

    # form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe7q4a-ze55KQfCmE1tGtyN42_UkGl_LYXAcgKXGnPiSPbq6Q/viewform?embedded=true"
    # st.title("Feedback Form")
    # st.markdown(
    #         f"""
    #     <iframe src="{form_url}" width="640" height="800" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    #     """,
    #     unsafe_allow_html=True,
    # )