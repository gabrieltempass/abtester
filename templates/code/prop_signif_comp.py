# Import the libraries
import random
import numpy as np
import pandas as pd

# Define the parameters
control_users = {{ i.control_users }}
treatment_users = {{ i.treatment_users }}
control_conversions = {{ i.control_conversions }}
treatment_conversions = {{ i.treatment_conversions }}
alternative = "{{ i.alternative }}"
confidence = {{ i.confidence }}
alpha = 1 - confidence
iterations = {{ i.iterations }}

# Calculate the observed difference
control_proportion = control_conversions / control_users
treatment_proportion = treatment_conversions / treatment_users
observed_diff = treatment_proportion - control_proportion

# Create the pool to draw the samples
control_no_conversions = control_users - control_conversions
treatment_no_conversions = treatment_users - treatment_conversions
conversion = [0] * (control_no_conversions + treatment_no_conversions)
conversion.extend([1] * (control_conversions + treatment_conversions))
conversion = pd.Series(conversion)

# Declare the permutation function
def permutation(x, nC, nT):
    n = nC + nT
    idx_T = set(random.sample(range(n), nT))
    idx_C = set(range(n)) - idx_T
    return x.loc[list(idx_T)].mean() - x.loc[list(idx_C)].mean()

# Execute the permutation test
random.seed(0)
perm_diffs = []
for _ in range(iterations):
    perm_diffs.append(
        permutation(
            conversion,
            control_users,
            treatment_users
        )
    )

# Calculate the p-value
if alternative == "smaller":
    p_value = np.mean([diff <= observed_diff for diff in perm_diffs])
elif alternative == "larger":
    p_value = np.mean([diff >= observed_diff for diff in perm_diffs])
elif alternative == "two-sided":
    p_value = np.mean([abs(diff) >= abs(observed_diff) for diff in perm_diffs])

# Show the result
if p_value <= alpha:
    result = "is statistically significant"
else:
    result = "is not statistically significant"
prefix = "<" if round(p_value, 4) < 0.0001 else ""
print("The difference {result}, with a p-value of: {prefix}{p_value:.4f}")
