import pandas as pd
import streamlit as st
from source.statistics import percentage


def get_menu_input():
    menu = st.selectbox(
        label="What do you want to do?",
        options=(
            "Calculate the sample size",
            "Evaluate the statistical significance",
        ),
        index=None,
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


def get_users_input(label, min_value, value, description):
    users = st.number_input(
        label=label,
        min_value=min_value,
        value=value,
        step=1,
        help=description,
    )
    return users


def get_control_conversion_input():
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


def get_sensitivity_input():
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
    return sensitivity


def get_alternative_input():
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
    return alternative


def get_confidence_input():
    confidence = percentage(
        st.slider(
            label="Confidence level",
            min_value=70,
            max_value=99,
            value=95,
            format="%d%%",
            help=description["confidence"],
        )
    )
    return confidence

def get_power_input():
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
    return power


def get_ratios_input():
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
            disabled=True,
        )
    )
    return control_ratio, treatment_ratio


def get_csv_input(description):
    file = st.file_uploader(
        label="Choose a CSV file",
        type="csv",
        help=description,
    )
    return file


def get_column_input(label, columns, description, df, alias, standard):
    if "User ID" in columns:
        columns.remove("User ID")
    column = st.selectbox(
        label=label,
        options=columns,
        index=None,
        help=description,
    )
    if column is None:
        alias.update({standard: standard})
        return df, alias
    else:
        df = df[column]
        alias.update({standard: column})
        return df, alias


def get_labels_input(df, alias):

    labels = list(df[alias["Group"]].unique())
    if len(labels) != 2:
        return st.error(f'The column "{alias["Group"]}" must have two labels, one marking the users in the control group and one the users in the treatment group. Download an example dataset to check the format required.')
    else:

        col_1, col_2 = st.columns(2)
        control = col_1.selectbox(
            label="Control label",
            options=labels,
            help=description["control"],
            index=None,
        )

        if control is None:
            index = None
        else:
            treatment_label = labels.copy()
            treatment_label.remove(control)
            index = labels.index(treatment_label[0])

        treatment = col_2.selectbox(
            label="Treatment label",
            options=labels,
            help=description["treatment"],
            index=index,
            disabled=True,
        )

        if control is not None:
            alias.update({
                "Control": control,
                "Treatment": treatment,
            })
        return alias


def show_download_button(path, display, file, key):
    df = pd.read_csv(path + file)
    df = convert_df(df)
    st.download_button(
        label=f"Download {display}",
        data=df,
        file_name=file,
        mime="text/csv",
        key=key,
    )
    return


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def show_dataframe(df, height=230, use_container_width=True, hide_index=True):
    st.dataframe(
        data=df,
        height=height,
        use_container_width=use_container_width,
        hide_index=hide_index
    )
    return


def show_file_examples(requirements, file_names, path):
    st.write(requirements)
    df_format = pd.read_csv(f"{path}format.csv")
    show_dataframe(df_format)
    st.write(text["download_to_try"])

    i = 1
    for display, file in file_names.items():
        show_download_button(path=path, display=display, file=file, key=f"button_{i}")
        i += 1
    return


def show_file_summary(df):
    show_dataframe(df)

    row_plural = ""
    if df.shape[0] > 1:
        row_plural = "s"
    string = f"{df.shape[0]:,} row{row_plural} and 1 column"

    if type(df) == pd.core.frame.DataFrame:
        column_plural = ""
        if df.shape[1] > 1:
            column_plural = "s"
        string = string.removesuffix(" and 1 column")
        string += f" and {df.shape[1]:,} column{column_plural}"

    st.write(string)
    return


def get_test_statistic_input(menu, test):
    show = st.checkbox("Show advanced settings")
    if show:

        if menu == "Calculate the sample size":
            options = ("t-test", "z-test")
            index = 0
        if menu == "Evaluate the statistical significance":
            if test == "Means":
                options = ("t-test", "z-test", "Permutation")
                index = 0

        test_statistic = st.radio(
            label="Test statistic",
            options=options,
            index=index,
            help=description["test_statistic"],
            horizontal=True,
        )
        return test_statistic


