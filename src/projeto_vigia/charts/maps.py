import streamlit as st
import pandas as pd

def simple_map(df: pd.DataFrame):
    st.map(df[["lat", "lon"]], zoom=3)
