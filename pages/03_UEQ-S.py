import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import ueqs as ueq
from scripts import utils as ut

ut.intro("UEQ-S", "ueqs")

st.header("1. Downlad and fill the template")
with open("templates/template-ueqs.xlsx", "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template-ueqs.xlsx",
    data=file_bytes,
    file_name="template-ueqs.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="content"
)

st.header("2. Drop your Excel file")
uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx", "xls"], label_visibility="collapsed")

if st.button("Show an exemple", type="tertiary"):
    uploaded_file = "templates/template-ueqs.xlsx"

if uploaded_file is not None:

    # Lecture des données
    df_raw = pd.read_excel(uploaded_file)

    res = ueq.ueqs(df_raw)

    st.header("Overall")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mean", round(res.mean, 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mean, 1)} [{round(res.ci[0], 1)};{round(res.ci[1], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[-3, 3]),
            alt.Y('count()'),
            alt.Color("UserScore:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mean]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mean]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)

    st.header("Pragmatic Quality")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pragmatic Mean", round(res.mean_pragmatic, 1), border=True)
        st.write(f"Predicted Mean & CI (95%): {round(res.mean_pragmatic, 1)} [{round(res.ci_pragmatic[0], 1)};{round(res.ci_pragmatic[1], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("UserScore_Pragmatic:Q").bin(maxbins=20).scale(domain=[-3, 3]),
            alt.Y('count()'),
            alt.Color("UserScore_Pragmatic:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mean_pragmatic]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mean_pragmatic]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Predicted SUS Scores Distribution & Mean")

        st.altair_chart(plot)

    st.header("Hedonic Quality")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Hedonic Mean", round(res.mean_hedonic, 1), border=True)
        st.write(f"Predicted Mean & CI (95%): {round(res.mean_hedonic, 1)} [{round(res.ci_hedonic[0], 1)};{round(res.ci_hedonic[1], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("UserScore_Hedonic:Q").bin(maxbins=20).scale(domain=[-3, 3]),
            alt.Y('count()'),
            alt.Color("UserScore_Hedonic:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mean_hedonic]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mean_hedonic]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Predicted SUS Scores Distribution & Mean")

        st.altair_chart(plot)

    with st.expander("Data"):
        data_type = st.segmented_control("Type", ["Raw", "Processed"], label_visibility="collapsed", default="Raw")
        if data_type == "Raw":
            st.write(df_raw)
        elif data_type == "Processed":
            st.write(res.df)
