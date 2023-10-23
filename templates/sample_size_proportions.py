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
print("Minimum sample size")
print(f"Control: {control_sample:,d}")
print(f"Treatment: {treatment_sample:,d}")
print(f"Total: {(control_sample + treatment_sample):,d}")
