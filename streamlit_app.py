from PIL import Image
import streamlit as st

from source.utils import render_svg
from source.utils import add_spaces
from source.utils import add_header
from source.utils import add_subheader
from source.utils import add_calculate_button
from source.utils import wait_file
from source.inputs import get_menu
from source.inputs import get_size_inputs
from source.inputs import get_signif_inputs
from source.statistics import calculate_size
from source.statistics import evaluate_signif
from source.results import show_size_result
from source.results import show_signif_result


# Set browser tab title, favicon and menu options
st.set_page_config(
    page_title="abtester",
    page_icon=Image.open("images/icon.png"),
    initial_sidebar_state="collapsed",
)

html = {
    "hide_decoration": """
        <style>
            #stDecoration {
                visibility: hidden;
            }
        </style>
    """,
    "hide_menu": """
        <style>
            #MainMenu {
                visibility: hidden;
            }
        </style>
    """,
    "hide_footer": """
        <style>
            footer {
                visibility: hidden;
            }
        </style>
    """,
    "change_slider_font": """
        <style>
            div[data-testid="stThumbValue"], div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {
                font-family: "Source Sans Pro", sans-serif;
                font-size: 16px;
            }
        </style>
    """,
}

st.markdown(html["hide_decoration"], unsafe_allow_html=True)
st.markdown(html["hide_menu"], unsafe_allow_html=True)
st.markdown(html["hide_footer"], unsafe_allow_html=True)
st.markdown(html["change_slider_font"], unsafe_allow_html=True)

render_svg(open("images/logo.svg").read())
add_spaces(7)

menu = get_menu()
if menu == "sample size":

    add_header(menu)
    add_subheader("Parameters")
    inputs = get_size_inputs()
    add_calculate_button()
    wait_file(inputs)

    if inputs.test == "Proportions" or inputs.file is not None:
        add_subheader("Results")
        statistics = calculate_size(inputs)
        show_size_result(i=inputs, s=statistics)

elif menu == "statistical significance":

    add_header(menu)
    add_subheader("Parameters")
    inputs = get_signif_inputs()
    add_calculate_button()
    wait_file(inputs)

    if inputs.test == "Proportions" or inputs.file is not None:
        add_subheader("Results")
        statistics = evaluate_signif(inputs)
        show_signif_result(i=inputs, s=statistics)
