from jinja2 import FileSystemLoader, Environment
import streamlit as st


def show_size_result(inputs, size):
    show_size_report(inputs=inputs, size=size)
    show_code(inputs)


def show_signif_result(inputs, signif):
    show_signif_report(inputs=inputs, signif=signif)
    show_code(inputs)


def show_size_report(inputs, size):
    st.write("Sample size")
    st.write(f"Test statistic: {inputs.test_statistic}")
    st.write(f"Control: {size.control_sample:,}")
    st.write(f"Treatment: {size.treatment_sample:,}")
    st.write(f"Total: {(size.control_sample + size.treatment_sample):,}")


def show_signif_report(inputs, signif):

    if signif.p_value <= signif.alpha:
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

    prefix = "~" if round(signif.p_value, 4) == 0 else ""

    if inputs.test == "Proportions":
        st.write(f"Control proportion: {signif.control_prop:.2%}")
        st.write(f"Treatment proportion: {signif.treatment_prop:.2%}")
        st.write(f"Observed difference: {signif.observed_diff * 100:+.2f} p.p. ({signif.observed_diff / signif.control_prop:+.2%})")
    elif inputs.test == "Means":
        st.write(f"Control mean: {signif.control_mean:.2f}")
        st.write(f"Treatment mean: {signif.treatment_mean:.2f}")
        st.write(f"Observed difference: {signif.observed_diff / signif.control_mean:+.2%}")

    st.write(f"Alpha: {signif.alpha:.4f}")
    st.write(f"p-value: {prefix}{signif.p_value:.4f}")
    st.write(f"Since the p-value is {comparison['direction']} alpha (which comes from 1 minus the confidence level), the difference {comparison['significance']} statistically significant.")


def show_code(inputs):
    loader = FileSystemLoader("templates")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    if inputs.menu == "sample size":

        if inputs.test == "Proportions":
            template = env.get_template("prop_size.py")
        elif inputs.test == "Means":
            template = env.get_template("mean_size.py")

    elif inputs.menu == "statistical significance":

        if inputs.test == "Proportions":
            template = env.get_template("prop_signif.py")
        elif inputs.test == "Means":
            if inputs.test_statistic == "Permutation":
                template = env.get_template("mean_signif_comp.py")
            elif inputs.test_statistic == "t-test" or inputs.test_statistic == "z-test":
                template = env.get_template("mean_signif_freq.py")

    code = template.render(inputs=inputs)
    with st.expander("Show the code"):
        st.code(code, language="python")

