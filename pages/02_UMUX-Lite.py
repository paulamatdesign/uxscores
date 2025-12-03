import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import umuxlite as uml
from scripts import utils as ut

ut.intro("UMUX-Lite", "umux_lite")

st.header("1. Downlad and fill the template")
with open("templates/template-umux_lite.xlsx", "rb") as f:
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
    uploaded_file = "templates/template-umux_lite.xlsx"

if uploaded_file is not None:

    # Lecture des données
    df_raw = pd.read_excel(uploaded_file)

    res = uml.umuxlite(df_raw)

    st.header("Mean Score")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mean", round(res.mean), border=True)
        st.write(f"Mean & CI (95%): {round(res.mean)} [{round(res.ci[0])};{round(res.ci[1])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[0, 100]),
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

    st.header("SUS Predicted Score")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted Mean", round(res.sus_predicted), border=True)
        st.write(f"Predicted Mean & CI (95%): {round(res.sus_predicted)} [{round(res.sus_predicted_ci[0])};{round(res.sus_predicted_ci[1])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("SUS_Predicted:Q").bin(maxbins=20).scale(domain=[0, 100]),
            alt.Y('count()'),
            alt.Color("SUS_Predicted:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.sus_predicted]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.sus_predicted]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("PREDICTED MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="Predicted SUS Scores Distribution & Mean")

        st.altair_chart(plot)

    st.header("SUS Predicted Grade")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted Grade", res.grade, border=True)
        st.write(f"Grade & CI (95%) as Grade: {res.grade} [{res.sus_predicted_ci_grade[0]};{res.sus_predicted_ci_grade[1]}]")
    with col2:
        # === 1. Base chart: common encoding ===
        base = (
            alt.Chart(res.df)
            .encode(
                x='count()',
                y='Grades:N'
            )
        )

        # === 2. Bar chart showing counts per grade ===
        bars = base.mark_bar().encode(
            alt.Color("Grades:N").scale(scheme="redyellowgreen", reverse=True).legend(None)
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
                y=alt.Y(datum=res.grade, type="nominal")   # grade = "D"
            )
        )

        mean_text = (
            alt.Chart()
            .mark_text(align='left', dy=-8, color="red")
            .encode(
                y=alt.Y(datum=res.grade, type="nominal"),
                x=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("PREDICTED MEAN")
            )
        )

        # === 5. Combine all layers into one plot ===
        plot = (bars + labels + mean_rule + mean_text).properties(title="Grades Distribution & Mean")

        st.altair_chart(plot)

    st.header("SUS Predicted Acceptability")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted Acceptability", res.acceptability, border=True)
        st.write(f"Acceptability & CI (95%) as Acceptability: {res.acceptability} [{res.sus_predicted_ci_acceptability[0]};{res.sus_predicted_ci_acceptability[1]}]")
        st.caption("ACP: Acceptable, MAH: Marginal High, MAL: Marginal Low, NAC: Not Acceptable.")
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
                y=alt.Y(datum=res.acceptability, type="nominal")   # grade = "D"
            )
        )

        mean_text = (
            alt.Chart()
            .mark_text(align='left', dy=-8, color="red")
            .encode(
                y=alt.Y(datum=res.acceptability, type="nominal"),
                x=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("PREDICTED MEAN")
            )
        )

        # === 5. Combine all layers into one plot ===
        plot = (bars + labels + mean_rule + mean_text).properties(title="Acceptability Distribution & Mean")

        st.altair_chart(plot)

    st.divider()

    with st.expander("Data"):
        data_type = st.segmented_control("Type", ["Raw", "Processed"], label_visibility="collapsed", default="Raw")
        if data_type == "Raw":
            st.write(df_raw)
        elif data_type == "Processed":
            st.write(res.df)

