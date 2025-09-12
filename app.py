import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import requests
import io
from urllib.parse import urlparse, parse_qs
import json
from PIL import Image

# --- Configuração da Página e Tema ---
st.set_page_config(
    page_title="Análise de Queimadas no Brasil",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS customizado para o tema escuro
st.markdown("""
<style>
    /* Cor de fundo principal */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
    }
    /* Cor da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    /* Cor dos títulos principais */
    h1, h2, h3 {
        color: #f0f2f6;
    }
    /* Cor do texto geral */
    .st-emotion-cache-16txtl3 {
        color: #d1d1d1;
    }
    /* Cor dos cabeçalhos das métricas */
    .st-emotion-cache-10trblm {
        color: #ff6347; /* Tomate */
    }
    /* Estilo do botão primário */
    .stButton>button {
        border: 2px solid #ff6347;
        background-color: transparent;
        color: #ff6347;
        border-radius: 8px;
    }
    .stButton>button:hover {
        border-color: #e5533d;
        color: #e5533d;
    }
    .stButton>button:active {
        background-color: #e5533d;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Constantes ---
# Links diretos para os arquivos para evitar erros de permissão do Google Drive
FILE_URL = "https://drive.google.com/uc?export=download&id=1YlThY76iiE6TwU9ZPlBfNkm8FsccjCZm"
LOGO_URL = "https://drive.google.com/uc?export=download&id=1sUYhDEuduVYtF9dBn0CcIRYiMT9qc7o4"
PRIMARY_COLOR = "#ff6347"  # Cor Tomate para os gráficos


# --- Funções Auxiliares ---

@st.cache_data(ttl=86400)
def load_logo_from_url(url):
    """Carrega uma imagem de logotipo a partir de um link da web."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        logo_image = Image.open(io.BytesIO(response.content))
        return logo_image
    except Exception:
        return None


@st.cache_data(ttl=86400)
def load_csv_data(url):
    """
    Carrega e processa dados de queimadas a partir de um link da web (CSV),
    lidando com a confirmação de download do Google Drive.
    """
    try:
        with st.spinner(f"Baixando e processando dados CSV..."):
            session = requests.Session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            file_id = query_params.get('id', [None])[0]

            if not file_id:
                st.error("URL do Google Drive inválida.")
                return pd.DataFrame()

            response = session.get(url, stream=True, headers=headers)
            token = None
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    token = value
                    break

            if token:
                params = {'id': file_id, 'export': 'download', 'confirm': token}
                response = session.get("https://drive.google.com/uc", params=params, stream=True, headers=headers)

            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            # Adicionado 'application/octet-stream' para maior compatibilidade com Google Drive
            if 'text/csv' not in content_type and 'application/vnd.ms-excel' not in content_type and 'application/octet-stream' not in content_type:
                st.error("Erro de Download: O link não retornou um arquivo CSV válido.")
                st.info(f"Tipo de conteúdo recebido: `{content_type}`.")
                st.warning("Verifique o link ou as permissões de compartilhamento.")
                return pd.DataFrame()

            df = pd.read_csv(io.StringIO(response.text))

            rename_map = {'DataHora': 'data_hora', 'Latitude': 'lat', 'Longitude': 'lon', 'Estado': 'estado_nome',
                          'Municipio': 'municipio_nome'}
            essential_cols = ['DataHora', 'Latitude', 'Longitude', 'Estado', 'Municipio', 'Bioma', 'DiaSemChuva',
                              'RiscoFogo']

            if not all(col in df.columns for col in essential_cols):
                st.error(f"O arquivo CSV não contém as colunas essenciais: {', '.join(essential_cols)}")
                return pd.DataFrame()

            df.rename(columns=rename_map, inplace=True)
            df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
            df['DiaSemChuva'] = pd.to_numeric(df['DiaSemChuva'], errors='coerce').replace(-999, pd.NA)
            df['RiscoFogo'] = pd.to_numeric(df['RiscoFogo'], errors='coerce')
            df.dropna(subset=['lat', 'lon', 'data_hora', 'RiscoFogo'], inplace=True)
            return df

    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar dados da URL: {e}")
        return pd.DataFrame()
    except pd.errors.ParserError:
        st.error("Erro de processamento: Não foi possível ler o arquivo como CSV.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
        return pd.DataFrame()


# --- Interface do Usuário (UI) ---

st.title("🔥 Painel de Análise de Queimadas no Brasil")
st.markdown("Este painel realiza uma análise interativa de focos de queimadas com base em um arquivo de dados da web.")

df_full = load_csv_data(FILE_URL)

# --- Barra Lateral ---
logo = load_logo_from_url(LOGO_URL)
if logo:
    st.sidebar.image(logo)
else:
    st.sidebar.warning("Não foi possível carregar o logotipo.")

st.sidebar.header("Filtros de Análise")
is_data_loaded = not df_full.empty

if is_data_loaded:
    lista_estados = ["Todos"] + sorted(df_full['estado_nome'].unique().tolist())
    estado_selecionado_nome = st.sidebar.selectbox("Selecione um Estado", lista_estados)

    min_date = df_full['data_hora'].min().date()
    max_date = df_full['data_hora'].max().date()
    start_date = st.sidebar.date_input('Data de Início', value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input('Data de Fim', value=max_date, min_value=start_date, max_value=max_date)
else:
    estado_selecionado_nome = st.sidebar.selectbox("Selecione um Estado", ["Dados não carregados"], disabled=True)
    st.sidebar.date_input('Data de Início', disabled=True)
    st.sidebar.date_input('Data de Fim', disabled=True)

buscar_dados = st.sidebar.button("Analisar", type="primary", disabled=not is_data_loaded)

# --- Exibição dos Dados ---
if not is_data_loaded:
    st.warning("Os dados não puderam ser carregados. Verifique os erros acima.")
else:
    if buscar_dados:
        if estado_selecionado_nome == "Todos":
            df_focos = df_full.copy()
        else:
            df_focos = df_full[df_full['estado_nome'] == estado_selecionado_nome].copy()

        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date) + pd.Timedelta(days=1)
        mask = (df_focos['data_hora'] >= start_datetime) & (df_focos['data_hora'] < end_datetime)
        df_focos = df_focos.loc[mask]

        if not df_focos.empty:
            st.success(
                f"Análise concluída para **{estado_selecionado_nome}** entre **{start_date.strftime('%d/%m/%Y')}** e **{end_date.strftime('%d/%m/%Y')}**!")

            tab1, tab2, tab3, tab4 = st.tabs(
                ["🗺️ Mapa e Métricas", "📈 Análise Temporal", "🌳 Análise por Bioma e Município", "💡 Prevenção"])

            with tab1:
                st.subheader(f"Resumo para {estado_selecionado_nome}")
                total_focos = len(df_focos)
                municipio_mais_afetado = df_focos['municipio_nome'].value_counts().idxmax()
                total_municipios_afetados = df_focos['municipio_nome'].nunique()
                avg_dias_sem_chuva = df_focos['DiaSemChuva'].mean()

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total de Focos no Período", f"{total_focos} 🔥")
                col2.metric("Município com Mais Focos", municipio_mais_afetado)
                col3.metric("Nº de Municípios Afetados", total_municipios_afetados)
                col4.metric("Média de Dias Sem Chuva",
                            f"{avg_dias_sem_chuva:.1f} dias" if pd.notna(avg_dias_sem_chuva) else "N/A")

                st.subheader("Mapa de Distribuição dos Focos")
                st.map(df_focos[['lat', 'lon']], zoom=3)

            with tab2:
                st.subheader("Focos de Queimada ao Longo do Tempo")
                df_focos['data'] = df_focos['data_hora'].dt.date
                focos_por_dia = df_focos.groupby('data').size().reset_index(name='contagem')
                time_chart = alt.Chart(focos_por_dia).mark_line(point=True, color=PRIMARY_COLOR).encode(
                    x=alt.X('data:T', title='Data'),
                    y=alt.Y('contagem:Q', title='Número de Focos Diários'),
                    tooltip=['data:T', 'contagem:Q']
                ).properties(title='Evolução Diária dos Focos de Queimada').interactive()
                st.altair_chart(time_chart, use_container_width=True)

            with tab3:
                st.subheader("Distribuição de Focos por Bioma")
                focos_por_bioma = df_focos['Bioma'].value_counts().reset_index()
                focos_por_bioma.columns = ['Bioma', 'Número de Focos']
                bioma_chart = alt.Chart(focos_por_bioma).mark_bar().encode(
                    x=alt.X('Número de Focos:Q'),
                    y=alt.Y('Bioma:N', sort='-x'),
                    tooltip=['Bioma', 'Número de Focos'],
                    color=alt.Color('Bioma:N', legend=None, scale=alt.Scale(scheme='redyellowgreen'))
                ).properties(title='Focos de Queimada por Bioma')
                st.altair_chart(bioma_chart, use_container_width=True)

                st.subheader("Top 10 Municípios com Mais Focos")
                focos_por_municipio = df_focos['municipio_nome'].value_counts().nlargest(10).reset_index()
                focos_por_municipio.columns = ['Município', 'Número de Focos']
                municipio_chart = alt.Chart(focos_por_municipio).mark_bar(color=PRIMARY_COLOR).encode(
                    x=alt.X('Número de Focos:Q'),
                    y=alt.Y('Município:N', sort='-x'),
                    tooltip=['Município', 'Número de Focos']
                ).properties(title='Top 10 Municípios com Mais Focos de Queimada')
                st.altair_chart(municipio_chart, use_container_width=True)

            with tab4:
                st.subheader("Como Prevenir Queimadas")
                st.markdown("""
                A prevenção é a forma mais eficaz de combater os incêndios florestais. A maioria deles começa por descuidos humanos. Siga estas dicas:
                - **🚭 Não jogue bitucas de cigarro** pela janela do carro ou em áreas de vegetação.
                - **🗑️ Não queime lixo** em quintais, terrenos ou qualquer área com vegetação. A prática é ilegal e perigosa.
                - **🏕️ Cuidado com fogueiras:** Se precisar acender uma, escolha um local limpo, longe de árvores e vegetação seca. Apague completamente com água e terra antes de sair.
                - **🎈 Não solte balões:** Além de ser crime, balões podem cair em florestas e iniciar grandes incêndios.
                - **🏡 Manutenção de terrenos:** Mantenha seu terreno limpo, criando uma faixa livre de vegetação seca (aceiro) ao redor de sua propriedade.
                - **📞 Avise sobre focos de incêndio:** Se avistar um foco de incêndio, ligue imediatamente para o Corpo de Bombeiros (193) ou para a Defesa Civil (199).
                """)

            with st.expander("Ver dados brutos (todas as colunas do arquivo)"):
                df_display = df_focos.rename(columns={'lat': 'Latitude', 'lon': 'Longitude', 'data_hora': 'Data/Hora',
                                                      'municipio_nome': 'Município', 'estado_nome': 'Estado'})
                st.dataframe(df_display)
        else:
            st.warning("Nenhum foco de queimada foi encontrado para os filtros selecionados.")
    else:
        st.info("⬅️ Selecione os filtros na barra lateral e clique em 'Analisar' para começar.")

