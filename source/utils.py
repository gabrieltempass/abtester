import base64

import streamlit as st


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" width="300" alt="abtester logo"/>' % b64
    c = st.container()
    c.write(html, unsafe_allow_html=True)
    return


def add_spaces(n):
    for i in range(n):
        st.write("")


def add_header(menu):
    add_spaces(3)
    st.header(menu.capitalize())


def add_subheader(subheader):
    add_spaces(3)
    st.subheader(subheader)


def add_calculate_button():
    if not st.button("Calculate", type="primary"):
        st.stop()


def wait_file(inputs):
    if inputs.df is None and inputs.test == "Means":
        st.error(f"You must choose a file to be able to calculate the {inputs.menu}.")

