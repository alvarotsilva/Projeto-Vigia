# 🔥 Painel de Análise de Queimadas no Brasil

Este é um painel interativo desenvolvido com **Streamlit** para visualizar e analisar dados de focos de queimadas no Brasil.  
A aplicação carrega os dados de satélite (NOAA/INPE), oferece filtros dinâmicos e apresenta as informações em múltiplos formatos, incluindo mapas, gráficos e métricas resumidas.

---

## ✨ Recursos

- **Painel Interativo**: Interface web amigável e reativa para explorar os dados.  
- **Tema Escuro Personalizado**: Um tema visualmente agradável com logotipo e paleta de cores coesa.  
- **Filtros Dinâmicos**: Filtre os focos de queimadas por Estado e intervalo de datas.  
- **Análise Multidimensional**:  
  - 🗺️ **Mapa e Métricas**: geolocalização dos focos e estatísticas principais.  
  - 📈 **Análise Temporal**: evolução diária dos focos.  
  - 🌳 **Análise por Bioma e Município**: distribuição dos focos por bioma e municípios mais afetados.  
  - 💡 **Prevenção**: dicas práticas de combate e prevenção de incêndios.  
- **Visualização de Dados Brutos**: seção expansível com toda a tabela analisada.

---

## 📊 Fonte de Dados

Os dados vêm do **NOAA/INPE**, obtidos por satélites de monitoramento (ex.: GOES-19).  
Cada linha do arquivo CSV representa **um foco de calor detectado em coordenadas específicas**, com atributos ambientais associados.

* O arquivo CSV está hospedado em um link público do Google Drive. A função de carregamento é projetada para lidar com a confirmação de download do Google, garantindo um acesso mais estável aos dados.

### O que cada coluna representa

- **DataHora** → instante em que o satélite detectou o foco de calor (data + hora UTC).  
- **Satelite** → qual satélite fez a observação (aqui: GOES-19).  
- **Pais / Estado / Municipio** → localização administrativa associada às coordenadas.  
- **Bioma** → bioma onde o foco ocorreu (Caatinga, Cerrado, Mata Atlântica).  
- **DiaSemChuva** → número de dias consecutivos sem registro de chuva. `-999` = valor faltante.  
- **Precipitacao** → precipitação acumulada (mm) no dia da observação.  
- **RiscoFogo** → índice adimensional (0–1), quanto mais próximo de 1, maior o risco.  
- **Latitude / Longitude** → coordenadas geográficas do foco.  
- **FRP (Fire Radiative Power)** → potência radiativa do fogo, em MW, relacionada à intensidade do incêndio.

---

## 🔎 O que podemos analisar a partir da base

- **Distribuição temporal**  
  - Registros entre **07/04/2025 e 10/04/2025**.  
  - Detecções em horários diurnos e noturnos (alta frequência do GOES-19).  

- **Distribuição espacial**  
  - Estados mais recorrentes: **Bahia (Caatinga)** e **Minas Gerais (Cerrado)**.  
  - Outros registros: Mato Grosso do Sul, Piauí, Pernambuco, Maranhão, Paraíba.  

- **Biomas**  
  - Presentes: **Caatinga, Cerrado e Mata Atlântica**.  
  - Destaque para a Caatinga na Bahia (Ibicoara, Itaguaçu da Bahia, Mortugaba).  

- **Condições climáticas associadas**  
  - Dias sem chuva: 0 a 16.  
  - Precipitação: geralmente 0 → ambiente seco. Casos pontuais com chuva > 1 mm.  

- **Risco de fogo**  
  - Maioria com valores altos (0.8–1.0).  
  - Casos com risco menor (0.18–0.65) também detectados.  

- **Intensidade (FRP)**  
  - Varia entre ~62 MW e 285 MW.  
  - Mais altos (ex.: Ibicoara/BA) indicam incêndios intensos.  

- **Duplicidade / Revisita**  
  - Mesma região pode aparecer em horários próximos (ex.: Uberaba/MG), indicando revisita do satélite ou detecção múltipla.

---

## 🚀 Como Executar

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd Projeto-Vigia-main
```

### 2. Configurar ambiente com Poetry
```bash
poetry install
```

### 3. Rodar a aplicação
```bash
poetry run streamlit run src/projeto_vigia/app.py
```

O painel abrirá automaticamente no navegador em **http://localhost:8501**.

---

## 🎨 Personalização

- **Tema e cores**: definidos em `theming.py` via CSS customizado.  
- **URLs do logotipo e dados**: configuradas em `config.py` (`LOGO_URL` e `FILE_URL`).  

---

## 📂 Estrutura de Pastas

```
projeto_vigia/
├─ pyproject.toml
├─ src/
│  └─ projeto_vigia/
│     ├─ __init__.py
│     ├─ app.py                      # Streamlit “enxuto”: orquestra
│     ├─ config.py                   # Constantes/URLs/cores
│     ├─ theming.py                  # CSS/tema e set_page_config()
│     ├─ services/                   # Camada de acesso a dados
│     │   ├─ __init__.py
│     │   ├─ drive_fetch.py          # Download seguro do GDrive/HTTP
│     │   └─ data_io.py              # Leitura CSV + validação/normalização
│     ├─ domain/                     # Modelos e pré-processamento
│     │   ├─ __init__.py
│     │   ├─ models.py               # Pydantic BaseModel dos dados
│     │   └─ preprocessing.py        # Limpeza, renome, tipos, etc.
│     ├─ analytics/                  # Filtros e agregações
│     │   ├─ __init__.py
│     │   ├─ filters.py              # Filtragem por estado e janela de data
│     │   └─ aggregations.py         # groupbys (por dia, bioma, município)
│     ├─ charts/                     # Gráficos
│     │   ├─ __init__.py
│     │   ├─ time_series.py          # Altair line
│     │   ├─ bar_charts.py           # Bioma/município
│     │   └─ maps.py                 # st.map / pydeck (se quiser evoluir)
│     └─ ui/                         # Sidebar e seções do painel
│         ├─ __init__.py
│         ├─ sidebar.py              # Selectbox, date inputs, botão “Analisar”
│         └─ sections.py             # Métricas, tabs, expander, prevenção
└─ tests/                            # Testes unitários
   ├─ test_data_io.py                # Não implementado
   ├─ test_filters.py
   └─ test_aggregations.py           # Não implementado
```

---

## ✅ Testes

Testes básicos estão disponíveis em `tests/` para validar filtros, agregações e IO de dados.
