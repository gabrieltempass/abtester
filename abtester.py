import os

import streamlit as st
from streamlit_navigation_bar import st_navbar
from PIL import Image

import pages as pg


# Set the browser tab title, favicon and initial sidebar state.
st.set_page_config(
    page_title="abtester",
    page_icon=Image.open("images/icon.png"),
    initial_sidebar_state="collapsed",
)

pages = ["Size", "Significance", "GitHub"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "images/icon_white.svg")
urls = {
    "GitHub": "https://github.com/gabrieltempass/abtester"
}
styles = {
    "nav": {"background-color": "rgb(66, 135, 245)"},
    "div": {"max-width": "31.25rem"},
    "span": {"color": "white"},
}
options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Get the active page from a navigation bar component.
page = st_navbar(
    pages,
    selected="Size",
    logo_path=logo_path,
    logo_page="Size",
    urls=urls,
    styles=styles,
    options=options,
)

# Make CSS adjustments.
st.html(
    """
    <style>
        /* Match the slider font style to the rest of the app */
        div[data-testid="stThumbValue"],
        div[data-testid="stTickBarMin"],
        div[data-testid="stTickBarMax"] {
            font-family: "Source Sans Pro", sans-serif;
            font-size: 16px;
        }
        /* Prevent layout shift caused by scrollbars
        https://github.com/streamlit/streamlit/issues/8504 */
        section.main {
            overflow-y: scroll;
        }
    </style>
    """
)

# Map page names to functions with their respective content.
functions = {
    "Size": pg.size,
    "Significance": pg.significance,
}
show_page = functions.get(page)
if show_page:
    # Display the content of the active page.
    show_page()
