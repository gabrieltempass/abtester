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

# Calculate the observed difference
control_proportion = control_conversions / control_users
treatment_proportion = treatment_conversions / treatment_users
observed_diff = treatment_proportion - control_proportion

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
    print("The difference is statistically significant")
    comparison = {
        "direction": "less than or equal to",
        "significance": "is"
    }
else:
    print("The difference is not statistically significant")
    comparison = {
        "direction": "greater than",
        "significance": "is not"
    }
prefix = "<" if round(p_value, 4) < 0.0001 else ""
print(f"Control conversion: {control_proportion:.2%}")
print(f"Treatment conversion: {treatment_proportion:.2%}")
print(f"Observed difference: {observed_diff * 100:+.2f} p.p. ({observed_diff / control_proportion:+.2%})")
print(f"Alpha: {alpha:.4f}")
print(f"p-value: {prefix}{p_value:.4f}")
print(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")
