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


def alpha(confidence_level):
    return 1 - confidence_level


def beta(power):
    return 1 - power


def proportion_ttest(control_conversion, treatment_conversion, alternative, alpha, power):
    # Cohen's h
    effect_size = sms.proportion_effectsize(control_conversion,
                                            treatment_conversion)
    analysis = sms.TTestIndPower()
    sample = math.ceil(analysis.solve_power(
        effect_size,
        alternative=alternative,
        alpha=alpha,
        power=power,
        ratio=1,
    ))
    return sample


def permutation(x, nA, nB):
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[idx_B].mean() - x.loc[idx_A].mean()


# def mean_ztest(df, sensitivity, alpha, beta):
# 	control_users = df[df['group'] == 'control'].shape[0]
# 	treatment_users = df[df['group'] == 'treatment'].shape[0]
# 	total_users = (control_users + treatment_users)
# 	std = df[df['group'] == 'control']['measurement'].std()
#   
# 	q0 = control_users/total_users
# 	q1 = treatment_users/total_users
# 	z_alpha = norm.ppf(1 - alpha/2)
# 	z_beta = norm.ppf(1 - beta)
# 	a = 1/q1 + 1/q0
# 	b = pow(z_alpha + z_beta, 2)
#   
# 	sample = math.ceil(a*b/pow(sensitivity/std, 2))
# 	return sample


# def calculate_sample(test):
# 	if test == 'Proportions':
# 		sample = proportion_ttest()
# 	elif test == 'Means':
# 		sample = mean_ztest()
# 	return sample


# def evaluate_significance():

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

        treatment_conversion = control_conversion * (1 + sensitivity)
        alpha = alpha(confidence_level)

        if not (st.button("Calculate")):
            st.stop()

        sample = proportion_ttest(
            control_conversion=control_conversion,
            treatment_conversion=treatment_conversion,
            alternative=alternative,
            alpha=alpha,
            power=power
        )

        st.subheader("Result")
        st.write(f"Minimum sample for the control group: {sample}")
        st.write(f"Minimum sample for the treatment group: {sample}")
        st.write(f"Total minimum sample for the experiment: {sample*2}")

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

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("File uploaded. Preview of the first 10 rows:")
            st.table(df.head(10))
        else:
            st.write(
                'The file must have each row with a unique user. One column named "group", with the user classification as "control" or "treatment". And one column named "measurement", with the value of the metric for the respective user. Below is an example of how the file should look like:'
            )
            data_sample = pd.read_csv("data_sample.csv")
            st.table(data_sample)

        sensitivity = st.number_input(
            label="Sensitivity (%)",
            min_value=0.0,
            value=10.0,
            step=0.1,
            format="%.1f",
            help=description["sensitivity"],
        )

        confidence_level = st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            key="pre-test-means",
            help=description["confidence_level"],
        )

        power = st.slider(
            label="Power",
            min_value=70,
            max_value=99,
            value=80,
            format="%d%%",
            help=description["power"],
        )

        # Format the variables according to the function requirements
        sensitivity = percentage(sensitivity)
        alternative = "two-sided"
        confidence_level = percentage(confidence_level)
        alpha = alpha(confidence_level)
        power = percentage(power)
        beta = beta(power)

        if not (st.button("Calculate")):
            st.stop()

        if uploaded_file is None:
            st.error(
                "You must choose a file to be able to calculate the minimum sample."
            )

        else:
            control_users = df[df["group"] == "control"].shape[0]
            treatment_users = df[df["group"] == "treatment"].shape[0]
            total_users = control_users + treatment_users

            std = df[df["group"] == "control"]["measurement"].std()
            # std = 2

            q0 = control_users / total_users
            q1 = treatment_users / total_users
            z_alpha = norm.ppf(1 - alpha / 2)
            z_beta = norm.ppf(1 - beta)
            a = 1 / q1 + 1 / q0
            b = pow(z_alpha + z_beta, 2)

            sample = math.ceil(a * b / pow(sensitivity / std, 2))

            st.subheader("Result")
            st.write(f"Minimum sample for the control group: {sample}")
            st.write(f"Minimum sample for the treatment group: {sample}")
            st.write(f"Total minimum sample for the experiment: {sample*2}")

            code = template.render(
                test=test,
                sensitivity=sensitivity,
                confidence_level=confidence_level,
                power=power,
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
        alpha = alpha(confidence_level)

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
            f"Observed difference: {observed_diff*100:+.2f} p.p. ({observed_diff/control_effect:+.2%})"
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

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("File uploaded. Preview of the first 10 rows:")
            st.table(df.head(10))
        else:
            st.write(
                'The file must have each row with a unique user. One column named "group", with the user classification as "control" or "treatment". And one column named "measurement", with the value of the metric for the respective user. Below is an example of how the file should look like:'
            )
            data_sample = pd.read_csv("data_sample.csv")
            st.table(data_sample)

        confidence_level = st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            key="post-test-means",
            help=description["confidence_level"],
        )

        confidence_level = percentage(confidence_level)
        alpha = alpha(confidence_level)

        if not (st.button("Calculate")):
            st.stop()

        if uploaded_file is None:
            st.error(
                "You must choose a file to be able to calculate the statistical significance."
            )

        else:
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

            p_value = np.mean([diff > observed_diff for diff in perm_diffs])

            st.subheader("Result")
            if p_value <= alpha:
                st.success("The difference is statistically significant")
            else:
                st.error("The difference is not statistically significant")
            st.write(f"Control mean: {control_mean:.2f}")
            st.write(f"Treatment mean: {treatment_mean:.2f}")
            st.write(f"Observed difference: {observed_diff/control_mean:+.2%}")
            st.write(f"p-value: {p_value:.2f}")

            code = template.render(test=test, confidence_level=confidence_level)
            with st.expander("Show the code"):
                st.code(code, language="python")
