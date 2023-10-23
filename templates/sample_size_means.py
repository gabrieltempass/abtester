# Import the libraries
import math
import pandas as pd
from scipy.stats import norm

# Define the parameters
sensitivity = {{ sensitivity }}
alternative = "{{ alternative }}"
confidence_level = {{ confidence_level }}
alpha = 1 - confidence_level
power = {{ power }}
control_ratio = {{ control_ratio }}
treatment_ratio = {{ treatment_ratio }}

# Calculate the sample size
{% if alternative == "one-sided" %}
z_alpha = norm.ppf(1 - alpha)
{% elif alternative == "two-sided" %}
z_alpha = norm.ppf(1 - alpha / 2)
{% endif %}
z_beta = norm.ppf(1 - beta)
a = 1 / control_ratio + 1 / treatment_ratio
b = pow(z_alpha + z_beta, 2)
control_mean = df["measurement"].mean()
treatment_mean = control_mean * (1 + sensitivity)
effect_size = treatment_mean - control_mean
std_dev = df["measurement"].std()
sample = math.ceil(a * b / pow(effect_size / std_dev, 2))
control_sample = math.ceil(sample * control_ratio)
treatment_sample = math.ceil(sample * treatment_ratio)

# Show the result
print(f"Minimum sample for the control group: {control_sample}")
print(f"Minimum sample for the treatment group: {treatment_sample}")
print(f"Total minimum sample for the experiment: {control_sample + treatment_sample}")
