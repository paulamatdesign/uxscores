import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import suprq as suprq
from scripts import nps as nps
from scripts import utils as ut

ut.intro("SUPR-Q", "suprq")

st.caption("From: Sauro (2015).")

st.header("1. Downlad and fill the template")

template_path = "templates/template-suprq.xlsx"

with open(template_path, "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template-suprq.xlsx",
    data=file_bytes,
    file_name="template-suprq.xlsx",
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

    res = suprq.SUPRQ(df_raw)

    st.header("Overview")

    suprq.slider_suprq(round(res.mci[0], 1), round(res.mci[0]))

    st.header("Overall Mean")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci[0], 1)} [{round(res.mci[1], 1)};{round(res.mci[2], 1)}]")
    with col2:
        pass

    bar_chart = alt.Chart(res.df).mark_bar().encode(
        alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[1, 5]),
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

    ut.plot_save_info()




    st.header("Usability")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_usability[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_usability[0], 1)} [{round(res.mci_usability[1], 1)};{round(res.mci_usability[2], 1)}]")
    with col2:

        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Usability:Q").bin(maxbins=20).scale(domain=[1, 5]),
            alt.Y('count()'),
            alt.Color("Usability:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_usability[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_usability[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Distribution & Mean")

        st.altair_chart(plot)




    st.header("Credibility")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_credibility[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_credibility[0], 1)} [{round(res.mci_credibility[1], 1)};{round(res.mci_credibility[2], 1)}]")
    with col2:

        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Credibility:Q").bin(maxbins=20).scale(domain=[1, 5]),
            alt.Y('count()'),
            alt.Color("Credibility:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_credibility[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_credibility[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Distribution & Mean")

        st.altair_chart(plot)



    st.header("Loyalty")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_loyalty[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_loyalty[0], 1)} [{round(res.mci_loyalty[1], 1)};{round(res.mci_loyalty[2], 1)}]")
    with col2:

        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Loyalty:Q").bin(maxbins=20).scale(domain=[1, 5]),
            alt.Y('count()'),
            alt.Color("Loyalty:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_loyalty[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_loyalty[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Distribution & Mean")

        st.altair_chart(plot)




    st.header("Appearance")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_appearance[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_appearance[0], 1)} [{round(res.mci_appearance[1], 1)};{round(res.mci_appearance[2], 1)}]")
    with col2:

        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Appearance:Q").bin(maxbins=20).scale(domain=[1, 5]),
            alt.Y('count()'),
            alt.Color("Appearance:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_appearance[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_appearance[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Distribution & Mean")

        st.altair_chart(plot)




    st.header("Interpretation")

    ut.caption_important("It is recommended to purchase a MeasuringU license (https://measuringu.com/product/suprq/) in order to obtain your SUPR-Q percentile and benchmark it against hundreds of websites and organizations across multiple sectors.")

    df_nps = pd.DataFrame()
    df_nps["Q1"] = df_raw["Q5"]
    res_nps = nps.NPS(df_nps)

    st.header("NPS")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Score", f"{round(res_nps.score)}%", border=True)
    with col2:
        st.metric("Interpretation", res_nps.interpretation, border=True)

    base = (
        alt.Chart(res_nps.df)
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

    ut.show_data(df_raw, res.df)
