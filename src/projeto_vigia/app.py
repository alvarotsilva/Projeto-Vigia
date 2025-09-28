from __future__ import annotations
import streamlit as st
import pandas as pd
from projeto_vigia.theming import setup_page, inject_css
from projeto_vigia.config import FILE_URL, LOGO_URL
from projeto_vigia.services.data_io import read_csv_from_gdrive
from projeto_vigia.domain.preprocessing import normalize_dataframe
from projeto_vigia.analytics.filters import filter_by_state_and_date
from projeto_vigia.analytics.aggregations import by_day, by_biome, top_municipios
from projeto_vigia.ui.sidebar import render_sidebar
from projeto_vigia.ui.sections import (
    render_summary_tab, render_time_tab, render_biome_city_tab, render_prevention_tab
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
    start_dt = sidebar_state["start_date"]
    end_dt = sidebar_state["end_date"]

    df_focos = filter_by_state_and_date(df_full, estado, start_dt, end_dt)
    if df_focos.empty:
        st.warning("Nenhum foco de queimada foi encontrado para os filtros selecionados.")
    else:
        st.success(f"Análise concluída para **{estado}** entre **{start_dt:%d/%m/%Y}** e **{end_dt:%d/%m/%Y}**!")
        tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Mapa e Métricas", "📈 Análise Temporal", "🌳 Bioma & Município", "💡 Prevenção"])

        with tab1: render_summary_tab(df_focos, estado)
        with tab2: render_time_tab(by_day(df_focos))
        with tab3: render_biome_city_tab(by_biome(df_focos), top_municipios(df_focos))
        with tab4: render_prevention_tab()

        with st.expander("Ver dados brutos (todas as colunas)"):
            df_disp = df_focos.rename(columns={"lat":"Latitude","lon":"Longitude","data_hora":"Data/Hora",
                                               "municipio_nome":"Município","estado_nome":"Estado"})
            st.dataframe(df_disp)
else:
    st.info("⬅️ Selecione os filtros na barra lateral e clique em **Analisar** para começar.")
