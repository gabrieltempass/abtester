from PIL import Image
from jinja2 import FileSystemLoader, Environment
import pandas as pd
import streamlit as st

from source.inputs import get_proportions_sample_inputs
from source.inputs import get_means_sample_inputs
from source.inputs import get_proportions_significance_inputs
from source.inputs import get_means_significance_inputs

from source.statistics import calculate_proportions_sample
from source.statistics import calculate_means_sample
from source.statistics import evaluate_proportions_significance
from source.statistics import evaluate_means_significance

from source.utils import percentage
from source.utils import get_alpha
from source.utils import get_beta
from source.utils import show_sample_result
from source.utils import show_file_summary
from source.utils import show_download_button
from source.utils import convert_df
from source.utils import permutation


# Set browser tab title, favicon and menu options
about = """
This app was made by Gabriel Tem Pass. You can check the source code at [https://github.com/gabrieltempass/ab-tester](https://github.com/gabrieltempass/ab-tester).

If you would like to provide feedback, learn more about the A/B Tester, or anything else, feel free to send an email to contact@abtester.app.
"""
st.set_page_config(
    page_title="A/B Tester",
    page_icon=Image.open("images/favicon.png"),
    menu_items={
        "Get help": "https://gitter.im/ab-tester-app/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link",
        "Report a bug": "https://github.com/gabrieltempass/ab-tester/issues/new?title=Your%20issue%20title%20here&body=Your%20issue%20description%20here.",
        "About": about,
    },
)

# Hide top right menu and "Made with Streamlit" footer
hide_menu_style = """
	<style>
	#MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
	</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("A/B Tester")
option = st.selectbox(
    "What do you want to do?",
    (
        "Select an option",
        "Calculate the minimum sample size",
        "Evaluate the statistical significance",
    ),
)

description = "A proportions test is when the data can be expressed in discrete binary values. For example: the conversions of a web page (when the user does not convert it is a zero and when he or she converts it is a one).\n\nA means test is when the data is continuous. For example: the time spent in a web page."

loader = FileSystemLoader("templates")
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

if option == "Calculate the minimum sample size":
    template = env.get_template("calculate_sample.py")

    st.header("Sample size")
    test = st.radio(
        label="Test",
        options=("Proportions", "Means"),
        index=0,
        key="sample-size",
        horizontal=True,
        help=description,
    )

    if test == "Proportions":
        (
            control_conversion,
            sensitivity,
            alternative,
            confidence_level,
            power,
        ) = get_proportions_sample_inputs()

        if not (st.button("Calculate")):
            st.stop()

        control_sample, treatment_sample = calculate_proportions_sample(
            control_conversion=control_conversion,
            sensitivity=sensitivity,
            alternative=alternative,
            confidence_level=confidence_level,
            power=power
        )

        show_sample_result(control_sample, treatment_sample)

        code = template.render(
            test=test,
            control_conversion=control_conversion,
            sensitivity=sensitivity,
            alternative=alternative,
            confidence_level=confidence_level,
            power=power,
        )
        with st.expander("Show the code"):
            st.code(code, language="python")

    elif test == "Means":

        (
            sensitivity,
            confidence_level,
            power,
            uploaded_file
        ) = get_means_sample_inputs()

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            show_file_summary(df, option)
        else:
            st.write(
                'The file must have each row with a unique user. And one column named "measurement", with the value of the metric for the respective user. Below is an example of how the file should look like:'
            )

            path = "sample_datasets/minimum_sample/"
            df_format = pd.read_csv(f"{path}format.csv")
            st.table(df_format)

            st.write("Don't have a CSV file available? Download one of the sample datasets below and try it out.")

            show_download_button("dataset A", path, "dataset_a.csv")
            show_download_button("dataset B", path, "dataset_b.csv")
            show_download_button("dataset C", path, "dataset_c.csv")

        if not (st.button("Calculate")):
            st.stop()

        if uploaded_file is None:
            st.error(
                "You must choose a file to be able to calculate the minimum sample."
            )

        else:

            control_sample, treatment_sample = calculate_means_sample(
                sensitivity=sensitivity,
                confidence_level=confidence_level,
                power=power,
                control_ratio=control_ratio,
                treatment_ratio=treatment_ratio,
                df=df,
            )

            show_sample_result(control_sample, treatment_sample)

            code = template.render(
                test=test,
                sensitivity=sensitivity,
                confidence_level=confidence_level,
                power=power,
                control_ratio=control_ratio,
            )
            with st.expander("Show the code"):
                st.code(code, language="python")

if option == "Evaluate the statistical significance":
    template = env.get_template("evaluate_significance.py")    

    st.header("Statistical significance")
    test = st.radio(
        label="Test",
        options=("Proportions", "Means"),
        index=0,
        key="statistical-significance",
        horizontal=True,
        help=description,
    )

    if test == "Proportions":

        (
            control_users,
            treatment_users,
            control_conversions,
            treatment_conversions,
            confidence_level
        ) = get_proportions_significance_inputs()

        if not (st.button("Calculate")):
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

        st.subheader("Result")
        if p_value <= alpha:
            st.success("The difference is statistically significant")
            comparison = {
                "direction": "less than or equal to",
                "significance": "is"
            }
        else:
            st.error("The difference is not statistically significant")
            comparison = {
                "direction": "greater than",
                "significance": "is not"
            }

        prefix = "~" if round(p_value, 4) == 0 else ""
        st.write(f"Control conversion: {control_effect:.2%}")
        st.write(f"Treatment conversion: {treatment_effect:.2%}")
        st.write(f"Observed difference: {observed_diff * 100:+.2f} p.p. ({observed_diff / control_effect:+.2%})")
        st.write(f"Alpha: {alpha:.4f}")
        st.write(f"p-value: {prefix}{p_value:.4f}")
        st.write(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")

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
            show_file_summary(df, option)
        else:
            st.write(
                'The file must have each row with a unique user. One column named "group", with the user classification as "control" or "treatment". And one column named "measurement", with the value of the metric for the respective user. Below is an example of how the file should look like:'
            )

            path = "sample_datasets/statistical_significance/"
            df_format = pd.read_csv(f"{path}format.csv")
            st.table(df_format)

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

            st.subheader("Result")
            if p_value <= alpha:
                st.success("The difference is statistically significant")
                comparison = {
                    "direction": "less than or equal to",
                    "significance": "is"
                }
            else:
                st.error("The difference is not statistically significant")
                comparison = {
                    "direction": "greater than",
                    "significance": "is not"
                }

            prefix = "~" if round(p_value, 4) == 0 else ""
            st.write(f"Control mean: {control_mean:.2f}")
            st.write(f"Treatment mean: {treatment_mean:.2f}")
            st.write(f"Observed difference: {observed_diff / control_mean:+.2%}")
            st.write(f"Alpha: {alpha:.4f}")
            st.write(f"p-value: {prefix}{p_value:.4f}")
            st.write(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")

            code = template.render(test=test, confidence_level=confidence_level)
            with st.expander("Show the code"):
                st.code(code, language="python")
