import streamlit as st
import config
from streamlit.components.v1 import iframe, html

def show_modal():
    if "force_modal" not in st.session_state:
        st.session_state.force_modal = True

    if st.button("Open Feedback Form"):
        st.session_state.force_modal = True

    if st.session_state.force_modal:
            with st.modal("Feedback Form"):
                iframe(
                    "https://tally.so/r/mOpM5M",
                    height=650
                )

def show_graph():
    st.header('Embedding Explorer')
    
    with open("streamlit_app/content/plotly_page.md", "r", encoding="utf-8") as f:
        markdown_text = f.read()

    st.markdown(markdown_text, unsafe_allow_html=True)  

    show_modal() 
    
    # html(
    # #     """<script async src="https://tally.so/widgets/embed.js"></script>

    # # <script>
    # # function openTallyWhenReady() {
    # #     // If Tally exists, open the popup
    # #     if (window.Tally) {
    # #         Tally.openPopup('mOpM5M', {
    # #             width: 1000,
    # #             hideTitle: false,
    # #             overlay: true,
    # #             autoClose: false
    # #         });
    # #     } else {
    # #         // Try again after 200ms
    # #         setTimeout(openTallyWhenReady, 200);
    # #     }
    # # }

    # # // Ensure we run only after the iframe DOM is ready
    # # setTimeout(openTallyWhenReady, 300);
    # # </script>
    # #     """
    #     """
    #     <script async src="https://tally.so/widgets/embed.js"></script>

    #     <!-- Add your button with the data attributes -->
    #     <button 
    #     data-tally-open="mOpM5M" 
    #     data-tally-width="1000" 
    #     data-tally-emoji-text="👋" 
    #     data-tally-emoji-animation="wave"
    #     style="
    #         background-color: #4CAF50;
    #         color: white;
    #         padding: 10px 20px;
    #         font-size: 16px;
    #         border: none;
    #         border-radius: 8px;
    #         cursor: pointer;
    #     "
    #     >
    #     Open Feedback Form
    #     </button>
    #     """
    #      , height=10, 
    #    # scrolling=True
    #     )

    iframe(config.PLOTLY_URL, width=1400, height=1200)

 
