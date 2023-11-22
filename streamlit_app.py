from PIL import Image
import streamlit as st
from source.utils import render_svg
from source.utils import add_spaces
from source.utils import add_header
from source.utils import add_section
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
)

html = {
    "linear gradient": """
        <style>
            div[class='st-emotion-cache-1dp5vir ezrtsby1'] {display:none;}
        </style>
    """,
    "menu": """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """,
}

# Hide the default linear gradient at the top of the page
st.markdown(html["linear gradient"], unsafe_allow_html=True)

# Hide the top right menu and the "Made with Streamlit" footer
st.markdown(html["menu"], unsafe_allow_html=True)

render_svg(open("images/logo.svg").read())
add_spaces(7)

menu = get_menu()
if menu == "sample size":

    add_header(menu)
    add_section("Parameters")
    inputs = get_size_inputs()
    add_calculate_button()
    wait_file(inputs)

    if inputs.test == "Proportions" or inputs.file is not None:
        add_section("Results")
        statistics = calculate_size(inputs)
        show_size_result(i=inputs, s=statistics)

elif menu == "statistical significance":

    add_header(menu)
    add_section("Parameters")
    inputs = get_signif_inputs()
    add_calculate_button()
    wait_file(inputs)

    if inputs.test == "Proportions" or inputs.file is not None:
        add_section("Results")
        statistics = evaluate_signif(inputs)
        show_signif_result(i=inputs, s=statistics)
