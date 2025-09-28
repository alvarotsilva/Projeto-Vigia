from __future__ import annotations
import streamlit as st
import pandas as pd
from projeto_vigia.theming import setup_page, inject_css
from projeto_vigia.config import FILE_URL, LOGO_URL
from projeto_vigia.services.data_io import read_csv_from_gdrive
from projeto_vigia.domain.preprocessing import normalize_dataframe
from projeto_vigia.analytics.filters import (
    filter_by_date_range, filter_by_turno, filter_by_biomes, filter_numeric_columns
)
from projeto_vigia.analytics.aggregations import (
    by_day, by_biome, top_municipios, series_by_dimension, compute_critical_regions
)
from projeto_vigia.ui.sidebar import render_sidebar
from projeto_vigia.ui.sections import (
    render_summary_tab, render_time_tab, render_biome_city_tab,
    render_prevention_tab, render_stats_tab
)

setup_page()
inject_css()

st.title("🔥 Painel de Análise de Queimadas no Brasil")
st.markdown("Este painel realiza uma análise interativa de focos de queimadas com base em um arquivo de dados da web.")

@st.cache_data(ttl=86400, show_spinner="Baixando e processando dados CSV...")
def load_dataset(url: str) -> pd.DataFrame:
    df = read_csv_from_gdrive(url)
    return normalize_dataframe(df)

try:
    df_full = load_dataset(FILE_URL)
except Exception as e:
    df_full = pd.DataFrame()
    st.error(f"Falha ao carregar dados: {e}")

sidebar_state = render_sidebar(df_full, LOGO_URL)

if df_full.empty:
    st.warning("Os dados não puderam ser carregados. Verifique o link/permissões.")
elif sidebar_state and sidebar_state["buscar"]:
    estado = sidebar_state["estado"]
    biomas = sidebar_state["biomas"]
    start_dt = sidebar_state["start"]
    end_dt = sidebar_state["end"]
    turno_preset = sidebar_state["turno_preset"]
    custom_time = sidebar_state["custom_time"]
    numeric_rules = sidebar_state["numeric_rules"]

    # Estado
    dff = df_full if estado == "Todos" else df_full[df_full["estado_nome"] == estado].copy()
    # Período
    dff = filter_by_date_range(dff, start_dt, end_dt)
    # Bioma(s)
    dff = filter_by_biomes(dff, biomas)
    # Turno
    dff = filter_by_turno(dff, preset=turno_preset, custom_range=custom_time)
    # Regras numéricas
    dff = filter_numeric_columns(dff, numeric_rules)

    if dff.empty:
        st.warning("Nenhum foco de queimada foi encontrado para os filtros selecionados.")
    else:
        # Regiões críticas (box na tela principal)
        crit = compute_critical_regions(dff, top_n=5)

        st.success(f"Análise concluída para **{estado}** entre **{start_dt:%d/%m/%Y}** e **{end_dt:%d/%m/%Y}**!")
        st.subheader("Regiões Críticas (top 5)")
        st.dataframe(crit[["estado_nome","municipio_nome","Bioma","focos","risco_medio","frp_medio","frp_max","precip_media","dias_sem_chuva_med"]])

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🗺️ Mapa e Métricas",
            "📈 Séries Temporais",
            "🌳 Bioma & Município",
            "📊 Estatística",
            "💡 Prevenção",
        ])

        with tab1:
            render_summary_tab(dff, estado)
        with tab2:
            render_time_tab(
                by_day(dff),
                series_by_dimension(dff, "estado_nome"),
                series_by_dimension(dff, "Bioma"),
            )
        with tab3:
            render_biome_city_tab(by_biome(dff), top_municipios(dff))
        with tab4:
            render_stats_tab(dff)
        with tab5:
            render_prevention_tab()

        with st.expander("Ver dados brutos (todas as colunas)"):
            df_disp = dff.rename(columns={"lat":"Latitude","lon":"Longitude","data_hora":"Data/Hora",
                                          "municipio_nome":"Município","estado_nome":"Estado"})
            st.dataframe(df_disp)
else:
    st.info("⬅️ Selecione os filtros na barra lateral e clique em **Analisar** para começar.")
