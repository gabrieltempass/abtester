import streamlit as st

from source.utils import add_spaces, add_calculate_button, wait_file
from source.inputs import get_signif_inputs
from source.statistics import evaluate_signif
from source.results import show_result


def significance():

    st.header("Statistical significance")
    st.write(
        """
        In a properly designed hypothesis test, an observed difference between
        two groups must be either due to a real effect or to random chance. To
        evaluate if the difference in your experiment is statistically
        significant, enter the parameters below.
        """
    )
    add_spaces(1)

    st.subheader("Parameters")
    inputs = get_signif_inputs()
    add_calculate_button()
    wait_file(inputs)
    add_spaces(1)

    if inputs.test == "Proportions" or inputs.file is not None:
        st.subheader("Results")
        statistics = evaluate_signif(inputs)
        show_result(i=inputs, s=statistics)
