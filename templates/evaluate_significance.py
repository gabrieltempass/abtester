# Import the libraries
import random
import numpy as np
import pandas as pd

# Declare the permutation function
def permutation(x, nA, nB):
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[idx_B].mean() - x.loc[idx_A].mean()

# Define the parameters
{% if test == 'Proportions' %}
control_users = {{ control_users }}
treatment_users = {{ treatment_users }}
control_conversions = {{ control_conversions }}
treatment_conversions = {{ treatment_conversions }}
{% endif %}
confidence_level = {{ confidence_level }}
alpha = 1 - confidence_level
{% if test == 'Means' %}

# Get the measurements and count the users
measurements = dataframe['measurement']
control_users = dataframe[dataframe['group'] == 'control'].shape[0]
treatment_users = dataframe[dataframe['group'] == 'treatment'].shape[0]
{% endif %}

# Calculate the observed difference
{% if test == 'Proportions' %}
control_effect = control_conversions/control_users
treatment_effect = treatment_conversions/treatment_users
observed_diff = treatment_effect - control_effect

# Create the pool to draw the samples
conversion = [0]*(control_users + treatment_users)
conversion.extend([1]*(control_conversions + treatment_conversions))
conversion = pd.Series(conversion)
{% elif test == 'Means' %}
control_mean = dataframe[dataframe['group'] == 'control']['measurement'].mean()
treatment_mean = dataframe[dataframe['group'] == 'treatment']['measurement'].mean()
observed_diff = treatment_mean - control_mean
{% endif %}

# Execute the permutation test
perm_diffs = []
for _ in range(1000):
    perm_diffs.append(permutation(
        {% if test == 'Proportions' %}
        conversion,
        control_users + control_conversions,
        treatment_users + treatment_conversions
        {% elif test == 'Means' %}
        measurements,
        control_users,
        treatment_users
        {% endif %}
    ))

# Calculate the p-value
p_value = np.mean([diff > observed_diff for diff in perm_diffs])

# Show the result
if p_value <= alpha:
    print('The difference is statistically significant')
else:
    print('The difference is not statistically significant')
{% if test == 'Proportions' %}
print(f'Control conversion: {control_effect:.2%}')
print(f'Treatment conversion: {treatment_effect:.2%}')
print(f'Observed difference: {observed_diff*100:+.2f} p.p. ({observed_diff/control_effect:+.2%})')
{% elif test == 'Means' %}
print(f'Control mean: {control_mean:.2f}')
print(f'Treatment mean: {treatment_mean:.2f}')
print(f'Observed difference: {observed_diff/control_mean:+.2%}')
{% endif %}
print(f'p-value: {p_value:.2f}')