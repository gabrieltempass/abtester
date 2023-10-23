import numpy as np
import pandas as pd


def get_random_normal_sample(mean, std_dev, size, label):
    sample = np.random.normal(loc=mean, scale=std_dev, size=size)
    df = pd.DataFrame({"group": label, "measurement": sample})
    return df


def generate_dataset(mean_c, mean_t, std_dev_c, std_dev_t, size_c, size_t, decimals):
    df_control = get_random_normal_sample(
        mean=mean_c, std_dev=std_dev_c, size=size_c, label="control"
    )
    df_treatment = get_random_normal_sample(
        mean=mean_t, std_dev=std_dev_t, size=size_t, label="treatment"
    )
    df = pd.concat([df_control, df_treatment])
    df = df.round(decimals=decimals)
    if decimals == 0:
        df = df.astype({"measurement": int})
    return df


np.random.seed(0)

# Statistical significance datasets

df_format_ss = generate_dataset(
    mean_c=90,
    mean_t=110,
    std_dev_c=40,
    std_dev_t=40,
    size_c=5,
    size_t=5,
    decimals=0
)
df_dataset_1 = generate_dataset(
    mean_c=150,
    mean_t=170,
    std_dev_c=32,
    std_dev_t=32,
    size_c=100,
    size_t=100,
    decimals=0,
)
df_dataset_2 = generate_dataset(
    mean_c=14370,
    mean_t=14340,
    std_dev_c=111,
    std_dev_t=111,
    size_c=8000,
    size_t=4000,
    decimals=0,
)
df_dataset_3 = generate_dataset(
    mean_c=600,
    mean_t=660,
    std_dev_c=240,
    std_dev_t=240,
    size_c=490,
    size_t=510,
    decimals=4,
)

path_ss = "sample_datasets/statistical_significance/"

df_format_ss.to_csv(f"{path_ss}format.csv", index=False)
df_dataset_1.to_csv(f"{path_ss}dataset_1.csv", index=False)
df_dataset_2.to_csv(f"{path_ss}dataset_2.csv", index=False)
df_dataset_3.to_csv(f"{path_ss}dataset_3.csv", index=False)

# Minimum sample datasets

df_format_ms = df_format_ss[df_format_ss["group"] == "control"]["measurement"]
df_dataset_a = df_dataset_1[df_dataset_1["group"] == "control"]["measurement"]
df_dataset_b = df_dataset_2[df_dataset_2["group"] == "control"]["measurement"]
df_dataset_c = df_dataset_3[df_dataset_3["group"] == "control"]["measurement"]

path_ms = "sample_datasets/minimum_sample/"

df_format_ms.to_csv(f"{path_ms}format.csv", index=False)
df_dataset_a.to_csv(f"{path_ms}dataset_a.csv", index=False)
df_dataset_b.to_csv(f"{path_ms}dataset_b.csv", index=False)
df_dataset_c.to_csv(f"{path_ms}dataset_c.csv", index=False)
