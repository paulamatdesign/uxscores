import streamlit as st
import pandas as pd
import os

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

col1, col2 = st.columns([11, 1])
with col1:
    st.title("UX Scores")
with col2:
    @st.dialog("About this app")
    def about():
        # Read the markdown file
        with open(f"README.md", "r", encoding="utf-8") as f:
            md_text = f.read()
        # Display it in Streamlit
        st.markdown(md_text)
    if st.button("", icon=":material/info:", type="tertiary", help="About"):
        about()

st.write("Welcome! Select a questionnaire to start calculating UX scores.")

st.caption(
    """
        Made by [Paul AMAT](https://paulamatdesign.github.io/). All data stays in-app and is never stored, logged, or sent to third parties.
    """
)

st.space()

df = pd.read_csv("assets/questionnaires.csv", sep=";")

df["Short"] = [True if int(x) <= 10 else False for x in df["Items"]]

col1, col2 = st.columns([4, 8], gap="large")

with col1:
    options = ["All"] + df["Scope"].unique().tolist()
    selection = st.selectbox("Scope", options)
    if selection != "All":
        df = df[df["Scope"] == selection]

    options = ["All"] + df["Measures"].unique().tolist()
    selection = st.selectbox("Measures", options)
    if selection != "All":
        df = df[df["Measures"] == selection]

    options = ["All"] + df["Sub_constructs"].unique().tolist()
    selection = st.selectbox("Sub-constructs", options)
    if selection != "All":
        df = df[df["Sub_constructs"] == selection]

    options = ["True", "False"]
    selection = st.toggle("Short only", False)
    if selection:
        df = df[df["Short"] == True]

    options = ["True", "False"]
    selection = st.toggle("Free only", False)
    if selection:
        df = df[df["Free"] == True]

with col2:
    df = df.sort_values(by = "Ready", ascending=False)

    if len(df) > 0:
        for name in df["Name"].unique():
            page_path = f"pages/{name}.py"
            if os.path.exists(page_path):
                d = False
                h = ""
            else:
                d = True
                h = "Not available..."
            if st.button(name, width="stretch", disabled=d, help=h, type="primary"):
                st.switch_page(f"pages/{name}.py")

    else:
        st.write("No questionnaire matches your filters.")
