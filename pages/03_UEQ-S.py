import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import ueqs as ueq
from scripts import utils as ut

ut.intro("UEQ-S", "ueqs")

st.caption(
    """
    From: Laugwitz, B., Schrepp, M. & Held, T. (2008). Construction and evaluation of a user experience questionnaire. In: Holzinger, A. (Ed.): USAB 2008, LNCS 5298, 63-76. [Article link](https://www.researchgate.net/publication/221217803_Construction_and_Evaluation_of_a_User_Experience_Questionnaire)
    """
)

st.header("1. Downlad and fill the template")

template_path = "templates/template-ueqs.xlsx"

with open(template_path, "rb") as f:
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
    uploaded_file = template_path

if uploaded_file is not None:

    # Lecture des données
    df_raw = pd.read_excel(uploaded_file)

    res = ueq.ueqs(df_raw)

    st.header("Overview")

    ut.slider_ueqs(round(res.mci[0]))

    st.header("Overall Mean")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci[0], 1)} [{round(res.mci[1], 1)};{round(res.mci[2], 1)}]")
    with col2:
        pass
    bar_chart = alt.Chart(res.df).mark_bar().encode(
        alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[-3, 3]),
        alt.Y('count()'),
        alt.Color("UserScore:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
    )

    mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
        x='mean_score:Q',
        tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
    )

    mean_text = (
        alt.Chart(pd.DataFrame({'mean_score': [res.mci[0]]}))
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

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Pragmatic Mean", round(res.mci_pragmatic[0], 1), border=True)
        st.write(f"Predicted Mean & CI (95%): {round(res.mci_pragmatic[0], 1)} [{round(res.mci_pragmatic[1], 1)};{round(res.mci_pragmatic[2], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("UserScore_Pragmatic:Q").bin(maxbins=20).scale(domain=[-3, 3]),
            alt.Y('count()'),
            alt.Color("UserScore_Pragmatic:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_pragmatic[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_pragmatic[0]]}))
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

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Hedonic Mean", round(res.mci_hedonic[0], 1), border=True)
        st.write(f"Predicted Mean & CI (95%): {round(res.mci_hedonic[0], 1)} [{round(res.mci_hedonic[1], 1)};{round(res.mci_hedonic[2], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("UserScore_Hedonic:Q").bin(maxbins=20).scale(domain=[-3, 3]),
            alt.Y('count()'),
            alt.Color("UserScore_Hedonic:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_hedonic[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_hedonic[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Predicted SUS Scores Distribution & Mean")

        st.altair_chart(plot)

    ut.show_data(df_raw, res.df)
