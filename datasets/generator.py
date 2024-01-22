import numpy as np
import pandas as pd


def get_random_normal(mean, std_dev, size):
    x = np.random.normal(loc=mean, scale=std_dev, size=size)
    return x


def get_non_neg_random_normal(x, mean, std_dev):
    if x < 0:
        x = get_random_normal(mean, std_dev, 1)
    return x if x >= 0 else get_non_neg_random_normal(x, mean, std_dev)


def add_label(df, label):
    df["Group"] = label
    return df


def build_base_df(mean, std_dev, size, decimals, non_neg):
    population = np.arange(1, size * 2 + 1)
    rng = np.random.default_rng(seed)
    user_ids = rng.choice(a=population, size=size, replace=False)
    measurements = get_random_normal(mean=mean, std_dev=std_dev, size=size)

    if non_neg and np.min(measurements) < 0:
        replace_negatives = np.vectorize(get_non_neg_random_normal)
        measurements = replace_negatives(measurements, mean=mean, std_dev=std_dev)

    df = pd.DataFrame({"User ID": user_ids, "Measurement": measurements})
    df = df.round(decimals=decimals)
    if decimals == 0:
        df = df.astype({"Measurement": int})
    return df


def generate_stat_sign_dataset(
    mean_c,
    mean_t,
    std_dev_c,
    std_dev_t,
    size_c,
    size_t,
    decimals,
    file_name,
    non_neg=True,
):
    df_control = add_label(
        df=build_base_df(
            mean=mean_c,
            std_dev=std_dev_c,
            size=size_c,
            decimals=decimals,
            non_neg=non_neg,
        ),
        label="Control",
    )
    df_treatment = add_label(
        df=build_base_df(
            mean=mean_t,
            std_dev=std_dev_t,
            size=size_t,
            decimals=decimals,
            non_neg=non_neg,
        ),
        label="Treatment",
    )
    df = pd.concat([df_control, df_treatment])
    path = "example_datasets/statistical_significance/"
    df.to_csv(f"{path}{file_name}.csv", index=False)
    return


def generate_samp_size_dataset(mean, std_dev, size, decimals, file_name, non_neg=True):
    df = build_base_df(
        mean=mean, std_dev=std_dev, size=size, decimals=decimals, non_neg=non_neg
    )
    path = "example_datasets/sample_size/"
    df.to_csv(f"{path}{file_name}.csv", index=False)
    return


seed = 0
np.random.seed(seed)

# Statistical significance datasets

generate_stat_sign_dataset(
    mean_c=90,
    mean_t=110,
    std_dev_c=40,
    std_dev_t=40,
    size_c=4,
    size_t=6,
    decimals=0,
    file_name="format",
)
generate_stat_sign_dataset(
    mean_c=170,
    mean_t=159,
    std_dev_c=32,
    std_dev_t=32,
    size_c=100,
    size_t=100,
    decimals=0,
    file_name="dataset_1",
)
generate_stat_sign_dataset(
    mean_c=14370,
    mean_t=14333,
    std_dev_c=600,
    std_dev_t=600,
    size_c=4000,
    size_t=7000,
    decimals=0,
    file_name="dataset_2",
)
generate_stat_sign_dataset(
    mean_c=600,
    mean_t=627,
    std_dev_c=240,
    std_dev_t=240,
    size_c=490,
    size_t=510,
    decimals=4,
    file_name="dataset_3",
)

# Sample size datasets

generate_samp_size_dataset(
    mean=150,
    std_dev=100,
    size=10,
    decimals=0,
    file_name="format",
)
generate_samp_size_dataset(
    mean=400,
    std_dev=160,
    size=230,
    decimals=0,
    file_name="dataset_a",
)
generate_samp_size_dataset(
    mean=720,
    std_dev=180,
    size=1400,
    decimals=0,
    file_name="dataset_b",
)
generate_samp_size_dataset(
    mean=3,
    std_dev=2.84,
    size=900,
    decimals=3,
    file_name="dataset_c",
    non_neg=False,
)
