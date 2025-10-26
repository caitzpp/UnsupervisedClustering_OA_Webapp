import streamlit as st

def show_home():
    st.header('Home')

    with open("content/home.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()
    st.markdown(markdown_text, unsafe_allow_html=True)