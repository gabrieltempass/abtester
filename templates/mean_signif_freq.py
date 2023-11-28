# Import the libraries
import random
import numpy as np
import pandas as pd
{% if i.method == "t-test" %}
from statsmodels.stats.weightstats import ttest_ind
{% elif i.method == "z-test" %}
from statsmodels.stats.weightstats import ztest
{% endif %}

# Load the CSV file
df = pd.read_csv("{{ i.file.name }}")

# Define the parameters
alternative = "{{ i.alternative }}"
confidence = {{ i.confidence }}
alpha = 1 - confidence

# Calculate the observed difference
control_mean = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Control'] }}"]["{{ i.alias['Measurement'] }}"].mean()
treatment_mean = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Treatment'] }}"]["{{ i.alias['Measurement'] }}"].mean()
observed_diff = treatment_mean - control_mean

# Get the control and treatment measurements
control_measurements = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Control'] }}"]["{{ i.alias['Measurement'] }}"]
treatment_measurements = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Treatment'] }}"]["{{ i.alias['Measurement'] }}"]

# Calculate the p-value
{% if i.method == "t-test" %}
tstat, p_value, dfree = ttest_ind(
    treatment_measurements,
    control_measurements,
    alternative=alternative
)
{% elif i.method == "z-test" %}
tstat, p_value = ztest(
    treatment_measurements,
    control_measurements,
    alternative=alternative
)
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
prefix = "<" if round(p_value, 4) < 0.0001 else ""
print(f"Control mean: {control_mean:.2f}")
print(f"Treatment mean: {treatment_mean:.2f}")
print(f"Observed difference: {observed_diff / control_mean:+.2%}")
print(f"Alpha: {alpha:.4f}")
print(f"p-value: {prefix}{p_value:.4f}")
print(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")
