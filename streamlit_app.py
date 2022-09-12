from PIL import Image
import random
import math
import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.stats.api as sms
from jinja2 import FileSystemLoader, Environment
import streamlit as st


def percentage(number):
    return number / 100


def get_alpha(confidence_level):
    return 1 - confidence_level


def get_beta(power):
    return 1 - power


def calculate_proportions_sample(
    control_conversion,
    sensitivity,
    alternative,
    confidence_level,
    power,
):
    treatment_conversion = control_conversion * (1 + sensitivity)
    alpha = get_alpha(confidence_level)

    # Cohen's h
    effect_size = sms.proportion_effectsize(control_conversion,
                                            treatment_conversion)
    analysis = sms.TTestIndPower()
    treatment_sample = math.ceil(analysis.solve_power(
        effect_size,
        alternative=alternative,
        alpha=alpha,
        power=power,
        ratio=1,
    ))
    control_sample = treatment_sample

    return control_sample, treatment_sample


def calculate_means_sample(
    sensitivity,
    confidence_level,
    power,
    control_ratio,
    treatment_ratio,
    df,
):
    alpha = get_alpha(confidence_level)
    beta = get_beta(power)

    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(1 - beta)
    a = 1 / control_ratio + 1 / treatment_ratio
    b = pow(z_alpha + z_beta, 2)

    std_dev = df["measurement"].std()

    total_sample = math.ceil(a * b / pow(sensitivity / std_dev, 2))
    control_sample = math.ceil(total_sample * control_ratio)
    treatment_sample = math.ceil(total_sample * treatment_ratio)

    return control_sample, treatment_sample


def show_sample_result(control_sample, treatment_sample):
    st.subheader("Result")
    st.write(f"Minimum sample for the control group: {control_sample}")
    st.write(f"Minimum sample for the treatment group: {treatment_sample}")
    st.write(f"Total minimum sample for the experiment: {control_sample + treatment_sample}")


def show_file_summary(df, option):
    st.write("**File summary**")
    st.write(f"Size: {df.shape[0]} rows and {df.shape[1]} columns")

    if option == "Evaluate the statistical significance":
        control_users = df[df["group"] == "control"].shape[0]
        treatment_users = df[df["group"] == "treatment"].shape[0]
        total_users = control_users + treatment_users

        control_ratio = control_users / total_users
        treatment_ratio = treatment_users / total_users
        st.write(f"Ratio: {control_users} control users ({control_ratio:.2%}) and {treatment_users} treatment users ({treatment_ratio:.2%})")

    st.write("Preview of the first 5 rows:")
    st.table(df.head(5))
    st.write("And the last 5 rows:")
    st.table(df.tail(5))


def show_download_button(name, path, file):
    df = pd.read_csv(path+file)
    df = convert_df(df)
    st.download_button(
        label=f"Download {name}",
        data=df,
        file_name=file,
        mime="text/csv",
    )


@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def permutation(x, nA, nB):
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[idx_B].mean() - x.loc[idx_A].mean()


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
	MainMenu {visibility: hidden; }
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

description = {
    "test": "A proportions test is when the data can be expressed in discrete binary values. For example: the conversions of a web page (when the user does not convert it is a zero and when he or she converts it is a one).\n\nA means test is when the data is continuous. For example: the time spent in a web page.",
    "control_conversion": "The conversion rate expected for the control. To help you set this value, you could use similar historical data. However, if that it is not available, make a guess based on your experience.",
    "sensitivity": "The minimum effect size that you want to be able to measure. A rule of thumb is to use 10% (meaning that you want to be able to detect at least a 10% difference for the treatment over the control).",
    "alternative": "A one-sided hypothesis is to test whether one group has a distribution greater then the other. While a two-sided is to test whether one group has a distribution smaller or greater then the other. If you are not sure about which one to use, choose the two-sided (more conservative).",
    "confidence_level": "The probability of detecting a true negative. That is, detecting that there is not a statistically significant difference between the control and the treatment, when this difference indeed does not exists. A rule of thumb is to use 95%.",
    "power": "The probability of detecting a true positive. That is, detecting that there is a statistically significant difference between the control and the treatment, when this difference indeed exists. A rule of thumb is to use 80%.",
    "control_users": "The number of users in the control group.",
    "treatment_users": "The number of users in the treatment group.",
    "control_conversions": "The number of users in the control group that converted. For example, if the control group received an email, the conversions could the number of users that clicked in an ad inside it.",
    "treatment_conversions": "The number of users in the treatment group that converted. For example, if the treatment group received an email, the conversions could the number of users that clicked in an ad inside it.",
    "control_ratio": "The percentage of users from the entire experiment who are part of the control group.",
    "treatment_ratio": "The percentage of users from the entire experiment who are part of the treatment group.",
}

loader = FileSystemLoader("templates")
env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

