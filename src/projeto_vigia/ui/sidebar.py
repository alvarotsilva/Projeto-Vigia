from __future__ import annotations
import streamlit as st
import pandas as pd
from PIL import Image
import requests
import io
from typing import Optional, Dict, Any, Tuple

def load_logo(url: str) -> Image.Image | None:
    try:
        r = requests.get(url, stream=True, timeout=20)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content))
    except Exception:
        return None

def _numeric_filter_block(label: str, key_prefix: str) -> Dict[str, Any]:
    cols = st.columns([1.2, 1, 1])
    op = cols[0].selectbox(f"{label} (operador)", ["(sem filtro)","=","<",">","<=" ,">=","entre"], key=f"{key_prefix}_op")
    a = cols[1].number_input("A", value=0.0, step=0.1, key=f"{key_prefix}_a")
    b = cols[2].number_input("B", value=0.0, step=0.1, key=f"{key_prefix}_b")
    return {"op": op, "a": a, "b": b}

def render_sidebar(df_full: pd.DataFrame | None, logo_url: str):
    if (logo := load_logo(logo_url)):
        st.sidebar.image(logo)
    else:
        st.sidebar.warning("Não foi possível carregar o logotipo.")

    st.sidebar.header("Filtros de Análise")

    if df_full is None or df_full.empty:
        st.sidebar.selectbox("Estado", ["Dados não carregados"], disabled=True)
        st.sidebar.date_input("Período", disabled=True)
        return None

    # Estado (com opção Todos)
    estados = ["Todos"] + sorted(df_full["estado_nome"].unique().tolist())
    estado = st.sidebar.selectbox("Estado", estados)

    # Biomas
    biomas_unique = sorted(df_full["Bioma"].dropna().unique().tolist())
    biomas = st.sidebar.multiselect("Biomas", options=biomas_unique, default=[])

    # Date range em 1 campo
    min_date = df_full["data_hora"].min().date()
    max_date = df_full["data_hora"].max().date()
    start_end = st.sidebar.date_input("Período (início – fim)", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(start_end, tuple):
        d0, d1 = start_end
    else:
        d0, d1 = min_date, max_date
    start_ts = pd.to_datetime(d0)
    end_ts = pd.to_datetime(d1)

    # Turno / horário
    st.sidebar.subheader("Turno / Horário")
    turno_preset = st.sidebar.selectbox("Turno", ["(sem filtro)","Madrugada","Manhã","Tarde","Noite"])
    custom_time = st.sidebar.checkbox("Usar faixa de horário personalizada")
    t0, t1 = None, None
    if custom_time:
        c1, c2 = st.sidebar.columns(2)
        t0 = c1.time_input("Início", value=pd.Timestamp("2000-01-01 08:00").time())
        t1 = c2.time_input("Fim", value=pd.Timestamp("2000-01-01 18:00").time())

    # Filtros numéricos
    st.sidebar.subheader("Filtros Numéricos")
    rule_dias = _numeric_filter_block("Dias sem chuva", "dias_sem_chuva")
    rule_prec = _numeric_filter_block("Precipitação (mm)", "precipitacao")
    rule_risco = _numeric_filter_block("Risco de fogo (0–1)", "risco")
    rule_frp = _numeric_filter_block("Intensidade (FRP)", "frp")

    buscar = st.sidebar.button("Analisar", type="primary")

    return {
        "estado": estado,
        "biomas": biomas,
        "start": start_ts,
        "end": end_ts,
        "turno_preset": None if turno_preset == "(sem filtro)" else turno_preset,
        "custom_time": (pd.to_datetime(str(t0)) if t0 else None, pd.to_datetime(str(t1)) if t1 else None) if custom_time else None,
        "numeric_rules": {
            "DiaSemChuva": rule_dias,
            "Precipitacao": rule_prec,
            "RiscoFogo": rule_risco,
            "FRP": rule_frp,
        },
        "buscar": buscar
    }
