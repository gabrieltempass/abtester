from jinja2 import FileSystemLoader, Environment
import streamlit as st


def show_sample_report(test_statistic, control_sample, treatment_sample):
    st.divider()
    st.subheader("Result")
    st.write("Sample size")
    st.write(f"Test statistic: {test_statistic}")
    st.write(f"Control: {control_sample:,}")
    st.write(f"Treatment: {treatment_sample:,}")
    st.write(f"Total: {(control_sample + treatment_sample):,}")
    return


def show_significance_report(
    test,
    control,
    treatment,
    observed_diff,
    alpha,
    p_value,
):
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


def show_code(
    menu,
    test,
    confidence,
    test_statistic=None,
    sensitivity=None,
    alternative=None,
    power=None,
    control_ratio=None,
    treatment_ratio=None,
    control_conversion=None,
    control_users=None,
    treatment_users=None,
    control_conversions=None,
    treatment_conversions=None,
    file_name=None,
    alias=None,
):
    loader = FileSystemLoader("templates")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    if menu == "Calculate the sample size":

        if test == "Proportions":
            template = env.get_template("sample_size_proportions.py")
        elif test == "Means":
            template = env.get_template("sample_size_means.py")

    elif menu == "Evaluate the statistical significance":

        if test == "Proportions":
            template = env.get_template("statistical_significance_proportions.py")
        elif test == "Means":
            if test_statistic == "Permutation":
                template = env.get_template("statistical_significance_means_comp.py")
            elif test_statistic == "t-test" or test_statistic == "z-test":
                template = env.get_template("statistical_significance_means_freq.py")

    code = template.render(
        sensitivity=sensitivity,
        alternative=alternative,
        confidence=confidence,
        power=power,
        control_ratio=control_ratio,
        treatment_ratio=treatment_ratio,
        control_conversion=control_conversion,
        control_users=control_users,
        treatment_users=treatment_users,
        control_conversions=control_conversions,
        treatment_conversions=treatment_conversions,
        file_name=file_name,
        alias=alias,
        test_statistic=test_statistic,
    )
    with st.expander("Show the code"):
        st.code(code, language="python")
    return


def show_sample_result(
    menu,
    test,
    sensitivity,
    alternative,
    confidence,
    power,
    control_sample,
    treatment_sample,
    test_statistic,
    control_ratio=None,
    treatment_ratio=None,
    control_conversion=None,
    file_name=None,
    alias=None,
):
    show_sample_report(test_statistic, control_sample, treatment_sample)
    show_code(
        menu=menu,
        test=test,
        sensitivity=sensitivity,
        alternative=alternative,
        confidence=confidence,
        power=power,
        control_conversion=control_conversion,
        control_ratio=control_ratio,
        treatment_ratio=treatment_ratio,
        file_name=file_name,
        alias=alias,
        test_statistic=test_statistic,
    )
    return


def show_significance_result(
    menu,
    test,
    control,
    treatment,
    observed_diff,
    alpha,
    p_value,
    test_statistic=None,
    control_users=None,
    treatment_users=None,
    control_conversions=None,
    treatment_conversions=None,
    confidence=None,
    file_name=None,
    alias=None,
):
    show_significance_report(
        test=test,
        control=control,
        treatment=treatment,
        observed_diff=observed_diff,
        alpha=alpha,
        p_value=p_value,
    )
    show_code(
        menu=menu,
        test=test,
        control_users=control_users,
        treatment_users=treatment_users,
        control_conversions=control_conversions,
        treatment_conversions=treatment_conversions,
        confidence=confidence,
        file_name=file_name,
        alias=alias,
        test_statistic=test_statistic,
    )