def get_non_standard_inputs(
    menu,
    df,
    measurement,
    group,
    control,
    treatment,
):
    alias = {
        "Measurement": "Measurement",
        "Group": "Group",
        "Control": "Control",
        "Treatment": "Treatment",
    }
    columns = list(df.columns)

    user_id = pd.DataFrame()
    if "User ID" in columns:
        user_id = df["User ID"]
    if "Measurement" in columns:
        measurement_df = df["Measurement"]
    if "Group" in columns:
        group_df = df["Group"]

    if menu == "Calculate the sample size":

        if measurement:
            df = df["Measurement"]

        elif not measurement:
            df, alias = get_column_input(
                label="Measurement column",
                columns=columns,
                description=description["measurement"],
                df=df,
                alias=alias,
                standard="Measurement",
            )

        if (
            measurement
            or (not measurement and alias["Measurement"] != "Measurement")
        ):
            df = pd.concat([user_id, df], axis=1)

        return df, alias

    elif menu == "Evaluate the statistical significance":

        if measurement and group:
            df = df[["Measurement", "Group"]]

        elif measurement and not group:
            columns.remove("Measurement")
            df, alias = get_column_input(
                label="Group column",
                columns=columns,
                description=description["group"],
                df=df,
                alias=alias,
                standard="Group",
            )
            if (alias["Group"] != "Group"):
                df = pd.concat([measurement_df, df], axis=1)

        elif not measurement and group:
            columns.remove("Group"),
            df, alias = get_column_input(
                label="Measurement column",
                columns=columns,
                description=description["measurement"],
                df=df,
                alias=alias,
                standard="Measurement",
            )
            if (alias["Measurement"] != "Measurement"):
                df = pd.concat([df, group_df], axis=1)

        elif not measurement and not group:

            measurement_df, alias = get_column_input(
                label="Measurement column",
                columns=columns,
                description=description["measurement"],
                df=df,
                alias=alias,
                standard="Measurement",
            )
            group_df, alias = get_column_input(
                label="Group column",
                columns=columns,
                description=description["group"],
                df=df,
                alias=alias,
                standard="Group",
            )

            if (
                alias["Measurement"] != "Measurement"
                and alias["Group"] != "Group"
            ):
                df = pd.concat([measurement_df, group_df], axis=1)

        if (
            (measurement and group)
            or (not measurement and group and alias["Measurement"] != "Measurement")
            or (measurement and not group and alias["Group"] != "Group")
            or (not measurement and not group and alias["Measurement"] != "Measurement" and alias["Group"] != "Group")
        ):
            df = pd.concat([user_id, df], axis=1)

        # Has "Group"
        if group:
            # Has "Group" and doesn't have "Control" or "Treatment"
            if not control or not treatment:
                alias = get_labels_input(
                    df=df,
                    alias=alias,
                )

        # Doesn't have "Group"
        elif not group:
            if alias["Group"] != "Group":

                # Doesn't have "Group" and check for "Control"
                if "Control" in df[alias["Group"]].unique():
                    control = True

                # Doesn't have "Group" and check for "Treatment"
                if "Treatment" in df[alias["Group"]].unique():
                    treatment = True

                # Doesn't have "Group" and doesn't have "Control" or "Treatment"
                if not control or not treatment:
                    alias = get_labels_input(
                        df=df,
                        alias=alias,
                    )

        return df, alias


def check_for_standard(
    menu,
    df,
    measurement=True,
    group=True,
    control=True,
    treatment=True,
):
    
    if menu == "Calculate the sample size":
        if "Measurement" not in df.columns:
            measurement = False

    elif menu == "Evaluate the statistical significance":
        if "Measurement" not in df.columns:
            measurement = False
        if "Group" not in df.columns:
            group = False
            control = False
            treatment = False
        else:
            if "Control" not in df["Group"].unique():
                control = False
            if "Treatment" not in df["Group"].unique():
                treatment = False

    return (
        menu,
        df,
        measurement,
        group,
        control,
        treatment,
    )


def get_file_input(menu, requirements, description, path, file_names):
    df, file_name, alias = None, None, None  # Revisar isso daqui
    csv = get_csv_input(description)

    if csv is not None:
        file_name = csv.name
        df = pd.read_csv(csv)
        df, alias = get_non_standard_inputs(
            *check_for_standard(
                menu=menu,
                df=df,
            )
        )
        show_file_summary(df)

    else:
        show_file_examples(
            requirements=requirements,
            path=path,
            file_names=file_names,
        )

    return df, file_name, alias


