import streamlit as st
import pandas as pd
import openpyxl
import altair as alt
import pandas as pd

from scripts import ueqs as ueq
from scripts import utils as ut

st.set_page_config("About", initial_sidebar_state="collapsed")

if st.button("Home", icon=":material/arrow_back:", type="tertiary"):
        st.switch_page("Home.py")
        
st.title("About")

with open("README.md", "r", encoding="utf-8") as f:
    md_text = f.read()
    # Display it in Streamlit
    st.markdown(md_text)