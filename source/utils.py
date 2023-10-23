import random
import numpy as np
import pandas as pd
import streamlit as st


def percentage(number):
    return number / 100


def get_alpha(confidence_level):
    return 1 - confidence_level


def get_beta(power):
    return 1 - power


def show_sample_result(control_sample, treatment_sample):
    st.subheader("Result")
    st.write("Minimum sample size")
    st.write(f"Control: {control_sample:,d}")
    st.write(f"Treatment: {treatment_sample:,d}")
    st.write(f"Total: {(control_sample + treatment_sample):,d}")


def show_file_summary(df, option):
    st.write("**File summary**")
    st.write(f"Size: {df.shape[0]} rows and {df.shape[1]} columns")

    if option == "Evaluate the statistical significance":
        control_users = df[df["group"] == "control"].shape[0]
        treatment_users = df[df["group"] == "treatment"].shape[0]
        total_users = control_users + treatment_users

        control_ratio = control_users / total_users
        treatment_ratio = treatment_users / total_users
        st.write(f"Ratio: {control_users} control users ({control_ratio:.2%}) and {treatment_users} treatment users ({treatment_ratio:.2%})")

    st.write("Preview of the first 5 rows:")
    st.table(df.head(5))
    st.write("And the last 5 rows:")
    st.table(df.tail(5))


def show_download_button(name, path, file):
    df = pd.read_csv(path+file)
    df = convert_df(df)
    st.download_button(
        label=f"Download {name}",
        data=df,
        file_name=file,
        mime="text/csv",
    )


@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def permutation(x, nA, nB):
    random.seed(0)
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[idx_B].mean() - x.loc[idx_A].mean()

