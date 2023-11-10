from PIL import Image
import streamlit as st

from source.inputs import get_menu_input
from source.inputs import get_test_input
from source.inputs import get_sample_inputs
from source.inputs import get_significance_proportions_inputs
from source.inputs import get_significance_means_inputs

from source.statistics import calculate_sample
from source.statistics import evaluate_proportions_significance
from source.statistics import evaluate_means_significance

from source.results import show_sample_result
from source.results import show_significance_result

from source.utils import render_svg
from source.utils import add_spaces


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

menu = get_menu_input()
if menu == "Calculate the sample size":

    add_spaces(3)
    st.header("Sample size")
    st.divider()
    st.subheader("Parameters")

    (
        test,
        control_conversion,
        sensitivity,
        alternative,
        confidence,
        power,
        control_ratio,
        treatment_ratio,
        df,
        file_name,
        alias,
        test_statistic,
    ) = get_sample_inputs(menu)

    if not st.button("Calculate"):
        st.stop()

    if df is None and test == "Means":
        st.error(
            "You must choose a file to be able to calculate the sample size."
        )
    else:
        control_sample, treatment_sample = calculate_sample(
            test=test,
            control_conversion=control_conversion,
            sensitivity=sensitivity,
            alternative=alternative,
            confidence=confidence,
            power=power,
            control_ratio=control_ratio,
            treatment_ratio=treatment_ratio,
            df=df,
            alias=alias,
            test_statistic=test_statistic,
        )

        show_sample_result(
            menu=menu,
            test=test,
            control_sample=control_sample,
            treatment_sample=treatment_sample,
            control_conversion=control_conversion,
            sensitivity=sensitivity,
            alternative=alternative,
            confidence=confidence,
            power=power,
            control_ratio=control_ratio,
            treatment_ratio=treatment_ratio,
            file_name=file_name,
            alias=alias,
            test_statistic=test_statistic,
        )

if menu == "Evaluate the statistical significance":

    add_spaces(3)
    st.header("Statistical significance")
    st.divider()
    st.subheader("Parameters")
    test = get_test_input()

    if test == "Proportions":

        (
            control_users,
            treatment_users,
            control_conversions,
            treatment_conversions,
            confidence
        ) = get_significance_proportions_inputs()

        if not st.button("Calculate"):
            st.stop()

        st.divider()
        st.subheader("Result")

        (
            control_effect,
            treatment_effect,
            observed_diff,
            alpha,
            p_value,
        ) = evaluate_proportions_significance(
            control_users=control_users,
            treatment_users=treatment_users,
            control_conversions=control_conversions,
            treatment_conversions=treatment_conversions,
            confidence=confidence,
        )
        show_significance_result(
            menu=menu,
            test=test,
            control=control_effect,
            treatment=treatment_effect,
            observed_diff=observed_diff,
            alpha=alpha,
            p_value=p_value,
            control_users=control_users,
            treatment_users=treatment_users,
            control_conversions=control_conversions,
            treatment_conversions=treatment_conversions,
            confidence=confidence,
        )

    elif test == "Means":

        (
            confidence,
            df,
            file_name,
            alias
        ) = get_significance_means_inputs(menu)

        if not st.button("Calculate"):
            st.stop()

        if df is None:
            st.error(
                "You must choose a file to be able to calculate the statistical significance."
            )

        else:

            st.divider()
            st.subheader("Result")
            (
                control_mean,
                treatment_mean,
                observed_diff,
                alpha,
                p_value,
            ) = evaluate_means_significance(
                confidence=confidence,
                df=df,
                alias=alias,
            )
            show_significance_result(
                menu=menu,
                test=test,
                control=control_mean,
                treatment=treatment_mean,
                observed_diff=observed_diff,
                alpha=alpha,
                p_value=p_value,
                confidence=confidence,
                file_name=file_name,
                alias=alias,
            )
