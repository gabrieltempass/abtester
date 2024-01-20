import base64
from typing import Union

from jinja2 import FileSystemLoader, Environment
import streamlit as st


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" width="300" alt="abtester logo"/>' % b64
    c = st.container()
    c.write(html, unsafe_allow_html=True)
    return


def add_spaces(n):
    for i in range(n):
        st.write("")


def add_header(menu):
    add_spaces(2)
    st.header(menu.capitalize())


def add_subheader(subheader):
    add_spaces(2)
    st.subheader(subheader)


def add_calculate_button():
    if not st.button("Calculate", type="primary"):
        st.stop()


def wait_file(inputs):
    if inputs.df is None and inputs.test == "Means":
        st.error(f"You must choose a file to be able to calculate the {inputs.menu}.")


def prettify_number(number: Union[float, int], decimals: int = 2, sign: str = "", thousand_separator: str = ",") -> str:

# TODO: Update to python 3.10+ to be able to use multiple types this way:
# def prettify_number(number: float|int, decimals: int = 2, sign: str = "") -> str:

    """
    Prettify the passed float or int number into a human-readable string,
    rounded and truncated to the passed number of decimal places.

    This converter prettifies floating-point numbers for human consumption,
    producing more readable results than the default :meth:`float.__str__`
    dunder method. Notably, this converter:

    * Strips all ignorable trailing zeroes and decimal points from this number
      (e.g., ``3`` rather than either ``3.`` or ``3.0``).
    * Rounds to the passed decimals for perceptual uniformity.

    Parameters
    ----------
    number : float | int
        Arbitrary real number to be prettified.
    decimals : int, optional
        **Decimals** (i.e., number of decimal places to round to). Defaults to
        a precision of 2 decimal places.
    sign : str, optional
        Can be "+" or "-". TODO: Describe what each option does.

    Returns
    ----------
    str
        Human-readable string prettified from this floating-point number.

    Raises
    ----------
    ValueError
        If this precision is negative.
    """

    # If this precision is negative, raise an exception.
    if decimals < 0:
        raise ValueError(f"Negative decimals {decimals} unsupported.")
    elif decimals >= 0:
        # String prettified from this number. In order:
        # * Coerce this number into a string rounded to this precision.
        result = f"{number:{sign}{thousand_separator}.{decimals}f}"
    if decimals > 0:
        # * Truncate all trailing zeroes from this string.
        # * Truncate any trailing decimal place if any from this string.
        result = result.rstrip("0").rstrip(".")

    # If rounding this string from a small negative number (e.g., "-0.001")
    # or positive, with the "+" sign, yielded the anomalous result of "-0"
    # or "+0", return "0" instead; else, return this result as is.
    return "0" if result in {"-0", "+0"} else result


def load_env(parent_directory):
    loader = FileSystemLoader(f"templates/{parent_directory}")
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    env.filters["prettify_number"] = prettify_number
    return env