if option == "Calculate the minimum sample size":
    st.header("Sample size")

    template = env.get_template("calculate_sample.py")

    test = st.radio(
        label="Test",
        options=("Proportions", "Means"),
        index=0,
        key="sample-size",
        horizontal=True,
        help=description["test"],
    )

    if test == "Proportions":

        control_conversion = percentage(
            st.number_input(
                label="Baseline conversion rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=15.0,
                step=0.1,
                format="%.1f",
                help=description["control_conversion"],
            )
        )

        sensitivity = percentage(
            st.number_input(
                label="Sensitivity (%)",
                min_value=0.0,
                value=10.0,
                step=0.1,
                format="%.1f",
                help=description["sensitivity"],
            )
        )

        alternative = st.radio(
            label="Hypothesis",
            options=("smaller", "two-sided"),
            index=1,
            key="pre-test",
            horizontal=True,
            format_func=lambda x: {"smaller": "One-sided", "two-sided": "Two-sided"}.get(x),
            help=description["alternative"],
        )

        confidence_level = percentage(
            st.slider(
                label="Confidence level",
                min_value=70,
                max_value=99,
                value=95,
                format="%d%%",
                key="pre-test-proportions",
                help=description["confidence_level"],
            )
        )

        power = percentage(
            st.slider(
                label="Power",
                min_value=70,
                max_value=99,
                value=80,
                format="%d%%",
                help=description["power"],
            )
        )

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

        sensitivity = percentage(
            st.number_input(
                label="Sensitivity (%)",
                min_value=0.0,
                value=10.0,
                step=0.1,
                format="%.1f",
                help=description["sensitivity"],
            )
        )

        confidence_level = percentage(
            st.slider(
                label="Confidence level",
                min_value=70,
                max_value=99,
                value=95,
                format="%d%%",
                key="pre-test-means",
                help=description["confidence_level"],
            )
        )

        power = percentage(
            st.slider(
                label="Power",
                min_value=70,
                max_value=99,
                value=80,
                format="%d%%",
                help=description["power"],
            )
        )

        col_1, col_2 = st.columns(2)

        control_ratio = percentage(
            col_1.number_input(
                label="Control ratio (%)",
                min_value=0.1,
                max_value=99.9,
                value=50.0,
                step=0.1,
                format="%.1f",
                help=description["control_ratio"],
            )
        )

        treatment_ratio = percentage(
            col_2.number_input(
                label="Treatment ratio (%)",
                min_value=0.1,
                max_value=99.9,
                value=100.0 - control_ratio * 100,
                step=0.1,
                format="%.1f",
                help=description["treatment_ratio"],
                disabled=True,
            )
        )

        uploaded_file = st.file_uploader("Choose a CSV file")

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
    st.header("Statistical significance")

    template = env.get_template("evaluate_significance.py")

    test = st.radio(
        label="Test",
        options=("Proportions", "Means"),
        index=0,
        key="statistical-significance",
        horizontal=True,
        help=description["test"],
    )

    if test == "Proportions":

        control_users = st.number_input(
            label="Users in the control",
            min_value=0,
            value=30000,
            step=1,
            help=description["control_users"],
        )

        treatment_users = st.number_input(
            label="Users in the treatment",
            min_value=0,
            value=30000,
            step=1,
            help=description["treatment_users"],
        )

        control_conversions = st.number_input(
            label="Conversions from the control",
            min_value=0,
            value=1215,
            step=1,
            help=description["control_conversions"],
        )

        treatment_conversions = st.number_input(
            label="Conversions from the treatment",
            min_value=0,
            value=1294,
            step=1,
            help=description["treatment_conversions"],
        )

        confidence_level = st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            key="post-test-proportions",
            help=description["confidence_level"],
        )

        confidence_level = percentage(confidence_level)
        alpha = get_alpha(confidence_level)

        if not (st.button("Calculate")):
            st.stop()

        control_effect = control_conversions / control_users
        treatment_effect = treatment_conversions / treatment_users
        observed_diff = treatment_effect - control_effect

        conversion = [0] * (control_users + treatment_users)
        conversion.extend([1] * (control_conversions + treatment_conversions))
        conversion = pd.Series(conversion)

        perm_diffs = []
        i = 1000
        my_bar = st.progress(0)
        for percent_complete in range(i):
            perm_diffs.append(
                permutation(
                    conversion,
                    control_users + control_conversions,
                    treatment_users + treatment_conversions,
                )
            )
            my_bar.progress((percent_complete + 1) / i)

        p_value = np.mean([diff > observed_diff for diff in perm_diffs])

        st.subheader("Result")
        if p_value <= alpha:
            st.success("The difference is statistically significant")
        else:
            st.error("The difference is not statistically significant")
        st.write(f"Control conversion: {control_effect:.2%}")
        st.write(f"Treatment conversion: {treatment_effect:.2%}")
        st.write(
            f"Observed difference: {observed_diff * 100:+.2f} p.p. ({observed_diff / control_effect:+.2%})"
        )
        st.write(f"p-value: {p_value:.2f}")

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

        confidence_level = st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            key="post-test-means",
            help=description["confidence_level"],
        )

        uploaded_file = st.file_uploader("Choose a CSV file")
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
            confidence_level = percentage(confidence_level)
            alpha = get_alpha(confidence_level)

            measurements = df["measurement"]
            control_users = df[df["group"] == "control"].shape[0]
            treatment_users = df[df["group"] == "treatment"].shape[0]

            control_mean = df[df["group"] == "control"]["measurement"].mean()
            treatment_mean = df[df["group"] == "treatment"]["measurement"].mean()
            observed_diff = treatment_mean - control_mean

            perm_diffs = []
            i = 1000
            my_bar = st.progress(0)
            for percent_complete in range(i):
                perm_diffs.append(
                    permutation(measurements, control_users, treatment_users)
                )
                my_bar.progress((percent_complete + 1) / i)

            p_value = np.mean([diff > abs(observed_diff) for diff in perm_diffs])

            st.subheader("Result")
            if p_value <= alpha:
                st.success("The difference is statistically significant")
            else:
                st.error("The difference is not statistically significant")
            st.write(f"Control mean: {control_mean:.2f}")
            st.write(f"Treatment mean: {treatment_mean:.2f}")
            st.write(f"Observed difference: {observed_diff / control_mean:+.2%}")
            st.write(f"p-value: {p_value:.2f}")

            code = template.render(test=test, confidence_level=confidence_level)
            with st.expander("Show the code"):
                st.code(code, language="python")
