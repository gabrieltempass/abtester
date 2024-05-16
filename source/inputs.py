import pandas as pd
import streamlit as st


class ExperimentInputs:
    def __init__(self):
        # Review this part
        self.df, self.file_name, self.alias = None, None, None

    def get_alternative(self):
        self.alternative = st.radio(
            label="Alternative",
            options=("smaller", "larger", "two-sided"),
            format_func=lambda option: {
                "smaller": "Smaller than the null",
                "larger": "Larger than the null",
                "two-sided": "Not equal to the null",
            }.get(option),
            captions=("One-sided", "One-sided", "Two-sided"),
            index=2,
            help=texts["alternative"],
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
                help=texts["confidence"],
            )
        )

    def get_method(self):
        if self.page == "Size":
            options = ("t-test", "Z-test")
            index = 0
        if self.page == "Significance":
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
            help=texts["method"],
            horizontal=True,
        )

        if self.method == "Permutation":
            self.iterations = st.select_slider(
                label="Iterations",
                options=[1000, 2000, 5000, 10000, 20000, 50000, 100000],
                value=10000,
                help=texts["iterations"],
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
        
        if self.page == "Size":
            if "Measurement" not in self.df.columns:
                measurement = False

        elif self.page == "Significance":
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

        if self.page == "Size":

            if measurement:
                df = df["Measurement"]

            elif not measurement:
                df, alias = self.get_column(
                    label="Measurement column",
                    columns=columns,
                    text=texts["measurement"],
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

        elif self.page == "Significance":

            if measurement and group:
                df = df[["Measurement", "Group"]]

            elif measurement and not group:
                columns.remove("Measurement")
                df, alias = self.get_column(
                    label="Group column",
                    columns=columns,
                    text=texts["group"],
                    df=df,
                    alias=alias,
                    standard="Group",
                )
                if (alias["Group"] != "Group"):
                    df = pd.concat([measurement_df, df], axis=1)

            elif not measurement and group:
                columns.remove("Group"),
                df, alias = self.get_column(
                    label="Measurement column",
                    columns=columns,
                    text=texts["measurement"],
                    df=df,
                    alias=alias,
                    standard="Measurement",
                )
                if (alias["Measurement"] != "Measurement"):
                    df = pd.concat([df, group_df], axis=1)

            elif not measurement and not group:

                measurement_df, alias = self.get_column(
                    label="Measurement column",
                    columns=columns,
                    text=texts["measurement"],
                    df=df,
                    alias=alias,
                    standard="Measurement",
                )
                group_df, alias = self.get_column(
                    label="Group column",
                    columns=columns,
                    text=texts["group"],
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
                    alias = self.get_labels(
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
                        alias = self.get_labels(
                            df=df,
                            alias=alias,
                        )

            self.df = df
            self.alias = alias

    @staticmethod
    def get_column(df, alias, label, columns, text, standard):
        if "User ID" in columns:
            columns.remove("User ID")
        column = st.selectbox(
            label=label,
            options=columns,
            index=None,
            help=text,
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
        st.write(texts["download_to_try"])

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
        self.page = "Size"
        self.method = "t-test"

    def get_sensitivity(self):
        self.sensitivity = percentage(
            st.number_input(
                label="Sensitivity (%)",
                min_value=0.1,
                value=10.0,
                step=0.1,
                format="%.1f",
                help=texts["sensitivity"],
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
                help=texts["power"],
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
                help=texts["control_ratio"],
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
                help=texts["treatment_ratio"],
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
                help=texts["control_proportion"],
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
        self.page = "Significance"
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
                help=texts["control"],
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
                help=texts["treatment"],
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
            label="Control subjects",
            min_value=1,
            value=30000,
            step=1,
            help=texts["control_users"]
        )
        self.treatment_users = col_2.number_input(
            label="Treatment subjects",
            min_value=1,
            value=30000,
            step=1,
            help=texts["treatment_users"]
        )

    def get_conversions(self):
        col_1, col_2 = st.columns(2)
        self.control_conversions = col_1.number_input(
            label="Control conversions",
            min_value=0,
            value=1202,
            step=1,
            help=texts["control_conversions"]
        )
        self.treatment_conversions = col_2.number_input(
            label="Treatment conversions",
            min_value=0,
            value=1298,
            step=1,
            help=texts["treatment_conversions"]
        )


class MeanSignifInputs(StatSignifInputs):
    def __init__(self):
        super().__init__()
        self.test = "Means"


def percentage(number):
    return number / 100


def get_test():
    return st.radio(
        label="Test",
        options=("Proportions", "Means"),
        index=0,
        horizontal=True,
        help=texts["test"],
    )


def get_size_inputs():
    test = get_test()
    if test == "Proportions":
        return get_prop_size_inputs()
    if test == "Means":
        return get_mean_size_inputs()


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
        requirements=texts["size_requirements"],
        description=texts["size_file"],
        path="datasets/sample_size/",
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
        return get_prop_signif_inputs()
    if test == "Means":
        return get_mean_signif_inputs()


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
        requirements=texts["significance_requirements"],
        description=texts["significance_file"],
        path="datasets/statistical_significance/",
        file_names={
            "dataset 1": "dataset_1.csv",
            "dataset 2": "dataset_2.csv",
            "dataset 3": "dataset_3.csv",
        },
    )
    inputs.get_method()
    return inputs


texts = {
    "test": (
        """
        If the test compares two proportions or two means, both having
        independent samples.
        
        A proportions test is when the subject data can be expressed in binary
        values. Such as the conversions of a web page. When the user converts
        it is one, otherwise it is zero. Averaging the users measurements
        produces a proportion, e.g. a 27% clickthrough rate.
        
        A means test is when the subject data is continuous. Such as the time
        spent in a web page. Averaging the users measurements produces a mean,
        e.g. a session duration of 49 seconds.
        """
    ),
    "control_proportion": (
        """
        The expected conversion rate for the future control group in the test.
        To set this value, you could use similar historical data. However, if
        that is not available, make a guess based on your experience.
        """
    ),
    "sensitivity": (
        """
        The minimum effect size that you want to be able to detect. For
        example, a sensitivity of 10% means you want to be capable of detecting
        at least a 10% difference between the control and the treatment.
        """
    ),
    "alternative": (
        """
        Whether the alternative hypothesis is smaller, larger or not equal to
        the null hypothesis. In other words, if you want to test whether the
        treatment measurements decreases, increases or is just different in
        relation to the control.
        """
    ),
    "confidence": (
        """
        The probability of detecting that there is not a statistically
        significant difference, between the control and the treatment, when the
        difference is indeed not real. Also known as the probability of
        detecting a true negative.
        
        Selecting a 95% confidence level is the same as selecting a 5%
        significance level (the probability of detecting a false positive),
        which some are more familiar with.
        """
    ),
    "power": (
        """
        The probability of detecting that there is a statistically significant
        difference, between the control and the treatment, when the difference
        is indeed real. Also known as the probability of detecting a true
        positive.
        """
    ),
    "control_users": (
        """
        The number of subjects in the control group.
        """
    ),
    "treatment_users": (
        """
        The number of subjects in the treatment group.
        """
    ),
    "control_conversions": (
        """
        The number of subjects in the control group that converted.
        """
    ),
    "treatment_conversions": (
        """
        The number of subjects in the treatment group that converted.
        """
    ),
    "control_ratio": (
        """
        The percentage of subjects from the entire experiment who are part of
        the control group.
        """
    ),
    "treatment_ratio": (
        """
        The percentage of subjects from the entire experiment who are part of
        the treatment group.
        
        This value is automatically calculated from the control ratio.
        """
    ),
    "size_file": (
        """
        The file with measurements that are expected to be similar to those of
        the future control group.
        """
    ),
    "significance_file": (
        """
        The file with the measurements collected in the experiment.
        """
    ),
    "size_requirements": (
        """
        The file must have a header as the first row, and a column with the
        measurement for every subject. Here is an example:
        """
    ),
    "significance_requirements": (
        """
        The file must have a header as the first row, a column with the
        measurement for every subject, and another column that classifies
        subjects as being part of the control or the treatment group. Here is
        an example:
        """
    ),
    "download_to_try": (
        """
        Don't have a CSV file available? Download one of the sample datasets
        below and try it out.
        """
    ),
    "measurement": (
        """
        The column with the measurement for every subject.
        """
    ),
    "group": (
        """
        The column that classifies subjects as being part of the control or the
        treatment group.
        """
    ),
    "control": (
        """
        The label that classifies the subjects who participated in the control
        group.
        """
    ),
    "treatment": (
        """
        The label that classifies the subjects who participated in the
        treatment group.
        """
    ),
    "method": (
        """
        The frequentist or computational statistical technique that performs
        the calculations.
        """
    ),
    "iterations": (
        """
        How many resampling combinations of the control and treatment groups
        the permutation performs. The higher the number, the more accurate the
        p-value tends to be. However, it also takes more time to be calculated.
        """
    ),
}
