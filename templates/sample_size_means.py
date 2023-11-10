# Import the libraries
import math
import pandas as pd
{% if test_statistic == "t-test" %}
from statsmodels.stats.power import tt_ind_solve_power
{% elif test_statistic == "z-test" %}
from statsmodels.stats.power import zt_ind_solve_power
{% endif %}

# Load the CSV file
df = pd.read_csv("{{ file_name }}")

# Define the parameters
sensitivity = {{ sensitivity }}
alternative = "{{ alternative }}"
confidence = {{ confidence }}
power = {{ power }}
control_ratio = {{ control_ratio }}
treatment_ratio = {{ treatment_ratio }}
control_mean = df["{{ alias['Measurement'] }}"].mean()
standard_deviation = df["{{ alias['Measurement'] }}"].std()

# Calculate the sample size
if alternative == "smaller":
    sensitivity *= -1
treatment_mean = control_mean * (1 + sensitivity)
difference = treatment_mean - control_mean
effect_size = difference / standard_deviation
alpha = 1 - confidence
ratio = treatment_ratio / control_ratio
{% if test_statistic == "t-test" %}
control_sample = math.ceil(tt_ind_solve_power(
{% elif test_statistic == "z-test" %}
control_sample = math.ceil(zt_ind_solve_power(
{% endif %}
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=ratio,
    alternative=alternative
))
treatment_sample = math.ceil(control_sample * ratio)

# Show the result
print("Sample size")
print(f"Control: {control_sample:,}")
print(f"Treatment: {treatment_sample:,}")
print(f"Total: {(control_sample + treatment_sample):,}")
