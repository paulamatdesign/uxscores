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

st.title("UX Scores")

st.write(
    """
    Welcome! Select a questionnaire to start calculating UX scores. All data stays in-app and is never stored, logged, or sent to third parties.
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

df = pd.read_csv("assets/questionnaires.csv")

df["Length"] = ["Short" if int(x) <= 10 else "Long" for x in df["Items"]]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    options = ["All"] + df["Scope"].unique().tolist()
    selection = st.selectbox("Scope", options)
    if selection != "All":
        df = df[df["Scope"] == selection]

with col2:
    options = ["All"] + df["Length"].unique().tolist()
    selection = st.selectbox("Length", options)
    if selection != "All":
        df = df[df["Length"] == selection]

with col3:
    options = ["All"] + df["Measures"].unique().tolist()
    selection = st.selectbox("Measures", options)
    if selection != "All":
        df = df[df["Measures"] == selection]

with col4:
    options = ["All"] + df["Sub_constructs"].unique().tolist()
    selection = st.selectbox("Sub-constructs", options)
    if selection != "All":
        df = df[df["Sub_constructs"] == selection]

with col5:
    options = ["True", "False"]
    selection = st.toggle("Free only", False)
    if selection:
        df = df[df["Free"] == True]

df = df.sort_values(by = "Ready", ascending=False)

if len(df) > 0:
    for name in df["Name"].unique():
        page_path = f"pages/{name}.py"
        if os.path.exists(page_path):
            d = False
            h = ""
        else:
            d = True
            h = "Coming soon..."
        if st.button(name, width="stretch", disabled=d, help=h, type="primary"):
            st.switch_page(f"pages/{name}.py")

else:
    st.write("No questionnaire matches your filters.")
