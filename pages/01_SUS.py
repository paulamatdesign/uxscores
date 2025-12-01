import streamlit as st
import pandas as pd
import openpyxl as pxl
import altair as alt
import pandas as pd
import numpy as np
from scipy import stats
#from plotnine import ggplot, aes, geom_col, labs

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

    df_processed = df_raw.copy()

    # Apply SUS scoring rules
    for i, col in enumerate(df_processed.columns, start=1):
        if i % 2 == 1:  
            # Odd-numbered items
            df_processed[col] = df_processed[col] - 1
        else:           
            # Even-numbered items
            df_processed[col] = 5 - df_processed[col]

    # Sum across the 10 items
    df_processed["UserScore"] = df_processed.sum(axis=1) * 2.5
    col = df_processed.pop("UserScore")   # remove the column
    df_processed.insert(0, "UserScore", col)  # reinsert at position 0

    def as_grade(s):
        if s <= 60:
            return 'F'
        elif s > 60 and s <= 70:
            return 'D'
        elif s > 70 and s <= 80:
            return 'C'
        elif s > 80 and s <= 90:
            return 'B'
        elif s > 90 and s <= 100:
            return 'A'

    df_processed['Grades'] = df_processed['UserScore'].apply(as_grade)
    col = df_processed.pop("Grades")   # remove the column
    df_processed.insert(0, "Grades", col)  # reinsert at position 0

    def as_acceptability(s):
        if s <= 50:
            return "NAC"   # Not Acceptable
        elif s <= 62:
            return "MAL"   # Marginal Low
        elif s <= 70:
            return "MAH"   # Marginal High
        else:
            return "ACP"   # Acceptable

    df_processed['Acceptability'] = df_processed['UserScore'].apply(as_acceptability)
    col = df_processed.pop("Acceptability")   # remove the column
    df_processed.insert(0, "Acceptability", col)  # reinsert at position 0

    score = round(df_processed["UserScore"].mean())
    grade = as_grade(score)
    acceptability = as_acceptability(score)

    # 1. Extract the SUS scores from the DataFrame
    scores = df_processed["UserScore"].dropna()

    # 2. Sample size
    n = len(scores)

    # 3. Sample mean
    sus_mean = score

    # 4. Sample standard deviation (unbiased, ddof=1)
    sus_sd = scores.std(ddof=1)

    # 5. Standard error of the mean
    sus_se = sus_sd / np.sqrt(n)

    # 6. Degrees of freedom
    dfree = n - 1

    # 7. t critical value for 95% CI (two-tailed)
    alpha = 0.05
    t_crit = stats.t.ppf(1 - alpha/2, dfree)
    
    # 8. Margin of error
    margin = t_crit * sus_se

    # 9. Confidence interval bounds
    ci_low = round(sus_mean - margin)
    ci_low_grade = as_grade(ci_low)
    ci_low_acceptability = as_acceptability(ci_low)

    ci_high = round(sus_mean + margin)
    ci_high_grade = as_grade(ci_high)
    ci_high_acceptability = as_acceptability(ci_high)

    st.subheader("Score")

    if n < 8:
        st.warning("Sample size is less than 8. The CI calculation may not be reliable.")

    if score < 0 or score > 100:
        st.error("The calculated SUS score is out of bounds (0-100). Please check your data.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Score", score, border=True)
    with col2:
        st.metric("Score & CI (95%)", f"{score} [{ci_low};{ci_high}]", border=False)

    bar_chart = alt.Chart(df_processed).mark_bar().encode(
        alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[0, 100]),
        alt.Y('count()'),
        alt.Color("UserScore:Q").bin(maxbins=20).scale(scheme="redyellowgreen").legend(None)
    )

    mean_line = alt.Chart(pd.DataFrame({'mean_score': [score]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
        x='mean_score:Q',
        tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
    )

    mean_text = (
        alt.Chart(pd.DataFrame({'mean_score': [score]}))
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
        st.metric("Grade", grade, border=True)
    with col2:
        st.metric("Grade & CI (95%) as Grade", f"{grade} [{ci_low_grade};{ci_high_grade}]", border=False)

    # === 1. Base chart: common encoding ===
    base = (
        alt.Chart(df_processed)
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
            y=alt.Y(datum=grade, type="nominal")   # grade = "D"
        )
    )

    mean_text = (
        alt.Chart()
        .mark_text(align='left', dy=-8, color="red")
        .encode(
            y=alt.Y(datum=grade, type="nominal"),
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
        st.metric("Acceptability", acceptability, border=True)
    with col2:
        st.metric("Acceptability & CI (95%) as Acceptability", f"{acceptability} [{ci_low_acceptability};{ci_high_acceptability}]", border=False)

    # === 1. Base chart: common encoding ===
    base = (
        alt.Chart(df_processed)
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
            y=alt.Y(datum=acceptability, type="nominal")   # grade = "D"
        )
    )

    mean_text = (
        alt.Chart()
        .mark_text(align='left', dy=-8, color="red")
        .encode(
            y=alt.Y(datum=acceptability, type="nominal"),
            x=alt.Y(datum=0.5, type="quantitative"),
            text=alt.value("MEAN")
        )
    )

    # === 5. Combine all layers into one plot ===
    plot = (bars + labels + mean_rule + mean_text).properties(title="Acceptability Distribution & Mean")

    st.altair_chart(plot)

    st.caption("NAC: Not Acceptable, MAL: Marginal Low, MAH: Marginal High, ACP: Acceptable.")

    st.subheader("Data")

    data_type = st.segmented_control("Type", ["Raw", "Processed"], label_visibility="collapsed", default="Raw")
    if data_type == "Raw":
        st.write(df_raw)
    elif data_type == "Processed":
        st.write(df_processed)

st.divider()

with st.expander("About SUS"):
    # Read the markdown file
    with open("descriptions/sus.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    # Display it in Streamlit
    st.markdown(md_text)

    #     p = (
    #         ggplot(plot_df, aes(x="colonne", y="moyenne")) +
    #         geom_col() +
    #         labs(title="Moyenne de la colonne", x="", y="Moyenne")
    #     )

    #     st.pyplot(p.draw())
