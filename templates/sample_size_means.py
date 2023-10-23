# Import the libraries
import math
import pandas as pd
from statsmodels.stats.power import zt_ind_solve_power

# Load the CSV file
df = pd.read_csv("{{ file_name }}")

# Define the parameters
sensitivity = {{ sensitivity }}
alternative = "{{ alternative }}"
confidence_level = {{ confidence_level }}
power = {{ power }}
control_ratio = {{ control_ratio }}
treatment_ratio = {{ treatment_ratio }}
control_mean = df["measurement"].mean()
standard_deviation = df["measurement"].std()

# Calculate the sample size
{% if alternative == "one-sided" %}
if alternative == "one-sided":
	alternative = "smaller"
{% endif %}
alpha = 1 - confidence_level
ratio = treatment_ratio / control_ratio
treatment_mean = control_mean * (1 + sensitivity)
difference = treatment_mean - control_mean
effect_size = difference / standard_deviation
control_sample = math.ceil(zt_ind_solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=ratio,
    alternative=alternative,
))
treatment_sample = control_sample * ratio

# Show the result
print(f"Minimum sample for the control group: {control_sample}")
print(f"Minimum sample for the treatment group: {treatment_sample}")
print(f"Total minimum sample for the experiment: {control_sample + treatment_sample}")
