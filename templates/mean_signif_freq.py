# Import the libraries
import random
import numpy as np
import pandas as pd
{% if inputs.test_statistic == "t-test" %}
from statsmodels.stats.weightstats import ttest_ind
{% elif inputs.test_statistic == "z-test" %}
from statsmodels.stats.weightstats import ztest
{% endif %}

# Load the CSV file
df = pd.read_csv("{{ inputs.file.name }}")

# Define the parameters
confidence = {{ inputs.confidence }}
alpha = 1 - confidence

# Calculate the observed difference
control_mean = df[df["{{ inputs.alias['Group'] }}"] == "{{ inputs.alias['Control'] }}"]["{{ inputs.alias['Measurement'] }}"].mean()
treatment_mean = df[df["{{ inputs.alias['Group'] }}"] == "{{ inputs.alias['Treatment'] }}"]["{{ inputs.alias['Measurement'] }}"].mean()
observed_diff = treatment_mean - control_mean

# Get the control and treatment measurements
control_measurements = df[df["{{ inputs.alias['Group'] }}"] == "{{ inputs.alias['Control'] }}"]["{{ inputs.alias['Measurement'] }}"]
treatment_measurements = df[df["{{ inputs.alias['Group'] }}"] == "{{ inputs.alias['Treatment'] }}"]["{{ inputs.alias['Measurement'] }}"]

# Calculate the p-value
{% if inputs.test_statistic == "t-test" %}
tstat, p_value, dfree = ttest_ind(control_measurements, treatment_measurements)
{% elif inputs.test_statistic == "z-test" %}
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
