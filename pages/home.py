import streamlit as st
import config

def show_home():
    st.header('Home')

    st.markdown(f"For feedback please use the following form: [Link]({config.GOOGLE_FORM_URL})")

    with open("content/home.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()
    st.markdown(markdown_text, unsafe_allow_html=True)