import math
import random
import numpy as np
import pandas as pd
import streamlit as st
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import tt_ind_solve_power, zt_ind_solve_power
from statsmodels.stats.weightstats import ttest_ind, ztest


def percentage(number):
    return number / 100


def get_alpha(confidence):
    return 1 - confidence


def get_beta(power):
    return 1 - power


def permutation(x, nA, nB):
    random.seed(0)
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[list(idx_B)].mean() - x.loc[list(idx_A)].mean()


def calculate_size(inputs):
    size = SampleSizeCalc()
    if inputs.test == "Proportions":
        size.calculate_prop_size(inputs)
    elif inputs.test == "Means":
        size.calculate_mean_size(inputs)
    return size


def evaluate_signif(inputs):
    signif = StatSignifCalc()
    if inputs.test == "Proportions":
        signif.evaluate_prop_signif(inputs)
    elif inputs.test == "Means":
        if inputs.test_statistic == "Permutation":
            signif.evaluate_mean_signif_comp(inputs)
        elif inputs.test_statistic == "t-test" or inputs.test_statistic == "z-test":
            signif.evaluate_mean_signif_freq(inputs)
    return signif


class SampleSizeCalc:
    def calculate_prop_size(self, inputs):
        if inputs.alternative == "smaller":
            inputs.sensitivity *= -1
        self.treatment_proportion = inputs.control_proportion * (1 + inputs.sensitivity)
        self.effect_size = proportion_effectsize(
            self.treatment_proportion,
            inputs.control_proportion
        )
        self.alpha = get_alpha(inputs.confidence)
        self.ratio = inputs.treatment_ratio / inputs.control_ratio

        if inputs.test_statistic == "t-test":
            self.t_test(inputs)
        elif inputs.test_statistic == "z-test":
            self.z_test(inputs)

        self.treatment_sample = math.ceil(self.control_sample * self.ratio)

    def calculate_mean_size(self, inputs):
        if inputs.alternative == "smaller":
            inputs.sensitivity *= -1
        self.control_mean = inputs.df[inputs.alias["Measurement"]].mean()
        self.treatment_mean = self.control_mean * (1 + inputs.sensitivity)
        self.difference = self.treatment_mean - self.control_mean
        self.standard_deviation = inputs.df[inputs.alias["Measurement"]].std()
        self.effect_size = self.difference / self.standard_deviation
        self.alpha = get_alpha(inputs.confidence)
        self.ratio = inputs.treatment_ratio / inputs.control_ratio

        if inputs.test_statistic == "t-test":
            self.t_test(inputs)
        elif inputs.test_statistic == "z-test":
            self.z_test(inputs)

        self.treatment_sample = math.ceil(self.control_sample * self.ratio)

    def t_test(self, inputs):
        self.control_sample = math.ceil(tt_ind_solve_power(
            effect_size=self.effect_size,
            alpha=self.alpha,
            power=inputs.power,
            ratio=self.ratio,
            alternative=inputs.alternative,
        ))

    def z_test(self, inputs):
        self.control_sample = math.ceil(zt_ind_solve_power(
            effect_size=self.effect_size,
            alpha=self.alpha,
            power=inputs.power,
            ratio=self.ratio,
            alternative=inputs.alternative,
        ))


class StatSignifCalc:
    def evaluate_prop_signif(self, inputs):
        self.alpha = get_alpha(inputs.confidence)
        self.control_prop = inputs.control_conversions / inputs.control_users
        self.treatment_prop = inputs.treatment_conversions / inputs.treatment_users
        self.observed_diff = self.treatment_prop - self.control_prop

        conversion = [0] * (inputs.control_users + inputs.treatment_users)
        conversion.extend([1] * (inputs.control_conversions + inputs.treatment_conversions))
        conversion = pd.Series(conversion)

        perm_diffs = []
        i = 1000
        # Show a progress bar that disappears when completed
        bar = st.empty().progress(0)
        for percent_complete in range(i):
            perm_diffs.append(
                permutation(
                    conversion,
                    inputs.control_users + inputs.control_conversions,
                    inputs.treatment_users + inputs.treatment_conversions,
                )
            )
            bar.progress((percent_complete + 1) / i)

        bar.empty()
        self.p_value = np.mean([diff > self.observed_diff for diff in perm_diffs])

    def evaluate_mean_signif_comp(self, inputs):
        self.alpha = get_alpha(inputs.confidence)

        measurement = inputs.alias["Measurement"]
        group = inputs.alias["Group"]
        control = inputs.alias["Control"]
        treatment = inputs.alias["Treatment"]

        measurements = inputs.df[measurement]
        self.control_users = inputs.df[inputs.df[group] == control].shape[0]
        self.treatment_users = inputs.df[inputs.df[group] == treatment].shape[0]

        self.control_mean = inputs.df[inputs.df[group] == control][measurement].mean()
        self.treatment_mean = inputs.df[inputs.df[group] == treatment][measurement].mean()
        self.observed_diff = self.treatment_mean - self.control_mean

        perm_diffs = []
        i = 1000
        # Show a progress bar that disappears when completed
        bar = st.empty().progress(0)
        for percent_complete in range(i):
            perm_diffs.append(
                permutation(measurements, self.control_users, self.treatment_users)
            )
            bar.progress((percent_complete + 1) / i)

        bar.empty()
        self.p_value = np.mean([diff > abs(self.observed_diff) for diff in perm_diffs])

    def evaluate_mean_signif_freq(self, inputs):
        self.alpha = get_alpha(inputs.confidence)

        measurement = inputs.alias["Measurement"]
        group = inputs.alias["Group"]
        control = inputs.alias["Control"]
        treatment = inputs.alias["Treatment"]

        self.control_mean = inputs.df[inputs.df[group] == control][measurement].mean()
        self.treatment_mean = inputs.df[inputs.df[group] == treatment][measurement].mean()
        self.observed_diff = self.treatment_mean - self.control_mean

        control_measurements = inputs.df[inputs.df[group] == control][measurement]
        treatment_measurements = inputs.df[inputs.df[group] == treatment][measurement]

        if inputs.test_statistic == "t-test":
            tstat, self.p_value, dfree = ttest_ind(control_measurements, treatment_measurements)
        elif inputs.test_statistic == "z-test":
            tstat, self.p_value = ztest(control_measurements, treatment_measurements)

