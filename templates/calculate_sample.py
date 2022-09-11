# Import the libraries
import math
{% if test == "Proportions" %}
import statsmodels.stats.api as sms
{% elif test == "Means" %}
import pandas as pd
from scipy.stats import norm
{% endif %}

# Define the parameters
{% if test == "Proportions" %}
control_conversion = {{ control_conversion }}
{% endif %}
sensitivity = {{ sensitivity }}
{% if test == "Proportions" %}
treatment_conversion = control_conversion * (1 + sensitivity)
{% endif %}
{% if test == "Proportions" %}
alternative = "{{ alternative }}"
{% endif %}
confidence_level = {{ confidence_level }}
alpha = 1 - confidence_level
power = {{ power }}
{% if test == "Means" %}
control_ratio = {{ control_ratio }}
treatment_ratio = 1 - control_ratio
std_dev = df["measurement"].std()
{% endif %}

# Calculate the minimum sample
{% if test == "Proportions" %}
effect_size = sms.proportion_effectsize(
    control_conversion,
    treatment_conversion
)
analysis = sms.TTestIndPower()
treatment_sample = math.ceil(analysis.solve_power(
    effect_size,
    power=power,
    alpha=alpha,
    ratio=1,
    alternative=alternative
))
control_sample = treatment_sample
{% elif test == "Means" %}
z_alpha = norm.ppf(1 - alpha / 2)
z_beta = norm.ppf(1 - beta)
a = 1 / control_ratio + 1 / treatment_ratio
b = pow(z_alpha + z_beta, 2)
total_sample = math.ceil(a * b / pow(sensitivity / std_dev, 2))
control_sample = math.ceil(total_sample * control_ratio)
treatment_sample = math.ceil(total_sample * treatment_ratio)
{% endif %}

# Show the result
print(f"Minimum sample for the control group: {control_sample}")
print(f"Minimum sample for the treatment group: {treatment_sample}")
print(f"Total minimum sample for the experiment: {control_sample + treatment_sample}")
