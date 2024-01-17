from jinja2 import FileSystemLoader, Environment
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from source.utils import prettify_number


def show_result(i, s):
    show_report(i=i, s=s)
    if i.menu == "statistical significance":
        if i.test == "Means":
            if i.method == "t-test":
                show_calculation(i=i, s=s)
    show_code(i=i)


def show_report(i, s):
    loader = FileSystemLoader("templates/result")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    env.filters["prettify_number"] = prettify_number

    if i.menu == "sample size":
        template = env.get_template("size.md")
        summary = template.render(i=i, s=s)
        st.info(summary)

        if i.test == "Proportions":
            template_1 = env.get_template("prop_size_1.md")
            template_2 = env.get_template("prop_size_2.md")

        elif i.test == "Means":
            template_1 = env.get_template("mean_size_1.md")
            template_2 = env.get_template("mean_size_2.md")

    elif i.menu == "statistical significance":

        template = env.get_template("signif.md")
        summary = template.render(s=s)
        if s.p_value <= s.alpha:
            st.success(summary)
        else:
            st.error(summary)

        if i.test == "Proportions":
            template_1 = env.get_template("prop_signif_1.md")
            template_2 = env.get_template("prop_signif_2.md")

        elif i.test == "Means":
            template_1 = env.get_template("mean_signif_1.md")
            template_2 = env.get_template("mean_signif_2.md")

    report_1 = template_1.render(i=i, s=s)
    report_2 = template_2.render(i=i, s=s)
    col_1, col_2 = st.columns(2)
    col_1.write(report_1)
    col_2.write(report_2)


def show_calculation(i, s):
    loader = FileSystemLoader("templates/calculation")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    if i.menu == "statistical significance":

        if i.test == "Means":
            if i.method == "t-test":
                template = env.get_template("mean_signif.md")

    calculation = template.render(i=i, s=s)
    with st.expander("Show calculation"):
        st.write(calculation)


def show_code(i):
    loader = FileSystemLoader("templates/code")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    if i.menu == "sample size":

        if i.test == "Proportions":
            template = env.get_template("prop_size.py")
        elif i.test == "Means":
            template = env.get_template("mean_size.py")

    elif i.menu == "statistical significance":

        if i.test == "Proportions":
            if i.method == "Permutation":
                template = env.get_template("prop_signif_comp.py")
            elif i.method == "z-test":
                template = env.get_template("prop_signif_freq.py")

        elif i.test == "Means":
            if i.method == "Permutation":
                template = env.get_template("mean_signif_comp.py")
            elif i.method == "t-test" or i.method == "z-test":
                template = env.get_template("mean_signif_freq.py")

    code = template.render(i=i)
    with st.expander("Show code"):
        st.code(code, language="python")

