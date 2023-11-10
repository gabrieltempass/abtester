# Import the libraries
import random
import numpy as np
import pandas as pd
{% if test_statistic == "t-test" %}
from statsmodels.stats.weightstats import ttest_ind
{% elif test_statistic == "z-test" %}
from statsmodels.stats.weightstats import ztest
{% endif %}

# Load the CSV file
df = pd.read_csv("{{ file_name }}")

# Define the parameters
confidence = {{ confidence }}
alpha = 1 - confidence

# Calculate the observed difference
control_mean = df[df["{{ alias['Group'] }}"] == "{{ alias['Control'] }}"]["{{ alias['Measurement'] }}"].mean()
treatment_mean = df[df["{{ alias['Group'] }}"] == "{{ alias['Treatment'] }}"]["{{ alias['Measurement'] }}"].mean()
observed_diff = treatment_mean - control_mean

# Get the control and treatment measurements
control_measurements = df[df["{{ alias['Group'] }}"] == "{{ alias['Control'] }}"]["{{ alias['Measurement'] }}"]
treatment_measurements = df[df["{{ alias['Group'] }}"] == "{{ alias['Treatment'] }}"]["{{ alias['Measurement'] }}"]

# Calculate the p-value
{% if test_statistic == "t-test" %}
tstat, p_value, dfree = ttest_ind(control_measurements, treatment_measurements)
{% elif test_statistic == "z-test" %}
tstat, p_value = ztest(control_measurements, treatment_measurements)
{% endif %}

# Show the result
if p_value <= alpha:
    print("The difference is statistically significant")
    comparison = {
        "direction": "less than or equal to",
        "significance": "is"
    }
else:
    print("The difference is not statistically significant")
    comparison = {
        "direction": "greater than",
        "significance": "is not"
    }
prefix = "~" if round(p_value, 4) == 0 else ""
print(f"Control mean: {control_mean:.2f}")
print(f"Treatment mean: {treatment_mean:.2f}")
print(f"Observed difference: {observed_diff / control_mean:+.2%}")
print(f"Alpha: {alpha:.4f}")
print(f"p-value: {prefix}{p_value:.4f}")
print(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")
