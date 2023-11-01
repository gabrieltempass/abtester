import math
import random
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import tt_ind_solve_power
from statsmodels.stats.power import zt_ind_solve_power
import streamlit as st


def percentage(number):
    return number / 100


def get_alpha(confidence_level):
    return 1 - confidence_level


def get_beta(power):
    return 1 - power


def permutation(x, nA, nB):
    random.seed(0)
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[list(idx_B)].mean() - x.loc[list(idx_A)].mean()


def calculate_sample(
    test,
    control_conversion,
    sensitivity,
    alternative,
    confidence_level,
    power,
    control_ratio,
    treatment_ratio,
    df,
):
    if test == "Proportions":
        control_sample, treatment_sample = calculate_proportions_sample(
            control_conversion=control_conversion,
            sensitivity=sensitivity,
            alternative=alternative,
            confidence_level=confidence_level,
            power=power,
            control_ratio=control_ratio,
            treatment_ratio=treatment_ratio,
        )
    elif test == "Means":
        control_sample, treatment_sample = calculate_means_sample(
            sensitivity=sensitivity,
            alternative=alternative,
            confidence_level=confidence_level,
            power=power,
            control_ratio=control_ratio,
            treatment_ratio=treatment_ratio,
            df=df,
        )
    return control_sample, treatment_sample


def calculate_proportions_sample(
    control_conversion,
    sensitivity,
    alternative,
    confidence_level,
    power,
    control_ratio,
    treatment_ratio,
):
    if alternative == "smaller":
        sensitivity *= -1
    treatment_conversion = control_conversion * (1 + sensitivity)
    effect_size = proportion_effectsize(treatment_conversion,
                                        control_conversion)
    alpha = get_alpha(confidence_level)
    ratio = treatment_ratio / control_ratio
    control_sample = math.ceil(tt_ind_solve_power(
        effect_size=effect_size,
        alternative=alternative,
        alpha=alpha,
        power=power,
        ratio=ratio,
    ))
    treatment_sample = math.ceil(control_sample * ratio)

    return control_sample, treatment_sample


def calculate_means_sample(
    sensitivity,
    alternative,
    confidence_level,
    power,
    control_ratio,
    treatment_ratio,
    df,
):
    if alternative == "smaller":
        sensitivity *= -1
    control_mean = df["Measurement"].mean()
    treatment_mean = control_mean * (1 + sensitivity)
    difference = treatment_mean - control_mean
    standard_deviation = df["Measurement"].std()
    effect_size = difference / standard_deviation
    alpha = get_alpha(confidence_level)
    ratio = treatment_ratio / control_ratio
    control_sample = math.ceil(zt_ind_solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative=alternative,
    ))
    treatment_sample = math.ceil(control_sample * ratio)

    return control_sample, treatment_sample


def evaluate_proportions_significance(
    control_users,
    treatment_users,
    control_conversions,
    treatment_conversions,
    confidence_level,
):
    alpha = get_alpha(confidence_level)
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

    return control_effect, treatment_effect, observed_diff, alpha, p_value


def evaluate_means_significance(
    confidence_level,
    df,
):
    alpha = get_alpha(confidence_level)

    measurements = df["Measurement"]
    control_users = df[df["Group"] == "Control"].shape[0]
    treatment_users = df[df["Group"] == "Treatment"].shape[0]

    control_mean = df[df["Group"] == "Control"]["Measurement"].mean()
    treatment_mean = df[df["Group"] == "Treatment"]["Measurement"].mean()
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

    return control_mean, treatment_mean, observed_diff, alpha, p_value

