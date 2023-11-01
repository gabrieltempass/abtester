from PIL import Image
from jinja2 import FileSystemLoader, Environment
import pandas as pd
import streamlit as st

from source.inputs import get_menu_input
from source.inputs import get_test_input
from source.inputs import get_sample_inputs
from source.inputs import get_proportions_significance_inputs
from source.inputs import get_means_significance_inputs
from source.inputs import show_file_summary

from source.statistics import percentage
from source.statistics import get_alpha
from source.statistics import get_beta
from source.statistics import permutation
from source.statistics import calculate_sample
from source.statistics import evaluate_proportions_significance
from source.statistics import evaluate_means_significance

from source.results import show_sample_result
from source.results import show_significance_result

from source.utils import render_svg
from source.utils import show_download_button
from source.utils import convert_df


# Set browser tab title, favicon and menu options
st.set_page_config(
    page_title="abtester",
    page_icon=Image.open("images/icon.png"),
)

# Hide the default linear gradient at the top of the page
st.markdown("<style>div[class='st-emotion-cache-1dp5vir ezrtsby1'] {display:none;} </style>", unsafe_allow_html=True)

# Hide top right menu and "Made with Streamlit" footer
hide_menu_style = """
	<style>
	#MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
	</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

render_svg(open("images/logo.svg").read())

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

menu = get_menu_input()
if menu == "Calculate the sample size":

    st.header("Sample size")
    (
        test,
        control_conversion,
        sensitivity,
        alternative,
        confidence_level,
        power,
        control_ratio,
        treatment_ratio,
        df,
        file_name,
    ) = get_sample_inputs()

    if not st.button("Calculate"):
        st.stop()

    control_sample, treatment_sample = calculate_sample(
        test=test,
        control_conversion=control_conversion,
        sensitivity=sensitivity,
        alternative=alternative,
        confidence_level=confidence_level,
        power=power,
        control_ratio=control_ratio,
        treatment_ratio=treatment_ratio,
        df=df,
    )

    show_sample_result(
        control_sample=control_sample,
        treatment_sample=treatment_sample,
        test=test,
        control_conversion=control_conversion,
        file_name=file_name,
        sensitivity=sensitivity,
        alternative=alternative,
        confidence_level=confidence_level,
        power=power,
        control_ratio=control_ratio,
        treatment_ratio=treatment_ratio,
    )

if menu == "Evaluate the statistical significance":

    st.header("Statistical significance")
    test = get_test_input()

    if test == "Proportions":

        (
            control_users,
            treatment_users,
            control_conversions,
            treatment_conversions,
            confidence_level
        ) = get_proportions_significance_inputs()

        if not st.button("Calculate"):
            st.stop()

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
            confidence_level=confidence_level,
        )
        show_significance_result(
            test=test,
            control=control_effect,
            treatment=treatment_effect,
            observed_diff=observed_diff,
            alpha=alpha,
            p_value=p_value,
        )

        loader = FileSystemLoader("templates")
        env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        template = env.get_template("statistical_significance_proportions.py")
        code = template.render(
            test=test,
            control_users=control_users,
            treatment_users=treatment_users,
            control_conversions=control_conversions,
            treatment_conversions=treatment_conversions,
            confidence_level=confidence_level,
        )
        with st.expander("Show the code"):
            st.code(code, language="python")

    elif test == "Means":

        confidence_level, uploaded_file = get_means_significance_inputs()

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            show_file_summary(df)
        else:
            st.write(
                'The file must have each row with a unique user. One column named "group", with the user classification as "control" or "treatment". And one column named "measurement", with the value of the metric for the respective user. Below is an example of how the file should look like:'
            )

            path = "sample_datasets/statistical_significance/"
            df_format = pd.read_csv(f"{path}format.csv")
            st.dataframe(df_format, height=230, use_container_width=True, hide_index=True)

            st.write("Don't have a CSV file available? Download one of the sample datasets below and try it out.")

            show_download_button("dataset 1", path, "dataset_1.csv")
            show_download_button("dataset 2", path, "dataset_2.csv")
            show_download_button("dataset 3", path, "dataset_3.csv")

        if not (st.button("Calculate")):
            st.stop()

        if uploaded_file is None:
            st.error(
                "You must choose a file to be able to calculate the statistical significance."
            )

        else:

            (
                control_mean,
                treatment_mean,
                observed_diff,
                alpha,
                p_value,
            ) = evaluate_means_significance(
                confidence_level=confidence_level,
                df=df,
            )
            show_significance_result(
                test=test,
                control=control_mean,
                treatment=treatment_mean,
                observed_diff=observed_diff,
                alpha=alpha,
                p_value=p_value,
            )

            loader = FileSystemLoader("templates")
            env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
            template = env.get_template("statistical_significance_means.py")
            code = template.render(
                file_name=uploaded_file.name,
                test=test,
                confidence_level=confidence_level,
            )
            with st.expander("Show the code"):
                st.code(code, language="python")
