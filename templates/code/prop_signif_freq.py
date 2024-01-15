# Import the libraries
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

# Define the parameters
control_users = {{ i.control_users }}
treatment_users = {{ i.treatment_users }}
control_conversions = {{ i.control_conversions }}
treatment_conversions = {{ i.treatment_conversions }}
alternative = "{{ i.alternative }}"
confidence = {{ i.confidence }}
alpha = 1 - confidence

# Calculate the p-value
count = np.array([treatment_conversions, control_conversions])
nobs = np.array([treatment_users, control_users])
tstat, p_value = proportions_ztest(
    count=count,
    nobs=nobs,
    alternative=alternative
)

# Show the result
if p_value <= alpha:
    result = "is statistically significant"
else:
    result = "is not statistically significant"
prefix = "<" if round(p_value, 4) < 0.0001 else ""
print("The difference {result}, with a p-value of: {prefix}{p_value:.4f}")
