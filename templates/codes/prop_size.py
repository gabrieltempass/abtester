# Import the libraries
import math
from statsmodels.stats.proportion import proportion_effectsize
{% if i.method == "t-test" %}
from statsmodels.stats.power import tt_ind_solve_power
{% elif i.method == "Z-test" %}
from statsmodels.stats.power import zt_ind_solve_power
{% endif %}

# Define the parameters
control_proportion = {{ i.control_proportion }}
sensitivity = {{ i.sensitivity }}
alternative = "{{ i.alternative }}"
confidence = {{ i.confidence }}
power = {{ i.power }}
control_ratio = {{ i.control_ratio }}
treatment_ratio = {{ i.treatment_ratio }}

# Calculate the sample size
if alternative == "smaller":
    sensitivity *= -1
treatment_proportion = control_proportion * (1 + sensitivity)
effect_size = proportion_effectsize(
    treatment_proportion,
    control_proportion
)
alpha = 1 - confidence
ratio = treatment_ratio / control_ratio
{% if i.method == "t-test" %}
control_sample = math.ceil(tt_ind_solve_power(
{% elif i.method == "Z-test" %}
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
