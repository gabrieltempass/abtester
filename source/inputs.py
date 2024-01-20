import pandas as pd
import streamlit as st

from source.statistics import percentage


def get_menu():
    menu = st.selectbox(
        label="What do you want to do?",
        options=("sample size", "statistical significance"),
        format_func=lambda x: {
            "sample size": "Calculate the sample size",
            "statistical significance": "Evaluate the statistical significance",
        }.get(x),
        index=None,
    )
    return menu


def get_test():
    test = st.radio(
        label="Test",
        options=("Proportions", "Means"),
        index=0,
        horizontal=True,
        help=description["test"],
    )
    return test


def get_size_inputs():
    test = get_test()
    if test == "Proportions":
        inputs = get_prop_size_inputs()
    elif test == "Means":
        inputs = get_mean_size_inputs()
    return inputs


def get_prop_size_inputs():
    inputs = PropSizeInputs()
    inputs.get_control_proportion()
    inputs.get_sensitivity()
    inputs.get_alternative()
    inputs.get_confidence()
    inputs.get_power()
    inputs.get_ratios()
    inputs.get_method()
    return inputs


def get_mean_size_inputs():
    inputs = MeanSizeInputs()
    inputs.get_sensitivity()
    inputs.get_alternative()
    inputs.get_confidence()
    inputs.get_power()
    inputs.get_ratios()
    inputs.get_file(
        requirements=text["size_requirements"],
        description=description["size_file"],
        path="example_datasets/sample_size/",
        file_names={
            "dataset A": "dataset_a.csv",
            "dataset B": "dataset_b.csv",
            "dataset C": "dataset_c.csv",
        },
    )
    inputs.get_method()
    return inputs


def get_signif_inputs():
    test = get_test()
    if test == "Proportions":
        inputs = get_prop_signif_inputs()
    elif test == "Means":
        inputs = get_mean_signif_inputs()
    return inputs


def get_prop_signif_inputs():
    inputs = PropSignifInputs()
    inputs.get_users()
    inputs.get_conversions()
    inputs.get_alternative()
    inputs.get_confidence()
    inputs.get_method()
    return inputs


def get_mean_signif_inputs():
    inputs = MeanSignifInputs()
    inputs.get_alternative()
    inputs.get_confidence()
    inputs.get_file(
        requirements=text["significance_requirements"],
        description=description["significance_file"],
        path="example_datasets/statistical_significance/",
        file_names={
            "dataset 1": "dataset_1.csv",
            "dataset 2": "dataset_2.csv",
            "dataset 3": "dataset_3.csv",
        },
    )
    inputs.get_method()
    return inputs


