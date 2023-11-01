import base64
import numpy as np
import pandas as pd
import streamlit as st


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" width="300" alt="abtester logo"/>' % b64
    c = st.container()
    c.write(html, unsafe_allow_html=True)
    return


def show_download_button(name, path, file):
    df = pd.read_csv(path+file)
    df = convert_df(df)
    st.download_button(
        label=f"Download {name}",
        data=df,
        file_name=file,
        mime="text/csv",
    )
    return


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

