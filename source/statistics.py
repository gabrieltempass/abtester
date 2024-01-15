import math
import random

import numpy as np
import pandas as pd
import streamlit as st
from statsmodels.stats.proportion import proportion_effectsize, proportions_ztest
from statsmodels.stats.power import tt_ind_solve_power, zt_ind_solve_power
from statsmodels.stats.weightstats import ttest_ind, ztest


def percentage(number):
    return number / 100


def get_alpha(confidence):
    return 1 - confidence


def get_beta(power):
    return 1 - power


def permutation(x, nC, nT):
    n = nC + nT
    idx_T = set(random.sample(range(n), nT))
    idx_C = set(range(n)) - idx_T
    return x.loc[list(idx_T)].mean() - x.loc[list(idx_C)].mean()


def calculate_size(i):
    size = SampleSizeCalc()
    if i.test == "Proportions":
        size.calculate_prop_size(i)
    elif i.test == "Means":
        size.calculate_mean_size(i)
    return size


def evaluate_signif(i):
    signif = StatSignifCalc()

    if i.test == "Proportions":
        if i.method == "Permutation":
            signif.evaluate_prop_signif_comp(i)
        elif i.method == "z-test":
            signif.evaluate_prop_signif_freq(i)

    elif i.test == "Means":
        if i.method == "Permutation":
            signif.evaluate_mean_signif_comp(i)
        elif i.method == "t-test" or i.method == "z-test":
            signif.evaluate_mean_signif_freq(i)
    return signif


class SampleSizeCalc:
    def calculate_prop_size(self, i):
        if i.alternative == "smaller":
            i.sensitivity *= -1
        self.treatment_proportion = i.control_proportion * (1 + i.sensitivity)
        self.effect_size = proportion_effectsize(
            self.treatment_proportion,
            i.control_proportion
        )
        self.alpha = get_alpha(i.confidence)
        self.ratio = i.treatment_ratio / i.control_ratio

        if i.method == "t-test":
            self.t_test(i)
        elif i.method == "z-test":
            self.z_test(i)

        self.treatment_sample = math.ceil(self.control_sample * self.ratio)

    def calculate_mean_size(self, i):
        if i.alternative == "smaller":
            i.sensitivity *= -1
        self.control_mean = i.df[i.alias["Measurement"]].mean()
        self.treatment_mean = self.control_mean * (1 + i.sensitivity)
        self.difference = self.treatment_mean - self.control_mean
        self.standard_deviation = i.df[i.alias["Measurement"]].std()
        self.effect_size = self.difference / self.standard_deviation
        self.alpha = get_alpha(i.confidence)
        self.ratio = i.treatment_ratio / i.control_ratio

        if i.method == "t-test":
            self.t_test(i)
        elif i.method == "z-test":
            self.z_test(i)

        self.treatment_sample = math.ceil(self.control_sample * self.ratio)

    def t_test(self, i):
        self.control_sample = math.ceil(tt_ind_solve_power(
            effect_size=self.effect_size,
            alpha=self.alpha,
            power=i.power,
            ratio=self.ratio,
            alternative=i.alternative,
        ))

    def z_test(self, i):
        self.control_sample = math.ceil(zt_ind_solve_power(
            effect_size=self.effect_size,
            alpha=self.alpha,
            power=i.power,
            ratio=self.ratio,
            alternative=i.alternative,
        ))


