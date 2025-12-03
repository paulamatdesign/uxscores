import streamlit as st
import numpy as np
from scipy import stats

@st.dialog("About")
def open_help(file):
    # Read the markdown file
    with open(f"descriptions/{file}.md", "r", encoding="utf-8") as f:
        md_text = f.read()
    # Display it in Streamlit
    st.markdown(md_text)

def intro(questionnaire=str, description=str):
    title = f"{questionnaire} Calculator"
    st.set_page_config(title, initial_sidebar_state="collapsed")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&family=Funnel+Sans:wght@300..800&display=swap');

    html, p {
        font-family: "Funnel Sans", sans-serif !important;
    }

    h1, h2 {
        font-family: "Funnel Display", sans-serif !important;
        font-weight: 800 !important;
    }
                
    h2 {
        margin-top: 1.5rem;
        font-weight: 400 !important;
        opacity: 0.6 !important;
        font-size: medium !important;
        text-transform: uppercase;
        letter-spacing: normal !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("Home", icon=":material/arrow_back:", type="tertiary"):
        st.switch_page("Home.py")
    col1, col2 = st.columns([11, 1])
    with col1:
        st.title(title)
    with col2:
        if st.button("", icon=":material/info:", type="tertiary", help="About"):
            open_help(description)

def ci(x):
    sd = x.std(ddof=1)
    n = len(x)
    se = sd / np.sqrt(n)
    dfree = n - 1
    t_crit = stats.t.ppf(1 - 0.05/2, dfree)
    errormargin = t_crit * se
    ci_low = x.mean() - errormargin
    ci_high = x.mean() + errormargin
    return [ci_low, ci_high]

def sus_as_grade(s):
    if s < 25.1:
        return "F"
    elif s < 51.7:
        return "F"
    elif s < 62.7:
        return "D"
    elif s < 65.0:
        return "C-"
    elif s < 71.1:
        return "C"
    elif s < 72.6:
        return "C+"
    elif s < 74.1:
        return "B-"
    elif s < 77.2:
        return "B"
    elif s < 78.9:
        return "B+"
    elif s < 80.8:
        return "A-"
    elif s < 84.1:
        return "A"
    else:
        return "A+"  # 84.1–100

def sus_as_acceptability(s):
    if s < 51.7:
        return "Not Acceptable"
    elif s < 71.1:
        return "Marginal"
    else:
        return "Acceptable"

def show_data(raw, proc):
    st.header("Data")
    with st.expander("Show data"):
        st.caption("Raw")
        st.write(raw)
        st.caption("Processed")
        st.write(proc)