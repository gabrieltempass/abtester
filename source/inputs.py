import streamlit as st
from source.utils import percentage


def get_proportions_sample_inputs():
    control_conversion = percentage(
        st.number_input(
            label="Control conversion rate (%)",
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
        label="Alternative is",
        options=("smaller", "larger", "two-sided"),
        index=2,
        format_func=lambda x: {
            "smaller": "Smaller than the null",
            "larger": "Larger than the null",
            "two-sided": "Not equal to the null",
        }.get(x),
        captions=("One-sided", "One-sided", "Two-sided"),
        help=description["alternative"],
        horizontal=True,
        disabled=False,
    )

    confidence_level = percentage(
        st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            help=description["confidence_level"],
            key="sample-proportions-confidence-level",
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
            step=1.0,
            format="%.1f",
            help=description["control_ratio"],
            key="sample-proportions-control-ratio",
        )
    )

    treatment_ratio = percentage(
        col_2.number_input(
            label="Treatment ratio (%)",
            min_value=0.1,
            max_value=99.9,
            value=100.0 - control_ratio * 100,
            step=1.0,
            format="%.1f",
            help=description["treatment_ratio"],
            key="sample-proportions-treatment-ratio",
            disabled=True,
        )
    )

    return (
        control_conversion,
        sensitivity,
        alternative,
        confidence_level,
        power,
        control_ratio,
        treatment_ratio,
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

    alternative = st.radio(
        label="Alternative is",
        options=("smaller", "larger", "two-sided"),
        index=2,
        format_func=lambda x: {
            "smaller": "Smaller than the null",
            "larger": "Larger than the null",
            "two-sided": "Not equal to the null",
        }.get(x),
        captions=("One-sided", "One-sided", "Two-sided"),
        help=description["alternative"],
        horizontal=True,
    )

    confidence_level = percentage(
        st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            help=description["confidence_level"],
            key="sample-means-confidence-level",
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
            step=1.0,
            format="%.1f",
            help=description["control_ratio"],
            key="sample-means-control-ratio",
        )
    )

    treatment_ratio = percentage(
        col_2.number_input(
            label="Treatment ratio (%)",
            min_value=0.1,
            max_value=99.9,
            value=100.0 - control_ratio * 100,
            step=1.0,
            format="%.1f",
            help=description["treatment_ratio"],
            key="sample-means-treatment-ratio",
            disabled=True,
        )
    )

    uploaded_file = st.file_uploader("Choose a CSV file")

    return (
    	sensitivity,
        alternative,
    	confidence_level,
    	power,
        control_ratio,
        treatment_ratio,
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
            help=description["confidence_level"],
            key="significance-proportions-confidence-level",
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
            help=description["confidence_level"],
            key="significance-means-confidence-level",
        )
    )

    uploaded_file = st.file_uploader("Choose a CSV file")

    return confidence_level, uploaded_file


description = {
    "control_conversion": "The conversion rate expected for the control. To help you set this value, you could use similar historical data. However, if that it is not available, make a guess based on your experience.",
    "sensitivity": "The minimum effect size that you want to be able to measure. A rule of thumb is to use 10% (meaning that you want to be able to detect at least a 10% difference for the treatment over the control).",
    "alternative": "Whether you believe that the alternative hypothesis (H₁) will be smaller or larger than the null hypothesis (H₀). If the hypothesis test is two-sided, H₁ is not equal to H₀ must be selected.",
    "confidence_level": "The probability of detecting a true negative. That is, detecting that there is not a statistically significant difference between the control and the treatment, when this difference indeed does not exists. A rule of thumb is to use 95%.",
    "power": "The probability of detecting a true positive. That is, detecting that there is a statistically significant difference between the control and the treatment, when this difference indeed exists. A rule of thumb is to use 80%.",
    "control_users": "The number of users in the control group.",
    "treatment_users": "The number of users in the treatment group.",
    "control_conversions": "The number of users in the control group that converted. For example, if the control group received an email, the conversions could the number of users that clicked in an ad inside it.",
    "treatment_conversions": "The number of users in the treatment group that converted. For example, if the treatment group received an email, the conversions could the number of users that clicked in an ad inside it.",
    "control_ratio": "The percentage of users from the entire experiment who are part of the control group.",
    "treatment_ratio": "The percentage of users from the entire experiment who are part of the treatment group.",
}
