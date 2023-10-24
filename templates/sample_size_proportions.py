# Import the libraries
import math
import statsmodels.stats.api as sms

# Define the parameters
control_conversion = {{ control_conversion }}
sensitivity = {{ sensitivity }}
alternative = "{{ alternative }}"
confidence_level = {{ confidence_level }}
power = {{ power }}
control_ratio = {{ control_ratio }}
treatment_ratio = {{ treatment_ratio }}

# Calculate the sample size
treatment_conversion = control_conversion * (1 + sensitivity)
alpha = 1 - confidence_level
ratio = treatment_ratio / control_ratio
effect_size = sms.proportion_effectsize(
    control_conversion,
    treatment_conversion
)
analysis = sms.TTestIndPower()
{% if alternative == "one-sided" %}
if alternative == "one-sided":
    alternative = "smaller"
{% endif %}
control_sample = math.ceil(analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=ratio,
    alternative=alternative
))
treatment_sample = math.ceil(control_sample * ratio)

# Show the result
print("Minimum sample size")
print(f"Control: {control_sample:,}")
print(f"Treatment: {treatment_sample:,}")
print(f"Total: {(control_sample + treatment_sample):,}")
