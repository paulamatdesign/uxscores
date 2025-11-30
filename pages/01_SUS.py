import streamlit as st
import pandas as pd
import openpyxl as pxl
import altair as alt
#from plotnine import ggplot, aes, geom_col, labs

st.set_page_config("SUS", initial_sidebar_state="collapsed")

if st.button("Home", icon=":material/arrow_back:", type="tertiary"):
    st.switch_page("Home.py")
st.title("SUS Score Calculator")

st.write("##### 1. Downlad and fill the template")
with open("templates/template_sus.xlsx", "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template_sus.xlsx",
    data=file_bytes,
    file_name="template_sus.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="content"
)

st.write("##### 2. Drop your SUS Excel file")
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

    def to_grade(s):
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

    df_processed['Grades'] = df_processed['UserScore'].apply(to_grade)
    col = df_processed.pop("Grades")   # remove the column
    df_processed.insert(0, "Grades", col)  # reinsert at position 0

    def to_acceptability(s):
        if s <= 50:
            return 'Not Acceptable'
        elif s > 50 and s <= 62:
            return 'Marginal Low'
        elif s > 62 and s <= 70:
            return 'Marginal High'
        elif s > 70 and s <= 100:
            return 'Acceptable'

    df_processed['Acceptability'] = df_processed['UserScore'].apply(to_acceptability)
    col = df_processed.pop("Acceptability")   # remove the column
    df_processed.insert(0, "Acceptability", col)  # reinsert at position 0

    score = df_processed["UserScore"].mean()
    grade = to_grade(score)
    acceptability = to_acceptability(score)

    st.divider()

    st.write("##### Stats")

    col1, col2, col3 = st.columns([3, 3, 6])
    with col1:
        st.metric("Score", score, border=True)
    with col2:
        st.metric("Grade", grade, border=True)
    with col3:
        st.metric("Acceptability", acceptability, border=True)

    st.write("##### Visuals")

    # 2. Create the Altair Bar Chart (your original plot)
    bar_chart = alt.Chart(df_processed).mark_bar().encode(
        alt.X("UserScore:Q").bin(maxbins=20).scale(domain=[0, 100]),
        alt.Y('count()'),
        alt.Color("UserScore:Q").bin(maxbins=20).scale(scheme="darkmulti")
    )

    # 3. Create the Vertical Line for the Mean
    mean_line = alt.Chart(pd.DataFrame({'mean_score': [score]})).mark_rule(color='red', strokeWidth=3).encode(
        x='mean_score:Q',
        tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
    )

    # 4. Layer the Bar Chart and the Mean Line
    plot = (bar_chart + mean_line).interactive()

    st.altair_chart(plot)

    st.write("##### Data")

    data_type = st.segmented_control("Type", ["Raw", "Processed"], label_visibility="collapsed", default="Raw")

    if data_type == "Raw":
        st.write(df_raw)
    elif data_type == "Processed":
        st.write(df_processed)

    #     p = (
    #         ggplot(plot_df, aes(x="colonne", y="moyenne")) +
    #         geom_col() +
    #         labs(title="Moyenne de la colonne", x="", y="Moyenne")
    #     )

    #     st.pyplot(p.draw())
