🔥 Painel de Análise de Queimadas no Brasil
Este é um painel interativo desenvolvido com Streamlit para visualizar e analisar dados de focos de queimadas no Brasil. A aplicação carrega os dados de um arquivo CSV hospedado online, oferece filtros dinâmicos e apresenta as informações em múltiplos formatos, incluindo mapas, gráficos e métricas resumidas.

✨ Recursos
Painel Interativo: Interface web amigável e reativa para explorar os dados.

Tema Escuro Personalizado: Um tema visualmente agradável com um logotipo personalizado e uma paleta de cores coesa.

Filtros Dinâmicos: Filtre os focos de queimadas por Estado e por um intervalo de datas específico.

Análise Multidimensional: Os dados são apresentados em quatro abas principais:

🗺️ Mapa e Métricas: Um mapa interativo com a geolocalização dos focos e cartões com estatísticas principais (total de focos, município mais afetado, etc.).

📈 Análise Temporal: Gráfico de linhas que mostra a evolução diária dos focos de queimada no período selecionado.

🌳 Análise por Bioma e Município: Gráficos de barras que detalham a distribuição dos focos por bioma e listam os 10 municípios mais afetados.

💡 Prevenção: Uma seção informativa com dicas práticas sobre como evitar incêndios florestais.

Visualização de Dados Brutos: Uma seção expansível para visualizar a tabela de dados completa que está sendo analisada.

🚀 Como Executar
Para executar este projeto localmente, siga os passos abaixo:

Clone o Repositório (ou baixe os arquivos)

Baixe o arquivo analise_queimadas_brasil.py.

Crie um Ambiente Virtual (Recomendado)

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

Instale as Dependências

Crie um arquivo requirements.txt com o conteúdo abaixo e execute pip install -r requirements.txt.

streamlit
pandas
altair
requests
Pillow

Execute a Aplicação

No seu terminal, navegue até a pasta onde o arquivo .py está salvo e execute o seguinte comando:

streamlit run analise_queimadas_brasil.py

O seu navegador abrirá automaticamente com o painel em execução.

📊 Fonte de Dados
O painel carrega os dados de um arquivo CSV hospedado em um link público do Google Drive. A função de carregamento é projetada para lidar com a confirmação de download do Google, garantindo um acesso mais estável aos dados.

O logotipo também é carregado a partir de um link da web.

🎨 Personalização
Tema e Cores: O estilo visual (cores, fundo, etc.) é definido usando CSS customizado no início do script. Você pode alterar os códigos hexadecimais para criar um novo tema.

Logotipo e Fonte de Dados: As URLs do logotipo e do arquivo CSV são definidas como constantes no início do script (LOGO_URL e FILE_URL). Você pode substituí-las para usar suas próprias fontes.
