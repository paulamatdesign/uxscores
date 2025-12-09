import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import csuq_short as csuqs
from scripts import utils as ut

ut.intro("CSUQ-Short", "csuq_short")

st.caption(
    """
    From: Lewis, James & R., James. (1995). IBM Computer Usability Satisfaction Questionnaires: Psychometric Evaluation and Instructions for Use. International Journal of Human-Computer Interaction. 7. 57-. 10.1080/10447319509526110. [Article link](https://www.researchgate.net/publication/200085994_IBM_Computer_Usability_Satisfaction_Questionnaires_Psychometric_Evaluation_and_Instructions_for_Use)
    """
)

st.header("1. Downlad and fill the template")

template_path = "templates/template-csuq_short.xlsx"

with open(template_path, "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template-csuq_short.xlsx",
    data=file_bytes,
    file_name="template-csuq_short.xlsx",
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

    res = csuqs.csuq_short(df_raw)

    st.header("CSUQ Overview")

    csuqs.slider_csuq_short(round(res.mci[0], 1), csuqs.csuq_interpret(round(res.mci[0], 1)))

    st.header("Mean Score")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci[0], 1)} [{round(res.mci[1], 1)};{round(res.mci[2], 1)}]")
    with col2:
        pass

    bar_chart = alt.Chart(res.df).mark_bar().encode(
        alt.X("OverallMean:Q").bin(maxbins=20).scale(domain=[1, 7]),
        alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
        alt.Color("OverallMean:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
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



    st.header("Interpretation")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Interpretation", csuqs.csuq_interpret(round(res.mci[0], 1)), border=True)
        st.write(f"Acceptability & CI (95%) as Acceptability: {csuqs.csuq_interpret(round(res.mci[0], 1))} [{csuqs.csuq_interpret(round(res.mci[1], 1))};{csuqs.csuq_interpret(round(res.mci[2], 1))}]")
    with col2:
        # === 1. Base chart: common encoding ===
        base = (
            alt.Chart(res.df)
            .encode(
                x=alt.X('count()', axis=alt.Axis(tickMinStep=1, format='d')),
                y='OverallInterpretation:N'
            )
        )

        # === 2. Bar chart showing counts per grade ===
        bars = base.mark_bar().encode(
            alt.Color("OverallInterpretation:N").scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        # === 3. Labels next to the bars ===
        labels = base.mark_text(
            align='left',
            dx=2
        )

        # === 5. Combine all layers into one plot ===
        plot = (bars + labels).properties(title="Distribution & Mean")

        st.altair_chart(plot)





    st.header("System Usefulness")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_system_usefulness[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_system_usefulness[0], 1)} [{round(res.mci_system_usefulness[1], 1)};{round(res.mci_system_usefulness[2], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("SystemUsefulness:Q").bin(maxbins=20).scale(domain=[1, 7]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("SystemUsefulness:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_system_usefulness[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_system_usefulness[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)



    st.header("Information Quality")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_information_quality[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_information_quality[0], 1)} [{round(res.mci_information_quality[1], 1)};{round(res.mci_information_quality[2], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("InformationQuality:Q").bin(maxbins=20).scale(domain=[1, 7]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("InformationQuality:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_information_quality[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_information_quality[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)


    
    st.header("Interface Quality")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_interface_quality[0], 1), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_interface_quality[0], 1)} [{round(res.mci_interface_quality[1], 1)};{round(res.mci_interface_quality[2], 1)}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("InterfaceQuality:Q").bin(maxbins=20).scale(domain=[1, 7]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("InterfaceQuality:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_interface_quality[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_interface_quality[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)





    

    ut.show_data(df_raw, res.df)
