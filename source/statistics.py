import math
import numpy as np
import pandas as pd
import statsmodels.stats.api as sms
from statsmodels.stats.power import zt_ind_solve_power
import streamlit as st

from source.utils import get_alpha
from source.utils import get_beta
from source.utils import permutation


def calculate_proportions_sample(
    control_conversion,
    sensitivity,
    alternative,
    confidence_level,
    power,
    control_ratio,
    treatment_ratio,
):
    treatment_conversion = control_conversion * (1 + sensitivity)
    alpha = get_alpha(confidence_level)
    ratio = treatment_ratio / control_ratio

    # Cohen's h
    effect_size = sms.proportion_effectsize(control_conversion,
                                            treatment_conversion)
    analysis = sms.TTestIndPower()
    if alternative == "one-sided":
        alternative = "smaller"
    control_sample = math.ceil(analysis.solve_power(
        effect_size,
        alternative=alternative,
        alpha=alpha,
        power=power,
        ratio=ratio,
    ))
    treatment_sample = control_sample * ratio

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
    if alternative == "one-sided":
        alternative = "smaller"
    alpha = get_alpha(confidence_level)
    ratio = treatment_ratio / control_ratio

    control_mean = df["measurement"].mean()
    treatment_mean = control_mean * (1 + sensitivity)
    difference = treatment_mean - control_mean
    standard_deviation = df["measurement"].std()
    effect_size = difference / standard_deviation

    control_sample = math.ceil(zt_ind_solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative=alternative,
    ))
    treatment_sample = control_sample * ratio

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

    p_value = np.mean([diff > abs(observed_diff) for diff in perm_diffs])

    return control_mean, treatment_mean, observed_diff, alpha, p_value

