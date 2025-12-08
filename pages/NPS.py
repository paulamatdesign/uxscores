import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import nps as nps
from scripts import utils as ut

ut.intro("NPS", "nps")

st.caption(
    """
    From: ---
    """
)

st.header("1. Downlad and fill the template")

template_path = "templates/template-nps.xlsx"

with open(template_path, "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template-nps.xlsx",
    data=file_bytes,
    file_name="template-nps.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="content"
)

st.header("2. Drop your Excel file")
uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx", "xls"], label_visibility="collapsed")

if st.button("Show an exemple", type="tertiary"):
    uploaded_file = template_path

if uploaded_file is not None:

    # Lecture des données
    df_raw = pd.read_excel(uploaded_file)

    res = nps.NPS(df_raw)

    st.header("NPS Overview")

    #ut.slider_sus(round(res.mci[0]), res.mci[0])

    st.header("NPS Score")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Score", round(res.score), border=True)
    with col2:
        st.metric("Interpretation", res.interpretation, border=True)

    base = (
            alt.Chart(res.df)
            .encode(
                y='count()',
                x='Q1:N'
            )
    )

    # === 2. Bar chart showing counts per grade ===
    bars = base.mark_bar().encode(
        alt.Color("Q1:N").scale(scheme="redyellowgreen", reverse=False).legend(None)
    )

    # === 3. Labels next to the bars ===
    labels = base.mark_text(
        align='left',
        dy=2
    )

    # === 5. Combine all layers into one plot ===
    plot = (bars + labels).properties(title="Distribution")

    st.altair_chart(plot)

    st.header("Groups")
    # === 1. Base chart: common encoding ===
    base = (
        alt.Chart(res.df)
        .encode(
            x='count()',
            y='Group:N'
        )
    )

    # === 2. Bar chart showing counts per grade ===
    bars = base.mark_bar().encode(
        alt.Color("Group:N").scale(scheme="redyellowgreen", reverse=False).legend(None)
    )

    # === 3. Labels next to the bars ===
    labels = base.mark_text(
        align='left',
        dx=2
    )

    # === 5. Combine all layers into one plot ===
    plot = (bars + labels).properties(title="Groups Distribution")

    st.altair_chart(plot)

    ut.show_data(df_raw, res.df)

