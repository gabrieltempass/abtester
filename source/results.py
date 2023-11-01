from jinja2 import FileSystemLoader, Environment
import streamlit as st


def show_sample_report(control_sample, treatment_sample):
    st.subheader("Result")
    st.write("Minimum sample size")
    st.write(f"Control: {control_sample:,}")
    st.write(f"Treatment: {treatment_sample:,}")
    st.write(f"Total: {(control_sample + treatment_sample):,}")
    return


def show_significance_report(df):
    control_users = df[df["Group"] == "Control"].shape[0]
    treatment_users = df[df["Group"] == "Treatment"].shape[0]
    total_users = control_users + treatment_users

    control_ratio = control_users / total_users
    treatment_ratio = treatment_users / total_users
    st.write(f"Ratio: {control_users:,} control users ({control_ratio:.2%}) and {treatment_users:,} treatment users ({treatment_ratio:.2%})")
    return


def show_sample_code(
    test,
    control_conversion,
    file_name,
    sensitivity,
    alternative,
    confidence_level,
    power,
    control_ratio,
    treatment_ratio,
):
    loader = FileSystemLoader("templates")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    if test == "Proportions":
        template = env.get_template("sample_size_proportions.py")
    elif test == "Means":
        template = env.get_template("sample_size_means.py")

    code = template.render(
        control_conversion=control_conversion,
        file_name=file_name,
        sensitivity=sensitivity,
        alternative=alternative,
        confidence_level=confidence_level,
        power=power,
        control_ratio=control_ratio,
        treatment_ratio=treatment_ratio,
    )
    with st.expander("Show the code"):
        st.code(code, language="python")
    return


def show_sample_result(
    control_sample,
    treatment_sample,
    test,
    control_conversion,
    file_name,
    sensitivity,
    alternative,
    confidence_level,
    power,
    control_ratio,
    treatment_ratio,
):
    show_sample_report(control_sample, treatment_sample)
    show_sample_code(
        test=test,
        control_conversion=control_conversion,
        file_name=file_name,
        sensitivity=sensitivity,
        alternative=alternative,
        confidence_level=confidence_level,
        power=power,
        control_ratio=control_ratio,
        treatment_ratio=treatment_ratio,
    )
    return


def show_significance_result(
    test,
    control,
    treatment,
    observed_diff,
    alpha,
    p_value,
):
    st.subheader("Result")
    if p_value <= alpha:
        st.success("The difference is statistically significant")
        comparison = {
            "direction": "less than or equal to",
            "significance": "is"
        }
    else:
        st.error("The difference is not statistically significant")
        comparison = {
            "direction": "greater than",
            "significance": "is not"
        }

    prefix = "~" if round(p_value, 4) == 0 else ""

    if test == "Proportions":
        st.write(f"Control conversion: {control:.2%}")
        st.write(f"Treatment conversion: {treatment:.2%}")
        st.write(f"Observed difference: {observed_diff * 100:+.2f} p.p. ({observed_diff / control:+.2%})")
    elif test == "Means":
        st.write(f"Control mean: {control:.2f}")
        st.write(f"Treatment mean: {treatment:.2f}")
        st.write(f"Observed difference: {observed_diff / control:+.2%}")

    st.write(f"Alpha: {alpha:.4f}")
    st.write(f"p-value: {prefix}{p_value:.4f}")
    st.write(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")
    return

