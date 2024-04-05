import os

from PIL import Image
import streamlit as st
from streamlit_navigation_bar import st_navbar

import pages as pg
from source.utils import stylized_container


# Set browser tab title, favicon and menu options
st.set_page_config(
    page_title="abtester",
    page_icon=Image.open("images/icon.png"),
    initial_sidebar_state="collapsed",
)

pages = ["Size", "Significance", "GitHub"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "images/icon.svg")
urls = {
    "GitHub": "https://github.com/gabrieltempass/ab-tester"
}
styles = {
    "nav": {"background-color": "#4285f4"},
    "div": {"max-width": "500px"},
    "span": {"color": "white"},
}

page = st_navbar(
    pages,
    selected="Size",
    logo_path=logo_path,
    logo_page="Size",
    urls=urls,
    styles=styles,
    options=False,
)

html = (
    """
    <style>
        div[data-testid="stThumbValue"], div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {
            font-family: "Source Sans Pro", sans-serif;
            font-size: 16px;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
    </style>
    """
)

with stylized_container("adjust"):
    st.markdown(html, unsafe_allow_html=True)

functions = {
    "Home": pg.show_home,
    "Size": pg.show_size,
    "Significance": pg.show_significance,
}
go_to = functions.get(page)
if go_to:
    go_to()
