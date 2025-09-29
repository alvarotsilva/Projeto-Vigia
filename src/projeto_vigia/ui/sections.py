from __future__ import annotations
import streamlit as st
import pandas as pd
import altair as alt
from ..charts.time_series import time_chart_overall, time_chart_by_dimension
from ..charts.bar_charts import bioma_chart as _bioma_chart, municipio_chart as _municipio_chart
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

    st.subheader("Mapa de Distribuição dos Focos (cor=Risco, raio=FRP)")
    simple_map(df)

def render_time_tab(focos_por_dia: pd.DataFrame, df_series_estado: pd.DataFrame, df_series_bioma: pd.DataFrame):
    st.subheader("Séries temporais (dinâmicas)")
    which = st.radio("Visualizar por:", ["Geral","Estado","Bioma"], horizontal=True)
    if which == "Geral":
        st.altair_chart(time_chart_overall(focos_por_dia), use_container_width=True)
    elif which == "Estado":
        st.altair_chart(time_chart_by_dimension(df_series_estado, "estado_nome"), use_container_width=True)
    else:
        st.altair_chart(time_chart_by_dimension(df_series_bioma, "Bioma"), use_container_width=True)

def render_biome_city_tab(df_bioma: pd.DataFrame, df_mun: pd.DataFrame):
    st.subheader("Distribuição de Focos por Bioma")
    st.altair_chart(_bioma_chart(df_bioma), use_container_width=True)

    st.subheader("Top 10 Municípios com Mais Focos")
    st.altair_chart(_municipio_chart(df_mun), use_container_width=True)

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

def render_stats_tab(df: pd.DataFrame):
    st.subheader("Análise Estatística")
    cols_num = ["DiaSemChuva","Precipitacao","RiscoFogo","FRP"]
    df_num = df[cols_num].dropna()

    st.markdown("**Resumo estatístico**")
    st.dataframe(df_num.describe().T)

    st.markdown("**Distribuições** (histograma + densidade)")
    target = st.selectbox("Escolha a variável:", cols_num, index=2)
    chart = (alt.Chart(df_num)
             .transform_density(target, as_=[target, 'density'])
             .mark_area(opacity=0.4)
             .encode(x=alt.X(f"{target}:Q", title=target), y="density:Q"))
    hist = (alt.Chart(df_num)
            .mark_bar(opacity=0.5)
            .encode(x=alt.X(f"{target}:Q", bin=True), y="count()"))
    st.altair_chart(hist + chart, use_container_width=True)

    st.markdown("**Correlação**")
    chosen = st.multiselect("Selecione variáveis para correlação", cols_num, default=cols_num)
    if len(chosen) >= 2:
        corr = df_num[chosen].corr().reset_index().melt("index")
        corr.columns = ["Var1", "Var2", "corr"]
        heat = (alt.Chart(corr)
                .mark_rect()
                .encode(
                    x="Var1:O", y="Var2:O",
                    color=alt.Color("corr:Q", scale=alt.Scale(scheme="redyellowblue", domain=(-1,1))),
                    tooltip=["Var1","Var2","corr"]
                ).properties(height=300))
        st.altair_chart(heat, use_container_width=True)
    else:
        st.info("Selecione pelo menos duas variáveis.")
