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
effect_size = df["measurement"].mean() * (1 + sensitivity)
std_dev = df["measurement"].std()

# Calculate the minimum sample
{% if alternative == "one-sided" %}
z_alpha = norm.ppf(1 - alpha)
{% elif alternative == "two-sided" %}
z_alpha = norm.ppf(1 - alpha / 2)
{% endif %}
z_beta = norm.ppf(1 - beta)
a = 1 / control_ratio + 1 / treatment_ratio
b = pow(z_alpha + z_beta, 2)
total_sample = math.ceil(a * b / pow(effect_size / std_dev, 2))
control_sample = math.ceil(total_sample * control_ratio)
treatment_sample = math.ceil(total_sample * treatment_ratio)

# Show the result
print(f"Minimum sample for the control group: {control_sample}")
print(f"Minimum sample for the treatment group: {treatment_sample}")
print(f"Total minimum sample for the experiment: {control_sample + treatment_sample}")
