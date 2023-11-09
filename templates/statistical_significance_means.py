# Import the libraries
import random
import numpy as np
import pandas as pd

# Load the CSV file
df = pd.read_csv("{{ file_name }}")

# Declare the permutation function
def permutation(x, nA, nB):
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[idx_B].mean() - x.loc[idx_A].mean()

# Define the parameters
confidence = {{ confidence }}
alpha = 1 - confidence

# Get the measurements and count the users
measurements = df["{{ alias['Measurement'] }}"]
control_users = df[df["{{ alias['Group'] }}"] == "{{ alias['Control'] }}"].shape[0]
treatment_users = df[df["{{ alias['Group'] }}"] == "{{ alias['Treatment'] }}"].shape[0]

# Calculate the observed difference
control_mean = df[df["{{ alias['Group'] }}"] == "{{ alias['Control'] }}"]["{{ alias['Measurement'] }}"].mean()
treatment_mean = df[df["{{ alias['Group'] }}"] == "{{ alias['Treatment'] }}"]["{{ alias['Measurement'] }}"].mean()
observed_diff = treatment_mean - control_mean

# Execute the permutation test
random.seed(0)
perm_diffs = []
for _ in range(1000):
    perm_diffs.append(
        permutation(
            measurements,
            control_users,
            treatment_users
        )
    )

# Calculate the p-value
p_value = np.mean([diff > abs(observed_diff) for diff in perm_diffs])

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
prefix = "~" if round(p_value, 4) == 0 else ""
print(f"Control mean: {control_mean:.2f}")
print(f"Treatment mean: {treatment_mean:.2f}")
print(f"Observed difference: {observed_diff / control_mean:+.2%}")
print(f"Alpha: {alpha:.4f}")
print(f"p-value: {prefix}{p_value:.4f}")
print(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")
