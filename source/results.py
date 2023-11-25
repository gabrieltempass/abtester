from jinja2 import FileSystemLoader, Environment
import streamlit as st


def show_size_result(i, s):
    show_size_report(i=i, s=s)
    show_code(i)


def show_signif_result(i, s):
    show_signif_report(i=i, s=s)
    show_code(i)


def show_size_report(i, s):
    st.write("Sample size")
    st.write(f"Test statistic: {i.test_statistic}")
    st.write(f"Control: {s.control_sample:,}")
    st.write(f"Treatment: {s.treatment_sample:,}")
    st.write(f"Total: {(s.control_sample + s.treatment_sample):,}")


def show_signif_report(i, s):

    if s.p_value <= s.alpha:
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

    prefix = "<" if round(s.p_value, 4) < 0.0001 else ""

    if i.test == "Proportions":
        st.write(f"Control proportion: {s.control_prop:.2%}")
        st.write(f"Treatment proportion: {s.treatment_prop:.2%}")
        st.write(f"Observed difference: {s.observed_diff * 100:+.2f} p.p. ({s.observed_diff / s.control_prop:+.2%})")
    elif i.test == "Means":
        st.write(f"Control standard deviation: {s.control_std:.2f}")
        st.write(f"Treatment standard deviation: {s.treatment_std:.2f}")
        st.write(f"Control mean: {s.control_mean:.2f}")
        st.write(f"Treatment mean: {s.treatment_mean:.2f}")
        st.write(f"Observed difference: {s.observed_diff / s.control_mean:+.2%}")

    st.write(f"Alpha: {s.alpha:.4f}")
    st.write(f"p-value: {prefix}{s.p_value:.4f}")
    st.write(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")


def show_code(i):
    loader = FileSystemLoader("templates")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    if i.menu == "sample size":

        if i.test == "Proportions":
            template = env.get_template("prop_size.py")
        elif i.test == "Means":
            template = env.get_template("mean_size.py")

    elif i.menu == "statistical significance":

        if i.test == "Proportions":
            if i.test_statistic == "Permutation":
                template = env.get_template("prop_signif_comp.py")
            elif i.test_statistic == "z-test":
                template = env.get_template("prop_signif_freq.py")

        elif i.test == "Means":
            if i.test_statistic == "Permutation":
                template = env.get_template("mean_signif_comp.py")
            elif i.test_statistic == "t-test" or i.test_statistic == "z-test":
                template = env.get_template("mean_signif_freq.py")

    code = template.render(i=i)
    with st.expander("Show the code"):
        st.code(code, language="python")

