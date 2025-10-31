import streamlit as st
import config
from streamlit.components.v1 import iframe

def show_graph():
    st.header('Embedding Explorer')
    st.markdown(f"[Link to Feedback Form]({config.GOOGLE_FORM_URL})")
    iframe(config.PLOTLY_URL, width=1400, height=1200)

    form_url = f"{config.EMBEDDING_GOOGLE_FORM_URL}"
    st.title("Feedback Form")
    st.markdown(
            f"""
        <iframe src="{form_url}" width="640" height="800" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
        """,
        unsafe_allow_html=True,
    )