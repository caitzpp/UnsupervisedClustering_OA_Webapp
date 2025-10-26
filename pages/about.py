import streamlit as st

def show_about():
    st.header('About')
    with open("content/about.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()
    st.markdown(markdown_text, unsafe_allow_html=True)