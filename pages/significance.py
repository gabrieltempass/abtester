import streamlit as st

from source.utils import add_spaces
from source.utils import add_calculate_button
from source.utils import wait_file
from source.inputs import get_signif_inputs
from source.statistics import evaluate_signif
from source.results import show_result


def show_significance():

    st.header("Statistical significance")
    add_spaces(2)
    st.subheader("Parameters")

    inputs = get_signif_inputs()
    add_calculate_button()
    wait_file(inputs)

    if inputs.test == "Proportions" or inputs.file is not None:
        add_spaces(2)
        st.subheader("Results")
        statistics = evaluate_signif(inputs)
        show_result(i=inputs, s=statistics)