def get_sample_proportions_inputs(menu, test):
    control_conversion = get_control_conversion_input()
    sensitivity = get_sensitivity_input()
    alternative = get_alternative_input()
    confidence = get_confidence_input()
    power = get_power_input()
    control_ratio, treatment_ratio = get_ratios_input()
    df, file_name, alias = None, None, None
    test_statistic = get_test_statistic_input(menu, test)

    return (
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
    )


def get_sample_means_inputs(menu, test):
    control_conversion = None
    sensitivity = get_sensitivity_input()
    alternative = get_alternative_input()
    confidence = get_confidence_input()
    power = get_power_input()
    control_ratio, treatment_ratio = get_ratios_input()
    df, file_name, alias = get_file_input(
        menu=menu,
        requirements=text["sample_requirements"],
        description=description["sample_file"],
        path="example_datasets/sample_size/",
        file_names={
            "dataset A": "dataset_a.csv",
            "dataset B": "dataset_b.csv",
            "dataset C": "dataset_c.csv",
        },
    )
    test_statistic = get_test_statistic_input(menu, test)

    return (
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
    )

def get_sample_inputs(menu):
    test = get_test_input()
    if test == "Proportions":
        (
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
        ) = get_sample_proportions_inputs(menu, test)
    elif test == "Means":
        (
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
        ) = get_sample_means_inputs(menu, test)
    return (
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
    )


def get_significance_proportions_inputs():
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
    confidence = get_confidence_input()
    return (
    	control_users,
    	treatment_users,
    	control_conversions,
    	treatment_conversions,
    	confidence,
    )


def get_significance_means_inputs(menu, test):
    confidence = get_confidence_input()
    df, file_name, alias = get_file_input(
        menu=menu,
        requirements=text["significance_requirements"],
        description=description["significance_file"],
        path="example_datasets/statistical_significance/",
        file_names={
            "dataset 1": "dataset_1.csv",
            "dataset 2": "dataset_2.csv",
            "dataset 3": "dataset_3.csv",
        },
    )
    test_statistic = get_test_statistic_input(menu, test)
    return confidence, df, file_name, alias, test_statistic


description = {
    "test": "A proportions test is when the data can be expressed in discrete binary values. For example: the conversions of a web page (when the user does not convert it is a zero and when he or she converts it is a one).\n\nA means test is when the data is continuous. For example: the time spent in a web page.",
    "control_conversion": "The conversion rate expected for the control. To help you set this value, you could use similar historical data. However, if that it is not available, make a guess based on your experience.",
    "sensitivity": "The minimum effect size that you want to be able to measure. A rule of thumb is to use 10% (meaning that you want to be able to detect at least a 10% difference for the treatment over the control).",
    "alternative": "Whether you believe that the alternative hypothesis (H₁) will be smaller or larger than the null hypothesis (H₀). If the hypothesis test is two-sided, H₁ is not equal to H₀ must be selected.",
    "confidence": "The probability of detecting a true negative. That is, detecting that there is not a statistically significant difference between the control and the treatment, when this difference indeed does not exists. A rule of thumb is to use 95%.",
    "power": "The probability of detecting a true positive. That is, detecting that there is a statistically significant difference between the control and the treatment, when this difference indeed exists. A rule of thumb is to use 80%.",
    "control_users": "The number of users in the control group.",
    "treatment_users": "The number of users in the treatment group.",
    "control_conversions": "The number of users in the control group that converted. For example, if the control group received an email, the conversions could the number of users that clicked in an ad inside it.",
    "treatment_conversions": "The number of users in the treatment group that converted. For example, if the treatment group received an email, the conversions could the number of users that clicked in an ad inside it.",
    "control_ratio": "The percentage of users from the entire experiment who are part of the control group.",
    "treatment_ratio": "The percentage of users from the entire experiment who are part of the treatment group.",
    "sample_file": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user.",
    "significance_file": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user. Another column must contain the labels that marks users who participated in the control or treatment groups.",
    "measurement": "Select the column with the measurements.",
    "group": "Select the column that contains the labels that marks users who participated in the control or treatment groups.",
    "control": "Select the label that marks users who participated in the control group.",
    "treatment": "Select the label that marks users who participated in the treatment group.",
    "test_statistic": "Choose which test statistic will be used to perform the calculations.",
}

text = {
    "sample_requirements": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user. Here is an example:",
    "significance_requirements": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user. Another column must contain the labels that marks users who participated in the control or treatment groups. Here is an example:",
    "download_to_try": "Don't have a CSV file available? Download one of the sample datasets below and try it out.",
}
