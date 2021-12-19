# Import the libraries
import math
{% if test == 'Proportions' %}
import statsmodels.stats.api as sms
{% elif test == 'Means' %}
import pandas as pd
from scipy.stats import norm
{% endif %}

# Define the parameters
{% if test == 'Proportions' %}
control_conversion = {{ control_conversion }}
{% endif %}
sensitivity = {{ sensitivity }}
{% if test == 'Proportions' %}
treatment_conversion = control_conversion * (1 + sensitivity)
{% endif %}
alternative = {% if test == 'Proportions' %}'{{ alternative }}'
{% elif test == 'Means' %}'two-sided'
{% endif %}
confidence_level = {{ confidence_level }}
alpha = 1 - confidence_level
power = {{ power }}
{% if test == 'Means' %}
beta = 1 - power

# Count the users and get the standard deviation
control_users = dataframe[dataframe['group'] == 'control'].shape[0]
treatment_users = dataframe[dataframe['group'] == 'treatment'].shape[0]
total_users = (control_users + treatment_users)
std = dataframe[dataframe['group'] == 'control']['measurement'].std()
{% endif %}

# Calculate the minimum sample
{% if test == 'Proportions' %}
effect_size = sms.proportion_effectsize(
    control_conversion,
    treatment_conversion
)
analysis = sms.TTestIndPower()
sample = math.ceil(analysis.solve_power(
    effect_size,
    power=power,
    alpha=alpha,
    ratio=1,
    alternative=alternative
))
{% elif test == 'Means' %}
q0 = control_users/total_users
q1 = treatment_users/total_users
z_alpha = norm.ppf(1 - alpha/2)
z_beta = norm.ppf(1 - beta)
a = 1/q1 + 1/q0
b = pow(z_alpha + z_beta, 2)
sample = math.ceil(a*b/pow(sensitivity/std, 2))
{% endif %}

# Show the result
print(f'Minimum sample for the control group: {sample}')
print(f'Minimum sample for the treatment group: {sample}')
print(f'Total minimum sample for the experiment: {sample * 2}')
