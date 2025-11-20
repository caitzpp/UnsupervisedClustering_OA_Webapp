import streamlit as st
import config
from streamlit.components.v1 import iframe, html



def show_graph():
    st.header('Embedding Explorer')
    
    with open("streamlit_app/content/plotly_page.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()

    st.markdown(markdown_text, unsafe_allow_html=True)  

    col1, col2 = st.columns([3, 2])
    with col1:
        iframe(config.PLOTLY_URL, width=1400, height=1200)

    with col2:
        html(

            """
            <script async src="https://tally.so/widgets/embed.js"></script>

            <!-- Add your button with the data attributes -->
            <button 
            data-tally-open="mOpM5M" 
            data-tally-width="1000" 
            data-tally-emoji-text="👋" 
            data-tally-emoji-animation="wave"
            style="
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            "
            >
            Open Feedback Form
            </button>
            """
            , height=1200, 
        # scrolling=True
            )



 