class ExperimentInputs:
    def __init__(self):
        # Review this part
        self.df, self.file_name, self.alias = None, None, None

    def get_alternative(self):
        self.alternative = st.radio(
            label="Alternative",
            options=("smaller", "larger", "two-sided"),
            format_func=lambda x: {
                "smaller": "Smaller than the null",
                "larger": "Larger than the null",
                "two-sided": "Not equal to the null",
            }.get(x),
            captions=("One-sided", "One-sided", "Two-sided"),
            index=2,
            help=description["alternative"],
            horizontal=True,
        )

    def get_confidence(self):
        self.confidence = percentage(
            st.slider(
                label="Confidence level",
                min_value=70,
                max_value=99,
                value=95,
                format="%d%%",
                help=description["confidence"],
            )
        )

    def get_method(self):
        if self.menu == "sample size":
            options = ("t-test", "Z-test")
            index = 0
        if self.menu == "statistical significance":
            if self.test == "Proportions":
                options = ("Z-test", "Permutation")
                index = 0
            elif self.test == "Means":
                options = ("t-test", "Z-test", "Permutation")
                index = 0

        self.method = st.radio(
            label="Method",
            options=options,
            index=index,
            help=description["method"],
            horizontal=True,
        )

        if self.method == "Permutation":
            self.iterations = st.select_slider(
                label="Iterations",
                options=[1000, 2000, 5000, 10000, 20000, 50000, 100000],
                value=10000,
                help=description["iterations"],
            )

    def get_file(self, description, requirements, path, file_names):
        self.file = st.file_uploader(
            label="Choose a CSV file",
            type="csv",
            help=description,
        )

        if self.file is not None:
            self.df = pd.read_csv(self.file)
            self.get_non_standard(*self.check_for_standard())
            self.show_file_summary()

        else:
            self.show_file_examples(
                requirements=requirements,
                path=path,
                file_names=file_names,
            )

    def check_for_standard(
        self,
        measurement=True,
        group=True,
        control=True,
        treatment=True,
    ):
        
        if self.menu == "sample size":
            if "Measurement" not in self.df.columns:
                measurement = False

        elif self.menu == "statistical significance":
            if "Measurement" not in self.df.columns:
                measurement = False
            if "Group" not in self.df.columns:
                group = False
                # After the user inputs the non standard Group column the
                # control and treatment labels are checked.
                control = False
                treatment = False
            else:
                if "Control" not in self.df["Group"].unique():
                    control = False
                if "Treatment" not in self.df["Group"].unique():
                    treatment = False

        return measurement, group, control, treatment

    def get_non_standard(self, measurement, group, control, treatment):
        alias = {
            "Measurement": "Measurement",
            "Group": "Group",
            "Control": "Control",
            "Treatment": "Treatment",
        }
        df = self.df
        columns = list(df.columns)

        user_id = pd.DataFrame()
        if "User ID" in columns:
            user_id = df["User ID"]
        if "Measurement" in columns:
            measurement_df = df["Measurement"]
        if "Group" in columns:
            group_df = df["Group"]

        if self.menu == "sample size":

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

            self.df = df
            self.alias = alias

        elif self.menu == "statistical significance":

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
                    alias = get_labels(
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
                        alias = get_labels(
                            df=df,
                            alias=alias,
                        )

            self.df = df
            self.alias = alias

    @staticmethod
    def get_column(df, alias, label, columns, description, standard):
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

    def show_file_summary(self):
        self.show_dataframe(self.df)

        row_plural = ""
        if self.df.shape[0] > 1:
            row_plural = "s"
        string = f"{self.df.shape[0]:,} row{row_plural} and 1 column"

        if type(self.df) == pd.core.frame.DataFrame:
            column_plural = ""
            if self.df.shape[1] > 1:
                column_plural = "s"
            string = string.removesuffix(" and 1 column")
            string += f" and {self.df.shape[1]:,} column{column_plural}"

        st.write(string)

    @staticmethod
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode("utf-8")

    @staticmethod
    def show_dataframe(
        df,
        height=230,
        use_container_width=True,
        hide_index=True
    ):
        st.dataframe(
            data=df,
            height=height,
            use_container_width=use_container_width,
            hide_index=hide_index
        )

    @staticmethod
    def show_download_button(path, display, file_name, key):
        df = pd.read_csv(path + file_name)
        df = ExperimentInputs.convert_df(df)
        st.download_button(
            label=f"Download {display}",
            data=df,
            file_name=file_name,
            mime="text/csv",
            key=key,
        )

    @staticmethod
    def show_file_examples(requirements, file_names, path):
        st.write(requirements)
        df_format = pd.read_csv(f"{path}format.csv")
        ExperimentInputs.show_dataframe(df_format)
        st.write(text["download_to_try"])

        i = 1
        for display, file_name in file_names.items():
            ExperimentInputs.show_download_button(
                path=path,
                display=display,
                file_name=file_name,
                key=f"button_{i}"
            )
            i += 1


class SampleSizeInputs(ExperimentInputs):
    def __init__(self):
        super().__init__()
        self.menu = "sample size"
        self.method = "t-test"

    def get_sensitivity(self):
        self.sensitivity = percentage(
            st.number_input(
                label="Sensitivity (%)",
                min_value=0.1,
                value=10.0,
                step=0.1,
                format="%.1f",
                help=description["sensitivity"],
            )
        )

    def get_power(self):
        self.power = percentage(
            st.slider(
                label="Power",
                min_value=70,
                max_value=99,
                value=80,
                format="%d%%",
                help=description["power"],
            )
        )

    def get_ratios(self):
        col_1, col_2 = st.columns(2)
        self.control_ratio = percentage(
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
        self.treatment_ratio = percentage(
            col_2.number_input(
                label="Treatment ratio (%)",
                min_value=0.1,
                max_value=99.9,
                value=100.0 - self.control_ratio * 100,
                step=1.0,
                format="%.1f",
                help=description["treatment_ratio"],
                disabled=True,
            )
        )


class PropSizeInputs(SampleSizeInputs):
    def __init__(self):
        super().__init__()
        self.test = "Proportions"

    def get_control_proportion(self):
        self.control_proportion = percentage(
            st.number_input(
                label="Control proportion (%)",
                min_value=0.1,
                max_value=100.0,
                value=15.0,
                step=0.1,
                format="%.1f",
                help=description["control_proportion"],
            )
        )


class MeanSizeInputs(SampleSizeInputs):
    def __init__(self):
        super().__init__()
        self.test = "Means"
        self.control_proportion = None


class StatSignifInputs(ExperimentInputs):
    def __init__(self):
        super().__init__()
        self.menu = "statistical significance"
        self.method = "Permutation"
        self.iterations = 10000

    @staticmethod
    def get_labels(df, alias):

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


class PropSignifInputs(StatSignifInputs):
    def __init__(self):
        super().__init__()
        self.test = "Proportions"

    def get_users(self):
        col_1, col_2 = st.columns(2)
        self.control_users = col_1.number_input(
            label="Users in the control",
            min_value=1,
            value=30000,
            step=1,
            help=description["control_users"]
        )
        self.treatment_users = col_2.number_input(
            label="Users in the treatment",
            min_value=1,
            value=30000,
            step=1,
            help=description["treatment_users"]
        )

    def get_conversions(self):
        col_1, col_2 = st.columns(2)
        self.control_conversions = col_1.number_input(
            label="Conversions from the control",
            min_value=0,
            value=1202,
            step=1,
            help=description["control_conversions"]
        )
        self.treatment_conversions = col_2.number_input(
            label="Conversions from the treatment",
            min_value=0,
            value=1298,
            step=1,
            help=description["treatment_conversions"]
        )


class MeanSignifInputs(StatSignifInputs):
    def __init__(self):
        super().__init__()
        self.test = "Means"


description = {
    "test": "A proportions test is when the data can be expressed in discrete binary values. For example: the conversions of a web page (when the user does not convert it is a zero and when he or she converts it is a one).\n\nA means test is when the data is continuous. For example: the time spent in a web page.",
    "control_proportion": "The conversion rate expected for the control. To help you set this value, you could use similar historical data. However, if that it is not available, make a guess based on your experience.",
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
    "size_file": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user.",
    "significance_file": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user. Another column must contain the labels that marks users who participated in the control or treatment groups.",
    "measurement": "Select the column with the measurements.",
    "group": "Select the column that contains the labels that marks users who participated in the control or treatment groups.",
    "control": "Select the label that marks users who participated in the control group.",
    "treatment": "Select the label that marks users who participated in the treatment group.",
    "method": "Choose which method will be used to perform the calculations.",
    "iterations": "How many resampling combinations of the control and treatment groups the permutation test will perform. The higher the number, the more accurate the p-value will be. However, it will also take more time to be calculated.",
}

text = {
    "size_requirements": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user. Here is an example:",
    "significance_requirements": "The file must have a header as the first row, and one of the columns must have the values of the metric of interest for every respective unique user. Another column must contain the labels that marks users who participated in the control or treatment groups. Here is an example:",
    "download_to_try": "Don't have a CSV file available? Download one of the sample datasets below and try it out.",
}
