import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import sus as sus
from scripts import utils as ut

ut.intro("SUS", "sus")

st.caption(
    """
    From: Brooke, John. (1995). SUS: A quick and dirty usability scale. Usability Eval. Ind.. 189. [Article link](https://www.researchgate.net/publication/228593520_SUS_A_quick_and_dirty_usability_scale)
    """
)

st.header("1. Downlad and fill the template")

template_path = "templates/template-sus.xlsx"

with open(template_path, "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template-sus.xlsx",
    data=file_bytes,
    file_name="template-sus.xlsx",
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

    res = sus.sus(df_raw)

    st.header("Overview")

    ut.slider_sus(round(res.mci[0]), res.mci_acceptability[0])

    st.header("Mean Score")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci[0])} [{round(res.mci[1])};{round(res.mci[2])}]")
    with col2:
        pass
    bar_chart = alt.Chart(res.df).mark_bar().encode(
        alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[0, 100]),
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

    st.header("Grade")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Grade", res.mci_grade[0], border=True)
        st.write(f"Grade & CI (95%) as Grade: {res.mci_grade[0]} [{res.mci_grade[1]};{res.mci_grade[2]}]")
    with col2:
        # === 1. Base chart: common encoding ===
        base = (
            alt.Chart(res.df)
            .encode(
                x='count()',
                y='Grade:N'
            )
        )

        # === 2. Bar chart showing counts per grade ===
        bars = base.mark_bar().encode(
            alt.Color("Grade:N").scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        # === 3. Labels next to the bars ===
        labels = base.mark_text(
            align='left',
            dx=2
        )

        # === 4. Vertical rule at the mean grade ===
        mean_rule = (
            alt.Chart()  # no data needed for a pure datum-based rule
            .mark_rule(color="red", size=2, strokeDash=[3, 3])
            .encode(
                y=alt.Y(datum=res.mci_grade[0], type="nominal")   # grade = "D"
            )
        )

        mean_text = (
            alt.Chart()
            .mark_text(align='left', dy=-8, color="red")
            .encode(
                y=alt.Y(datum=res.mci_grade[0], type="nominal"),
                x=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        # === 5. Combine all layers into one plot ===
        plot = (bars + labels + mean_rule + mean_text).properties(title="Grades Distribution & Mean")

        st.altair_chart(plot)

    st.header("Acceptability")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Acceptability", res.mci_acceptability[0], border=True)
        st.write(f"Acceptability & CI (95%) as Acceptability: {res.mci_acceptability[0]} [{res.mci_acceptability[1]};{res.mci_acceptability[2]}]")
    with col2:
        # === 1. Base chart: common encoding ===
        base = (
            alt.Chart(res.df)
            .encode(
                x='count()',
                y='Acceptability:N'
            )
        )

        # === 2. Bar chart showing counts per grade ===
        bars = base.mark_bar().encode(
            alt.Color("Acceptability:N").scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        # === 3. Labels next to the bars ===
        labels = base.mark_text(
            align='left',
            dx=2
        )

        # === 4. Vertical rule at the mean grade ===
        mean_rule = (
            alt.Chart()  # no data needed for a pure datum-based rule
            .mark_rule(color="red", size=2, strokeDash=[3, 3])
            .encode(
                y=alt.Y(datum=res.mci_acceptability[0], type="nominal")   # grade = "D"
            )
        )

        mean_text = (
            alt.Chart()
            .mark_text(align='left', dy=-8, color="red")
            .encode(
                y=alt.Y(datum=res.mci_acceptability[0], type="nominal"),
                x=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        # === 5. Combine all layers into one plot ===
        plot = (bars + labels + mean_rule + mean_text).properties(title="Acceptability Distribution & Mean")

        st.altair_chart(plot)

    st.header("Learnability")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Learnability", round(res.mci_learnability[0]), border=True)
        st.write(f"Learnability & CI (95%): {round(res.mci_learnability[0])} [{round(res.mci_learnability[1])};{round(res.mci_learnability[2])}]")
        st.caption("No official learnability formula found; using the overall mean method: sum x (100 / (2x4)).")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Learnability:Q").bin(maxbins=20).scale(domain=[1, 100]),
            alt.Y('count()'),
            alt.Color("Learnability:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_learnability[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_learnability[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Learnability Distribution & Mean")

        st.altair_chart(plot)

    st.header("Usability")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Usability", round(res.mci_usability[0]), border=True)
        st.write(f"Usability & CI (95%): {round(res.mci_usability[0])} [{round(res.mci_usability[1])};{round(res.mci_usability[2])}]")
        st.caption("No official usability formula found; using the overall mean method: sum x (100 / (8x4)).")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Usability:Q").bin(maxbins=20).scale(domain=[1, 100]),
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

        plot = (bar_chart + mean_line + mean_text).properties(title="Usability Distribution & Mean")

        st.altair_chart(plot)

    ut.show_data(df_raw, res.df)
