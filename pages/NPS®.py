import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import nps as nps
from scripts import utils as ut

ut.intro("NPS®", "nps")

st.caption(
    """
    Net Promoter®, NPS®, NPS Prism®, and the NPS-related emoticons are registered trademarks of Bain & Company, Inc., NICE Systems, Inc., and Fred Reichheld. Net Promoter ScoreSM and Net Promoter SystemSM are service marks of Bain & Company, Inc., NICE Systems, Inc., and Fred Reichheld.
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

    st.header("Overview")

    nps.slider_nps(round(res.score), res.interpretation)

    st.header("NPS")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Score", f"{round(res.score)}%", border=True)
    with col2:
        st.metric("Interpretation", res.interpretation, border=True)

    base = (
        alt.Chart(res.df)
        .encode(
            x=alt.X('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            y='Q1:O'
        )
    )

    # === 2. Bar chart showing counts per grade ===
    bars = base.mark_bar().encode(
        alt.Color("Q1:O").scale(scheme="redyellowgreen", reverse=False).legend(None)
    )

    # === 3. Labels next to the bars ===
    labels = base.mark_text(
        align='left',
        dy=2
    )

    # === 5. Combine all layers into one plot ===
    plot = (bars + labels).properties(title="Distribution")

    st.altair_chart(plot)

    ut.plot_save_info()

    st.header("Groups")
    # === 1. Base chart: common encoding ===
    base = (
        alt.Chart(res.df)
        .encode(
            x=alt.X('count()', axis=alt.Axis(tickMinStep=1, format='d')),
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