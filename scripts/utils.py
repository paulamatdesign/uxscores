import streamlit as st
import numpy as np
from scipy import stats

def header():
    st.html(
        """
            <style>
                h2 {
                    margin-top: 1.5rem;
                    font-weight: 400 !important;
                    opacity: 0.6 !important;
                    font-size: medium !important;
                    text-transform: uppercase;
                    letter-spacing: normal !important;
                }
        """
    )
    if st.button("Home", icon=":material/arrow_back:", type="tertiary"):
        st.switch_page("Home.py")

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
