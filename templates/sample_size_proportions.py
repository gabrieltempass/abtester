# Import the libraries
import math
import statsmodels.stats.api as sms

# Define the parameters
control_conversion = {{ control_conversion }}
sensitivity = {{ sensitivity }}
treatment_conversion = control_conversion * (1 + sensitivity)
alternative = "{{ alternative }}"
confidence_level = {{ confidence_level }}
alpha = 1 - confidence_level
power = {{ power }}

# Calculate the sample size
effect_size = sms.proportion_effectsize(
    control_conversion,
    treatment_conversion
)
analysis = sms.TTestIndPower()
{% if alternative == "one-sided" %}
if alternative == "one-sided":
    alternative = "smaller"
{% endif %}
treatment_sample = math.ceil(analysis.solve_power(
    effect_size,
    power=power,
    alpha=alpha,
    ratio=1,
    alternative=alternative
))
control_sample = treatment_sample

# Show the result
print(f"Minimum sample for the control group: {control_sample}")
print(f"Minimum sample for the treatment group: {treatment_sample}")
print(f"Total minimum sample for the experiment: {control_sample + treatment_sample}")
