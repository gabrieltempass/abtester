import streamlit as st
from source.utils import percentage


def get_proportions_sample_inputs():
    control_conversion = percentage(
        st.number_input(
            label="Baseline conversion rate (%)",
            min_value=0.1,
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
            min_value=0.1,
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
            key="sample-proportions-confidence-level",
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

    return (
        control_conversion,
        sensitivity,
        alternative,
        confidence_level,
        power
    )


def get_means_sample_inputs():
    sensitivity = percentage(
        st.number_input(
            label="Sensitivity (%)",
            min_value=0.1,
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
            key="sample-means-confidence-level",
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

    uploaded_file = st.file_uploader("Choose a CSV file")

    return (
    	sensitivity,
    	confidence_level,
    	power,
    	uploaded_file
    )


def get_proportions_significance_inputs():
    control_users = st.number_input(
        label="Users in the control",
        min_value=1,
        value=30000,
        step=1,
        help=description["control_users"],
    )

    treatment_users = st.number_input(
        label="Users in the treatment",
        min_value=1,
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

    confidence_level = percentage(
        st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            key="significance-proportions-confidence-level",
            help=description["confidence_level"],
        )
    )

    return (
    	control_users,
    	treatment_users,
    	control_conversions,
    	treatment_conversions,
    	confidence_level
    )


def get_means_significance_inputs():
    confidence_level = percentage(
        st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            key="significance-means-confidence-level",
            help=description["confidence_level"],
        )
    )

    uploaded_file = st.file_uploader("Choose a CSV file")

    return confidence_level, uploaded_file


description = {
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
