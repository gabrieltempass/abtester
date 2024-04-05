import streamlit as st

from source.utils import add_spaces
from source.utils import add_calculate_button
from source.utils import wait_file
from source.inputs import get_size_inputs
from source.statistics import calculate_size
from source.results import show_result


def show_size():

    st.header("Sample size")
    add_spaces(2)
    st.subheader("Parameters")

    inputs = get_size_inputs()
    add_calculate_button()
    wait_file(inputs)

    if inputs.test == "Proportions" or inputs.file is not None:
        add_spaces(2)
        st.subheader("Results")
        statistics = calculate_size(inputs)
        show_result(i=inputs, s=statistics)

