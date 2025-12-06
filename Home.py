import streamlit as st

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
</style>
""", unsafe_allow_html=True)

st.set_page_config("UX Scores", initial_sidebar_state="collapsed")

st.title("UX Scores")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.write(
        """
        Welcome! Select a questionnaire to start calculating UX scores.
        
        All data stays in-app and is never stored, logged, or sent to third parties.
        """
    )

    @st.dialog("About this app")
    def about():
        # Read the markdown file
        with open(f"README.md", "r", encoding="utf-8") as f:
            md_text = f.read()
        # Display it in Streamlit
        st.markdown(md_text)

    if st.button("More infos", icon=":material/info:", type="tertiary"):
        about()    

    st.caption(
        """
        Made by [Paul AMAT](https://paulamatdesign.github.io/).
        """
    )

with col2:
    if st.button("SUS", width="stretch"):
        st.switch_page("pages/01_SUS.py")
    if st.button("UMUX-Lite", width="stretch"):
        st.switch_page("pages/02_UMUX-Lite.py")
    if st.button("UEQ-S", width="stretch"):
        st.switch_page("pages/03_UEQ-S.py")
