# Import the libraries
import random
import numpy as np
import pandas as pd

# Load the CSV file
df = pd.read_csv("{{ i.file.name }}")

# Define the parameters
alternative = "{{ i.alternative }}"
confidence = {{ i.confidence }}
alpha = 1 - confidence
iterations = {{ i.iterations }}

# Get the measurements and count the subjects
measurements = df["{{ i.alias['Measurement'] }}"]
control_subjects = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Control'] }}"].shape[0]
treatment_subjects = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Treatment'] }}"].shape[0]

# Calculate the observed difference
control_mean = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Control'] }}"]["{{ i.alias['Measurement'] }}"].mean()
treatment_mean = df[df["{{ i.alias['Group'] }}"] == "{{ i.alias['Treatment'] }}"]["{{ i.alias['Measurement'] }}"].mean()
observed_diff = treatment_mean - control_mean

# Declare the permutation function
def permutation(x, nC, nT):
    n = nC + nT
    idx_C = set(random.sample(range(n), nT))
    idx_T = set(range(n)) - idx_C
    return x.loc[list(idx_T)].mean() - x.loc[list(idx_C)].mean()

# Execute the permutation test
random.seed(0)
perm_diffs = []
for _ in range(iterations):
    perm_diffs.append(
        permutation(
            measurements,
            control_subjects,
            treatment_subjects
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
    outcome = "is"
else:
    outcome = "is not"
if round(p_value, 4) < 0.0001:
    value = "< 0.0001"
else:
    value = f"= {p_value:.4f}"
print(f"The difference {outcome} statistically significant, with a p-value {value}.")
