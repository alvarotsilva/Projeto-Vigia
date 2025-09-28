from __future__ import annotations
import streamlit as st
import pandas as pd
from ..charts.time_series import time_chart
from ..charts.bar_charts import bioma_chart, municipio_chart
from ..charts.maps import simple_map

def render_summary_tab(df: pd.DataFrame, estado: str):
    st.subheader(f"Resumo para {estado}")
    total = len(df)
    municipio_top = df["municipio_nome"].value_counts().idxmax()
    n_muns = df["municipio_nome"].nunique()
    avg_sem_chuva = df["DiaSemChuva"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de Focos no Período", f"{total} 🔥")
    c2.metric("Município com Mais Focos", municipio_top)
    c3.metric("Nº de Municípios Afetados", n_muns)
    c4.metric("Média de Dias Sem Chuva", f"{avg_sem_chuva:.1f} dias" if pd.notna(avg_sem_chuva) else "N/A")

    st.subheader("Mapa de Distribuição dos Focos")
    simple_map(df)

def render_time_tab(focos_por_dia: pd.DataFrame):
    st.subheader("Focos de Queimada ao Longo do Tempo")
    st.altair_chart(time_chart(focos_por_dia), use_container_width=True)

def render_biome_city_tab(df_bioma: pd.DataFrame, df_mun: pd.DataFrame):
    st.subheader("Distribuição de Focos por Bioma")
    st.altair_chart(bioma_chart(df_bioma), use_container_width=True)

    st.subheader("Top 10 Municípios com Mais Focos")
    st.altair_chart(municipio_chart(df_mun), use_container_width=True)

def render_prevention_tab():
    st.subheader("Como Prevenir Queimadas")
    st.markdown("""
    - **🚭 Não jogue bitucas de cigarro** em áreas de vegetação.
    - **🗑️ Não queime lixo**; é ilegal e perigoso.
    - **🏕️ Fogueiras com cuidado** e apague totalmente ao sair.
    - **🎈 Não solte balões** (crime e risco grave).
    - **🏡 Faça aceiro e mantenha terreno limpo**.
    - **📞 Ao avistar foco, ligue 193 (Bombeiros) ou 199 (Defesa Civil)**.
    """)
