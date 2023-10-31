import base64
import random
import numpy as np
import pandas as pd
import streamlit as st


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" width="300" alt="abtester logo"/>' % b64
    c = st.container()
    c.write(html, unsafe_allow_html=True)


def percentage(number):
    return number / 100


def get_alpha(confidence_level):
    return 1 - confidence_level


def get_beta(power):
    return 1 - power


def show_sample_result(control_sample, treatment_sample):
    st.subheader("Result")
    st.write("Minimum sample size")
    st.write(f"Control: {control_sample:,}")
    st.write(f"Treatment: {treatment_sample:,}")
    st.write(f"Total: {(control_sample + treatment_sample):,}")


def show_file_summary(df, option):
    st.dataframe(df, height=230, use_container_width=True, hide_index=True)
    row_plural = ""
    column_plural = ""
    if df.shape[0] > 1:
        row_plural = "s"
    if df.shape[1] > 1:
        column_plural = "s"
    st.write(f"{df.shape[0]:,} row{row_plural} and {df.shape[1]:,} column{column_plural}")
    st.write("**File summary**")

    if option == "Evaluate the statistical significance":
        control_users = df[df["Group"] == "Control"].shape[0]
        treatment_users = df[df["Group"] == "Treatment"].shape[0]
        total_users = control_users + treatment_users

        control_ratio = control_users / total_users
        treatment_ratio = treatment_users / total_users
        st.write(f"Ratio: {control_users:,} control users ({control_ratio:.2%}) and {treatment_users:,} treatment users ({treatment_ratio:.2%})")


def show_download_button(name, path, file):
    df = pd.read_csv(path+file)
    df = convert_df(df)
    st.download_button(
        label=f"Download {name}",
        data=df,
        file_name=file,
        mime="text/csv",
    )


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def permutation(x, nA, nB):
    random.seed(0)
    n = nA + nB
    idx_A = set(random.sample(range(n), nB))
    idx_B = set(range(n)) - idx_A
    return x.loc[list(idx_B)].mean() - x.loc[list(idx_A)].mean()

