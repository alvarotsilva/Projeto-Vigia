import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="Análise de Queimadas no Brasil",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def inject_css():
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] { background-color: #1a1a1a; }
      [data-testid="stSidebar"] { background-color: #262730; }
      h1, h2, h3 { color: #f0f2f6; }
      .st-emotion-cache-16txtl3 { color: #d1d1d1; }
      .st-emotion-cache-10trblm { color: #ff6347; }
      .stButton>button {
        border: 2px solid #ff6347; background: transparent; color: #ff6347; border-radius: 8px;
      }
      .stButton>button:hover { border-color: #e5533d; color: #e5533d; }
      .stButton>button:active { background-color: #e5533d; color: white; }
    </style>
    """, unsafe_allow_html=True)
