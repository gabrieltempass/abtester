import pandas as pd
import streamlit as st
from source.statistics import percentage
from source.utils import show_download_button


def get_menu_input():
    menu = st.selectbox(
        "What do you want to do?",
        (
            "Select an option",
            "Calculate the sample size",
            "Evaluate the statistical significance",
        ),
    )
    return menu


def get_test_input():
    test = st.radio(
        label="Test",
        options=("Proportions", "Means"),
        index=0,
        horizontal=True,
        help=description["test"],
    )
    return test


def get_confidence_level_input():
    confidence_level = percentage(
        st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            help=description["confidence_level"],
        )
    )
    return confidence_level


def get_ratio_input(col, label, value, description, disabled=False):
    ratio = percentage(
        col.number_input(
            label=label,
            min_value=0.1,
            max_value=99.9,
            value=value,
            step=1.0,
            format="%.1f",
            help=description,
            disabled=disabled,
        )
    )
    return ratio


def get_proportions_sample_input():
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
    return control_conversion


def get_common_sample_inputs():
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
        label="Alternative",
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
    confidence_level = get_confidence_level_input()
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

    control_ratio = get_ratio_input(
        col=col_1,
        label="Control ratio (%)",
        value=50.0,
        description=description["control_ratio"],
    )
    treatment_ratio = get_ratio_input(
        col=col_2,
        label="Treatment ratio (%)",
        value=100.0 - control_ratio * 100,
        description=description["treatment_ratio"],
        disabled=True,
    )
    return (
        sensitivity,
        alternative,
        confidence_level,
        power,
        control_ratio,
        treatment_ratio,
    )


def get_file_sample_input():
    uploaded_file = st.file_uploader(
        label="Choose a CSV file",
        type="csv",
        help=description["uploaded_file"],
    )
    return uploaded_file


# def get_file_sample_inputs():
#     column = st.selectbox(
#         label="Select the column with the measurements",
#         options=(
#             "Column A",
#             "Column B",
#             "Column C",
#         ),
#         index=None,
#         placeholder="Choose an option",
#     )
#     return column


def show_file_examples():
    st.write(
        "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user. Here is an example:"
    )
    path = "sample_datasets/sample_size/"
    df_format = pd.read_csv(f"{path}format.csv")
    st.dataframe(df_format, height=230, use_container_width=True, hide_index=True)

    st.write("Don't have a CSV file available? Download one of the sample datasets below and try it out.")
    show_download_button("dataset A", path, "dataset_a.csv")
    show_download_button("dataset B", path, "dataset_b.csv")
    show_download_button("dataset C", path, "dataset_c.csv")
    return


def get_means_sample_inputs():
    uploaded_file = get_file_sample_input()
    df = None
    file_name = None

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        file_name = uploaded_file.name
        # column = get_file_sample_inputs()
        show_file_summary(df)
    else:
        show_file_examples()

    return df, file_name


def show_file_summary(df):
    st.dataframe(df, height=230, use_container_width=True, hide_index=True)
    row_plural = ""
    column_plural = ""
    if df.shape[0] > 1:
        row_plural = "s"
    if df.shape[1] > 1:
        column_plural = "s"
    st.write(f"{df.shape[0]:,} row{row_plural} and {df.shape[1]:,} column{column_plural}")
    return


def get_sample_inputs():
    test = get_test_input()
    if test == "Proportions":
        control_conversion = get_proportions_sample_input()
        df = None
        file_name = None

    (
        sensitivity,
        alternative,
        confidence_level,
        power,
        control_ratio,
        treatment_ratio,
    ) = get_common_sample_inputs()

    if test == "Means":
        df, file_name = get_means_sample_inputs()
        control_conversion = None

    return (
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
    )


def get_users_input(label, min_value, value, description):
    users = st.number_input(
        label=label,
        min_value=min_value,
        value=value,
        step=1,
        help=description,
    )
    return users


def get_proportions_significance_inputs():
    control_users = get_users_input(
        label="Users in the control",
        min_value=1,
        value=30000,
        description=description["control_users"]
    )
    treatment_users = get_users_input(
        label="Users in the treatment",
        min_value=1,
        value=30000,
        description=description["treatment_users"]
    )
    control_conversions = get_users_input(
        label="Conversions from the control",
        min_value=0,
        value=1215,
        description=description["control_conversions"]
    )
    treatment_conversions = get_users_input(
        label="Conversions from the treatment",
        min_value=0,
        value=1294,
        description=description["treatment_conversions"]
    )
    confidence_level = get_confidence_level_input()
    return (
    	control_users,
    	treatment_users,
    	control_conversions,
    	treatment_conversions,
    	confidence_level
    )


def get_means_significance_inputs():
    confidence_level = get_confidence_level_input()
    uploaded_file = st.file_uploader("Choose a CSV file")

    return confidence_level, uploaded_file


description = {
    "test": "A proportions test is when the data can be expressed in discrete binary values. For example: the conversions of a web page (when the user does not convert it is a zero and when he or she converts it is a one).\n\nA means test is when the data is continuous. For example: the time spent in a web page.",
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
    "uploaded_file": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user.",
}