class StatSignifCalc:
    def evaluate_prop_signif_comp(self, i):
        self.alpha = get_alpha(i.confidence)
        self.control_prop = i.control_conversions / i.control_users
        self.treatment_prop = i.treatment_conversions / i.treatment_users
        self.observed_diff = self.treatment_prop - self.control_prop

        self.control_no_conversions = i.control_users - i.control_conversions
        self.treatment_no_conversions = i.treatment_users - i.treatment_conversions

        conversion = [0] * (self.control_no_conversions + self.treatment_no_conversions)
        conversion.extend([1] * (i.control_conversions + i.treatment_conversions))
        conversion = pd.Series(conversion)

        random.seed(0)
        perm_diffs = []
        # Show a progress bar that disappears when completed
        bar = st.empty().progress(0)
        for percent_complete in range(i.iterations):
            perm_diffs.append(
                permutation(
                    conversion,
                    i.control_users,
                    i.treatment_users,
                )
            )
            bar.progress((percent_complete + 1) / i.iterations)
        bar.empty()

        self.get_comp_p_value(perm_diffs, i.alternative)

    def evaluate_prop_signif_freq(self, i):
        self.alpha = get_alpha(i.confidence)
        self.control_prop = i.control_conversions / i.control_users
        self.treatment_prop = i.treatment_conversions / i.treatment_users
        self.observed_diff = self.treatment_prop - self.control_prop

        count = np.array([i.treatment_conversions, i.control_conversions])
        nobs = np.array([i.treatment_users, i.control_users])
        self.tstat, self.p_value = proportions_ztest(
            count=count,
            nobs=nobs,
            alternative=i.alternative
        )

    def evaluate_mean_signif_comp(self, i):
        self.alpha = get_alpha(i.confidence)

        measurement = i.alias["Measurement"]
        group = i.alias["Group"]
        control = i.alias["Control"]
        treatment = i.alias["Treatment"]

        measurements = i.df[measurement]
        self.control_users = i.df[i.df[group] == control].shape[0]
        self.treatment_users = i.df[i.df[group] == treatment].shape[0]

        self.control_std = i.df[i.df[group] == control][measurement].std()
        self.treatment_std = i.df[i.df[group] == treatment][measurement].std()
        self.control_mean = i.df[i.df[group] == control][measurement].mean()
        self.treatment_mean = i.df[i.df[group] == treatment][measurement].mean()
        self.observed_diff = self.treatment_mean - self.control_mean

        random.seed(0)
        perm_diffs = []
        # Show a progress bar that disappears when completed
        bar = st.empty().progress(0)
        for percent_complete in range(i.iterations):
            perm_diffs.append(
                permutation(measurements, self.control_users, self.treatment_users)
            )
            bar.progress((percent_complete + 1) / i.iterations)
        bar.empty()

        self.get_comp_p_value(perm_diffs, i.alternative)

    def evaluate_mean_signif_freq(self, i):
        self.alpha = get_alpha(i.confidence)

        measurement = i.alias["Measurement"]
        group = i.alias["Group"]
        control = i.alias["Control"]
        treatment = i.alias["Treatment"]

        self.control_n = i.df[i.df[group] == control].shape[0]
        self.treatment_n = i.df[i.df[group] == treatment].shape[0]
        self.control_std = i.df[i.df[group] == control][measurement].std()
        self.treatment_std = i.df[i.df[group] == treatment][measurement].std()
        self.control_mean = i.df[i.df[group] == control][measurement].mean()
        self.treatment_mean = i.df[i.df[group] == treatment][measurement].mean()
        self.observed_diff = self.treatment_mean - self.control_mean

        control_measurements = i.df[i.df[group] == control][measurement]
        treatment_measurements = i.df[i.df[group] == treatment][measurement]

        if i.method == "t-test":
            self.tstat, self.p_value, self.dof = ttest_ind(
                treatment_measurements,
                control_measurements,
                alternative=i.alternative,
            )
        elif i.method == "z-test":
            self.tstat, self.p_value = ztest(
                treatment_measurements,
                control_measurements,
                alternative=i.alternative,
            )

    def get_comp_p_value(self, diffs, alternative):
        if alternative == "smaller":
            self.p_value = np.mean([diff <= self.observed_diff for diff in diffs])
        elif alternative == "larger":
            self.p_value = np.mean([diff >= self.observed_diff for diff in diffs])
        elif alternative == "two-sided":
            self.p_value = np.mean([abs(diff) >= abs(self.observed_diff) for diff in diffs])

