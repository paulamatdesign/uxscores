import streamlit as st

st.set_page_config("UX Scores", initial_sidebar_state="collapsed")
st.title("UX Scores")

st.write("Welcome! Select a questionnaire to start calculating UX scores.")

if st.button("SUS *(System Usability Scale)*", icon=":material/arrow_forward:", width="stretch"):
    st.switch_page("pages/01_SUS.py")
if st.button("UMUX-Lite *(Usability Metric for User Experience – Lite)*", icon=":material/arrow_forward:", width="stretch"):
    st.switch_page("pages/02_UMUX-Lite.py")
if st.button("UEQ-S *(User Experience Questionnaire – Short)*", icon=":material/arrow_forward:", width="stretch"):
    st.switch_page("pages/03_UEQ-S.py")
