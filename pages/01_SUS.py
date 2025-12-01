import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts.sus import sus

st.set_page_config("SUS", initial_sidebar_state="collapsed")

if st.button("Home", icon=":material/arrow_back:", type="tertiary"):
    st.switch_page("Home.py")
st.title("SUS Score Calculator")

st.subheader("1. Downlad and fill the template")
with open("templates/template_sus.xlsx", "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template_sus.xlsx",
    data=file_bytes,
    file_name="template_sus.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="content"
)

st.subheader("2. Drop your SUS Excel file")
uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx", "xls"], label_visibility="collapsed")

if uploaded_file is not None:

    # Lecture des données
    df_raw = pd.read_excel(uploaded_file)

    res = sus(df_raw)

    st.subheader("Score")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", round(res.mean), border=True)
    with col2:
        st.metric("Score & CI (95%)", f"{round(res.mean)} [{round(res.ci_low)};{round(res.ci_high)}]", border=False)

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

    st.subheader("Grade")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Grade", res.grade, border=True)
    with col2:
        st.metric("Grade & CI (95%) as Grade", f"{res.grade} [{res.ci_low_grade};{res.ci_high_grade}]", border=False)

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
            text=alt.value("MEAN")
        )
    )

    # === 5. Combine all layers into one plot ===
    plot = (bars + labels + mean_rule + mean_text).properties(title="Grades Distribution & Mean")

    st.altair_chart(plot)

    st.subheader("Acceptability")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Acceptability", res.acceptability, border=True)
    with col2:
        st.metric("Acceptability & CI (95%) as Acceptability", f"{res.acceptability} [{res.ci_low_acceptability};{res.ci_high_acceptability}]", border=False)

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
            text=alt.value("MEAN")
        )
    )

    # === 5. Combine all layers into one plot ===
    plot = (bars + labels + mean_rule + mean_text).properties(title="Acceptability Distribution & Mean")

    st.altair_chart(plot)

    st.caption("ACP: Acceptable, MAH: Marginal High, MAL: Marginal Low, NAC: Not Acceptable.")

    st.subheader("Data")

    data_type = st.segmented_control("Type", ["Raw", "Processed"], label_visibility="collapsed", default="Raw")
    if data_type == "Raw":
        st.write(df_raw)
    elif data_type == "Processed":
        st.write(res.df)

st.divider()

with st.expander("About SUS"):
    # Read the markdown file
    with open("descriptions/sus.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    # Display it in Streamlit
    st.markdown(md_text)
