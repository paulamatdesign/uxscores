import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import nasa_tlx as tlx
from scripts import utils as ut

ut.intro("NASA-TLX", "nasa_tlx")

st.caption("From: Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. In Advances in psychology (pp. 139–183).")

st.header("1. Downlad and fill the template")

template_path = "templates/template-nasa_tlx.xlsx"

with open(template_path, "rb") as f:
        file_bytes = f.read()

st.download_button(
    label=":material/download: template-nasa_tlx.xlsx",
    data=file_bytes,
    file_name="template-nasa_tlx.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="content"
)

st.header("2. Drop your Excel file")
uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx", "xls"], label_visibility="collapsed")

ut.caption_important("Only 21-points scales are supported.")

if st.button("Show an exemple", type="tertiary"):
    uploaded_file = template_path

if uploaded_file is not None:

    # Lecture des données
    df_raw = pd.read_excel(uploaded_file)

    res = tlx.NASATLX(df_raw)

    st.header("Overview")

    tlx.slider_nasa_tlx(round(res.mci[0]), tlx.nasa_tlx_interpret(round(res.mci[0])))

    st.header("Mean Score")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci[0])} [{round(res.mci[1])};{round(res.mci[2])}]")
    with col2:
        pass

    bar_chart = alt.Chart(res.df).mark_bar().encode(
        alt.X("Mean:Q").bin(maxbins=20).scale(domain=[1, 100]),
        alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
        alt.Color("Mean:Q").bin(maxbins=20).scale(scheme="redyellowgreen", reverse=True).legend(None)
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
        st.metric("Interpretation", tlx.nasa_tlx_interpret(round(res.mci[0])), border=True)
        st.write(f"Interpretation & CI (95%) as Interpretation: {tlx.nasa_tlx_interpret(round(res.mci[0]))} [{tlx.nasa_tlx_interpret(round(res.mci[1]))};{tlx.nasa_tlx_interpret(round(res.mci[2]))}]")
    with col2:
        # === 1. Base chart: common encoding ===
        base = (
            alt.Chart(res.df)
            .encode(
                x=alt.X('count()', axis=alt.Axis(tickMinStep=1, format='d')),
                y='MeanInterpretation:N'
            )
        )

        # === 2. Bar chart showing counts per grade ===
        bars = base.mark_bar().encode(
            alt.Color("MeanInterpretation:N").scale(scheme="redyellowgreen", reverse=False).legend(None)
        )

        # === 3. Labels next to the bars ===
        labels = base.mark_text(
            align='left',
            dx=2
        )

        # === 5. Combine all layers into one plot ===
        plot = (bars + labels).properties(title="Distribution & Mean")

        st.altair_chart(plot)




    st.header("Mental Demand")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_mental_demand[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_mental_demand[0])} [{round(res.mci_mental_demand[1])};{round(res.mci_mental_demand[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Q1:Q").bin(maxbins=20).scale(domain=[1, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("Q1:Q").bin(maxbins=20).scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_mental_demand[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_mental_demand[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)




    st.header("Physical Demand")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_physical_demand[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_physical_demand[0])} [{round(res.mci_physical_demand[1])};{round(res.mci_physical_demand[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Q2:Q").bin(maxbins=20).scale(domain=[1, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("Q2:Q").bin(maxbins=20).scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_physical_demand[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_physical_demand[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)






    st.header("Temporal Demand")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_temporal_demand[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_temporal_demand[0])} [{round(res.mci_temporal_demand[1])};{round(res.mci_temporal_demand[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Q3:Q").bin(maxbins=20).scale(domain=[1, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("Q3:Q").bin(maxbins=20).scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_temporal_demand[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_temporal_demand[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)




    st.header("Performance")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_performance[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_performance[0])} [{round(res.mci_performance[1])};{round(res.mci_performance[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Q4:Q").bin(maxbins=20).scale(domain=[1, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("Q4:Q").bin(maxbins=20).scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_performance[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_performance[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)




    st.header("Effort")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_effort[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_effort[0])} [{round(res.mci_effort[1])};{round(res.mci_effort[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Q5:Q").bin(maxbins=20).scale(domain=[1, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("Q5:Q").bin(maxbins=20).scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_effort[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_effort[0]]}))
            .mark_text(align='left', dx=8, color="red")
            .encode(
                x='mean_score:Q',
                y=alt.Y(datum=0.5, type="quantitative"),
                text=alt.value("MEAN")
            )
        )

        plot = (bar_chart + mean_line + mean_text).properties(title="User Scores Distribution & Mean")

        st.altair_chart(plot)






    st.header("Frustration")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.metric("Mean", round(res.mci_frustration[0]), border=True)
        st.write(f"Mean & CI (95%): {round(res.mci_frustration[0])} [{round(res.mci_frustration[1])};{round(res.mci_frustration[2])}]")
    with col2:
        bar_chart = alt.Chart(res.df).mark_bar().encode(
            alt.X("Q6:Q").bin(maxbins=20).scale(domain=[1, 100]),
            alt.Y('count()', axis=alt.Axis(tickMinStep=1, format='d')),
            alt.Color("Q6:Q").bin(maxbins=20).scale(scheme="redyellowgreen", reverse=True).legend(None)
        )

        mean_line = alt.Chart(pd.DataFrame({'mean_score': [res.mci_frustration[0]]})).mark_rule(color='red', size=2, strokeDash=[3, 3]).encode(
            x='mean_score:Q',
            tooltip=[alt.Tooltip('mean_score', title=f'Mean Score')]
        )

        mean_text = (
            alt.Chart(pd.DataFrame({'mean_score': [res.mci_frustration[0]]}))
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
