import streamlit as st

from source.utils import add_spaces, add_calculate_button, wait_file
from source.inputs import get_size_inputs
from source.statistics import calculate_size
from source.results import show_result


def show_size():

    st.header("Sample size")
    st.write(
        """
        A hypothesis test must use a large enough sample, so that an effect
        with practical significance has a high probability of being detected
        from the study. To calculate the minimum sample size required for your
        experiment, enter the parameters below.
        """
    )
    add_spaces(1)
    st.subheader("Parameters")

    inputs = get_size_inputs()
    add_calculate_button()
    wait_file(inputs)

    if inputs.test == "Proportions" or inputs.file is not None:
        add_spaces(1)
        st.subheader("Results")
        statistics = calculate_size(inputs)
        show_result(i=inputs, s=statistics)
