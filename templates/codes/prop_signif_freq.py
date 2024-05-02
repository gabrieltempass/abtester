# Import the libraries
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Define the parameters
control_subjects = {{ i.control_users }}
treatment_subjects = {{ i.treatment_users }}
control_conversions = {{ i.control_conversions }}
treatment_conversions = {{ i.treatment_conversions }}
alternative = "{{ i.alternative }}"
confidence = {{ i.confidence }}
alpha = 1 - confidence

# Calculate the p-value
count = np.array([treatment_conversions, control_conversions])
nobs = np.array([treatment_subjects, control_subjects])
tstat, p_value = proportions_ztest(
    count=count,
    nobs=nobs,
    alternative=alternative
)

# Show the result
if p_value <= alpha:
    outcome = "is"
else:
    outcome = "is not"
if round(p_value, 4) < 0.0001:
    value = "< 0.0001"
else:
    value = f"= {p_value:.4f}"
print(f"The difference {outcome} statistically significant, with a p-value {value}.")
