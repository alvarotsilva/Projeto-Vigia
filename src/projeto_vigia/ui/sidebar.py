from __future__ import annotations
import streamlit as st
import pandas as pd
from PIL import Image
import requests
import io

def load_logo(url: str) -> Image.Image | None:
    try:
        r = requests.get(url, stream=True, timeout=20)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content))
    except Exception:
        return None

def render_sidebar(df_full: pd.DataFrame | None, logo_url: str):
    if (logo := load_logo(logo_url)):
        st.sidebar.image(logo)
    else:
        st.sidebar.warning("Não foi possível carregar o logotipo.")

    st.sidebar.header("Filtros de Análise")
    if df_full is None or df_full.empty:
        st.sidebar.selectbox("Selecione um Estado", ["Dados não carregados"], disabled=True)
        st.sidebar.date_input("Data de Início", disabled=True)
        st.sidebar.date_input("Data de Fim", disabled=True)
        return None

    estados = ["Todos"] + sorted(df_full["estado_nome"].unique().tolist())
    estado = st.sidebar.selectbox("Selecione um Estado", estados)

    min_date = df_full["data_hora"].min().date()
    max_date = df_full["data_hora"].max().date()
    d0 = st.sidebar.date_input("Data de Início", value=min_date, min_value=min_date, max_value=max_date)
    d1 = st.sidebar.date_input("Data de Fim", value=max_date, min_value=d0, max_value=max_date)

    buscar = st.sidebar.button("Analisar", type="primary")
    return {"estado": estado, "start_date": pd.to_datetime(d0), "end_date": pd.to_datetime(d1), "buscar": buscar}
