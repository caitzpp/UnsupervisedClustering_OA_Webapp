import streamlit as st
import config
from streamlit.components.v1 import iframe, html

def show_graph():
    st.header('Embedding Explorer')
    st.markdown(f"[Link to Feedback Form]({config.GOOGLE_FORM_URL})")

    # html("""<script>
    # window.TallyConfig = {
    # "formId": "mOpM5M",
    # "popup": {
    #     "width": 500,
    #     "height": 650,
    #     "emoji": {
    #     "text": "👋",
    #     "animation": "wave"
    #     },
    #     "hideTitle": true
    # }
    # };
    # </script>

    # <script async src="https://tally.so/widgets/embed.js"></script>""",
    # width=1400, height=600)
#     html("""<iframe data-tally-src="https://tally.so/embed/mOpM5M?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="200" frameborder="0" marginheight="0" marginwidth="0" title="Example"></iframe>
# <script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>""")
    
    iframe(config.PLOTLY_URL, width=1400, height=1200)

    # form_url = f"{config.EMBEDDING_GOOGLE_FORM_URL}"
    # st.title("Feedback Form")
    html(
           """<iframe data-tally-src="https://tally.so/embed/mOpM5M?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="5031" frameborder="0" marginheight="0" marginwidth="0" title="Embedding Explorer"></iframe>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>""",
scrolling=True    )