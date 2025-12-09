import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import umuxlite as uml
from scripts import utils as ut

ut.intro("UMUX-Lite", "umux_lite")

st.caption(
    """
    From: Lewis, James R. et al. “UMUX-LITE: when there’s no time for the SUS.” Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (2013): n. pag. [Article link](https://www.semanticscholar.org/paper/UMUX-LITE%3A-when-there's-no-time-for-the-SUS-Lewis-Utesch/33995b2a7d85d2247ba1cd5ac5777da9248e82e8)
    """
)

st.header("1. Downlad and fill the template")

template_path = "templates/template-umux_lite.xlsx"

with open(template_path, "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template-umux_lite.xlsx",
    data=file_bytes,
    file_name="template-umux_lite.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="content"
)

st.header("2. Drop your Excel file")
uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx", "xls"], label_visibility="collapsed")
st.caption("Only 7-point scales are supported.")

if st.button("Show an exemple", type="tertiary"):
    uploaded_file = template_path

if uploaded_file is not None:

    # Lecture des données
    df_raw = pd.read_excel(uploaded_file)

    res = uml.umuxlite(df_raw)

    st.header("SUS Predicted Overview")

    ut.slider_sus(round(res.mci_sus[0]), res.mci_sus_acceptability[0])

    st.header("Mean Score")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci[0])} [{round(res.mci[1])};{round(res.mci[2])}]")
    with col2:
        pass
    bar_chart = alt.Chart(res.df).mark_bar().encode(
        alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[0, 100]),
        alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
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



    st.header("Usability")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_usability[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_usability[0])} [{round(res.mci_usability[1])};{round(res.mci_usability[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Usability:Q").bin(maxbins=20).scale(domain=[0, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
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

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)



    st.header("Ease of Use")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_easeofuse[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_easeofuse[0])} [{round(res.mci_easeofuse[1])};{round(res.mci_easeofuse[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("EaseOfUse:Q").bin(maxbins=20).scale(domain=[0, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("EaseOfUse:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_easeofuse[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_easeofuse[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)





    st.header("SUS Predicted Score")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Predicted Mean", round(res.mci_sus[0]), border=True)
        st.write(f"Predicted Mean & CI (95%): {round(res.mci_sus[0])} [{round(res.mci_sus[1])};{round(res.mci_sus[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("SUS_Predicted:Q").bin(maxbins=20).scale(domain=[0, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("SUS_Predicted:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_sus[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_sus[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("PREDICTED MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Predicted SUS Scores Distribution & Mean")

        st.altair_chart(plot)

    # st.header("SUS Predicted Grade")
    # col1, col2 = st.columns(2, gap="medium")
    # with col1:
    #     st.metric("Predicted Grade", res.mci_sus_grade[0], border=True)
    #     st.write(f"Grade & CI (95%) as Grade: {res.mci_sus_grade[0]} [{res.mci_sus_grade[1]};{res.mci_sus_grade[2]}]")
    # with col2:
    #     # === 1. Base chart: common encoding ===
    #     base = (
    #         alt.Chart(res.df)
    #         .encode(
    #             x='count()',
    #             y='SUS_Grade:N'
    #         )
    #     )

    #     # === 2. Bar chart showing counts per grade ===
    #     bars = base.mark_bar().encode(
    #         alt.Color("SUS_Grade:N").scale(scheme="redyellowgreen", reverse=True).legend(None)
    #     )

    #     # === 3. Labels next to the bars ===
    #     labels = base.mark_text(
    #         align='left',
    #         dx=2
    #     )

    #     # === 4. Vertical rule at the mean grade ===
    #     mean_rule = (
    #         alt.Chart()  # no data needed for a pure datum-based rule
    #         .mark_rule(color="red", size=2, strokeDash=[3, 3])
    #         .encode(
    #             y=alt.Y(datum=res.mci_sus_grade[0], type="nominal")   # grade = "D"
    #         )
    #     )

    #     mean_text = (
    #         alt.Chart()
    #         .mark_text(align='left', dy=-8, color="red")
    #         .encode(
    #             y=alt.Y(datum=res.mci_sus_grade[0], type="nominal"),
    #             x=alt.Y(datum=0.5, type="quantitative"),
    #             text=alt.value("PREDICTED MEAN")
    #         )
    #     )

    #     # === 5. Combine all layers into one plot ===
    #     plot = (bars + labels + mean_rule + mean_text).properties(title="Grades Distribution & Mean")

    #     st.altair_chart(plot)

    # st.header("SUS Predicted Acceptability")
    # col1, col2 = st.columns(2, gap="medium")
    # with col1:
    #     st.metric("Predicted Acceptability", res.mci_sus_acceptability[0], border=True)
    #     st.write(f"Acceptability & CI (95%) as Acceptability: {res.mci_sus_acceptability[0]} [{res.mci_sus_acceptability[1]};{res.mci_sus_acceptability[2]}]")
    # with col2:
    #     # === 1. Base chart: common encoding ===
    #     base = (
    #         alt.Chart(res.df)
    #         .encode(
    #             x='count()',
    #             y='SUS_Acceptability:N'
    #         )
    #     )

    #     # === 2. Bar chart showing counts per grade ===
    #     bars = base.mark_bar().encode(
    #         alt.Color("SUS_Acceptability:N").scale(scheme="redyellowgreen", reverse=True).legend(None)
    #     )

    #     # === 3. Labels next to the bars ===
    #     labels = base.mark_text(
    #         align='left',
    #         dx=2
    #     )

    #     # === 4. Vertical rule at the mean grade ===
    #     mean_rule = (
    #         alt.Chart()  # no data needed for a pure datum-based rule
    #         .mark_rule(color="red", size=2, strokeDash=[3, 3])
    #         .encode(
    #             y=alt.Y(datum=res.mci_sus_acceptability[0], type="nominal")   # grade = "D"
    #         )
    #     )

    #     mean_text = (
    #         alt.Chart()
    #         .mark_text(align='left', dy=-8, color="red")
    #         .encode(
    #             y=alt.Y(datum=res.mci_sus_acceptability[0], type="nominal"),
    #             x=alt.Y(datum=0.5, type="quantitative"),
    #             text=alt.value("PREDICTED MEAN")
    #         )
    #     )

    #     # === 5. Combine all layers into one plot ===
    #     plot = (bars + labels + mean_rule + mean_text).properties(title="Acceptability Distribution & Mean")

    #     st.altair_chart(plot)

    ut.show_data(df_raw, res.df)
