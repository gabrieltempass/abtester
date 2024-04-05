import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from source.utils import load_env


def show_result(i, s):
    screen = show_report(i=i, s=s)
    if i.page == "Significance":
        if i.method in {"t-test", "Z-test"}:
            show_calculation(i=i, s=s)
    show_code(i=i, screen=screen)


def show_report(i, s):
    env = load_env("reports")

    if i.page == "Size":
        template = env.get_template("summary_size.md")
        summary = template.render(i=i, s=s)
        st.info(summary)

        # large height calculation:
        # h = number_of_lines_with_text_on_left_column * 25px
        # + number_of_row_gaps_on_left_column * 16px

        # small height calculation:
        # h = number_of_lines_with_text_on_both_columns * 25px
        # + number_of_row_gaps_on_both_column * 16px

        if i.test == "Proportions":
            template_1 = env.get_template("prop_size.html")
            screen = {"large": 100, "small": 216}

        elif i.test == "Means":
            template_1 = env.get_template("mean_size.html")
            screen = {"large": 100, "small": 191}

    elif i.page == "Significance":
        template = env.get_template("summary_signif.md")
        summary = template.render(i=i, s=s)
        if s.p_value <= s.alpha:
            st.success(summary)
        else:
            st.error(summary)

        if i.test == "Proportions":
            template_1 = env.get_template("prop_signif.html")
            if i.method == "Z-test":
                screen = {"large": 182, "small": 380}
            elif i.method == "Permutation":
                screen = {"large": 182, "small": 314}

        elif i.test == "Means":
            template_1 = env.get_template("mean_signif.html")
            if i.method == "t-test":
                screen = {"large": 298, "small": 546}
            elif i.method == "Z-test":
                screen = {"large": 232, "small": 480}
            elif i.method == "Permutation":
                screen = {"large": 232, "small": 414}
    
    report = template_1.render(i=i, s=s)
    components.html(report, height=screen["large"])
    return screen


def show_calculation(i, s):
    env = load_env("calculations")

    if i.page == "Significance":

        if i.test == "Proportions":
            if i.method == "Z-test":
                template = env.get_template("prop_signif_z.md")

        elif i.test == "Means":
            if i.method == "t-test":
                template = env.get_template("mean_signif_t.md")
            elif i.method == "Z-test":
                template = env.get_template("mean_signif_z.md")

        calculation = template.render(i=i, s=s)
        with st.expander("Show calculation"):
            st.write(calculation)


def show_code(i, screen):
    env = load_env("codes")

    if i.page == "Size":

        if i.test == "Proportions":
            template = env.get_template("prop_size.py")
        elif i.test == "Means":
            template = env.get_template("mean_size.py")

    elif i.page == "Significance":

        if i.test == "Proportions":
            if i.method == "Permutation":
                template = env.get_template("prop_signif_comp.py")
            elif i.method == "Z-test":
                template = env.get_template("prop_signif_freq.py")

        elif i.test == "Means":
            if i.method == "Permutation":
                template = env.get_template("mean_signif_comp.py")
            elif i.method == "t-test" or i.method == "Z-test":
                template = env.get_template("mean_signif_freq.py")

    code = template.render(i=i)
    with st.expander("Show code"):
        st.code(code, language="python")

    env = load_env("reports")
    template = env.get_template("heights.html")
    html = template.render(
        height_large=screen["large"],
        height_small=screen["small"]
    )
    st.markdown(html, unsafe_allow_html=True)

