import streamlit as st
import numpy as np
from scipy import stats
import altair as alt

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

def mci(x):
    mean = x.mean()
    sd = x.std(ddof=1)
    n = len(x)
    se = sd / np.sqrt(n)
    dfree = n - 1
    t_crit = stats.t.ppf(1 - 0.05/2, dfree)
    errormargin = t_crit * se
    ci_low = mean - errormargin
    ci_high = mean + errormargin
    return [mean, ci_low, ci_high]

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
        return "Not-Acceptable"
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

def slider_sus(score, acceptability):
    """Load and display an SVG file in Streamlit."""
    with open("assets/slider-sus.svg", "r") as f:
        svg = f.read()
    svg = svg.replace("*sc*", str(score))
    svg = svg.replace('width="822"', 'width=100%')
    css1 = f"<style>#Not-Acceptable, #Marginal, #Acceptable {{opacity: 0;}} #frame-Not-Acceptable, #frame-Marginal, #frame-Acceptable {{opacity: 0.5;}}</style>"
    css2 = f"<style>#{acceptability}, #frame-{acceptability} {{opacity: 1 !important;}}</style>"
    html = css1 + css2 + svg
    # Streamlit doesn't render raw SVG directly, so wrap it in HTML
    st.markdown(f"<div style='max-width: 100%;'>{html}</div>", unsafe_allow_html=True)

def slider_ueqs(score):
    """Load and display an SVG file in Streamlit."""
    with open("assets/slider-ueqs.svg", "r") as f:
        svg = f.read()
    svg = svg.replace("*sc*", str(score))
    svg = svg.replace('width="822"', 'width=100%')
    css1 = f"<style>#bubble-3, #bubble-2, #bubble-1, #bubble0, #bubble1, #bubble2, #bubble3 {{opacity: 0;}} #frame-3, #frame-2, #frame-1, #frame0, #frame1, #frame2, #frame3 {{opacity: 0.5;}}</style>"
    css2 = f"<style>#bubble{score}, #frame{score} {{opacity: 1 !important;}}</style>"
    html = css1 + css2 + svg
    # Streamlit doesn't render raw SVG directly, so wrap it in HTML
    st.markdown(f"<div style='max-width: 100%;'>{html}</div>", unsafe_allow_html=True)

def plot_save_info():
    st.info("Select the three dots on the up-right corner of a plot to save as PNG or SVG!", icon="💡")
