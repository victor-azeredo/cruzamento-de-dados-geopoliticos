# 🗺️ Cruzador de Dados Geopolíticos (TSE x IBGE)

## 📖 Sobre o Projeto
Projeto desenvolvido em Python para o cruzamento espacial e higienização de bancos de dados públicos (TSE e IBGE). O objetivo principal é realizar análises geopolíticas, associando locais de votação (zonas e seções eleitorais) aos seus respectivos bairros através de coordenadas geográficas.

Essa estruturação permite realizar recortes municipais precisos, facilitando estudos sociodemográficos aprofundados e a compreensão da distribuição do eleitorado no território.

## 🚀 Funcionalidades
- **Leitura e Higienização de Dados:** Processamento de bases de dados massivas do TSE (CSV) e malhas territoriais do IBGE (Shapefile), com tratamento automático de valores nulos e coordenadas inválidas.
- **Filtro Customizado:** Seleção inteligente de municípios-alvo (ex: Rio de Janeiro, Campos dos Goytacazes e Niterói) através dos códigos oficiais.
- **Geoprocessamento (Spatial Join):** Cruzamento espacial que verifica se a coordenada (latitude/longitude) de uma seção eleitoral está contida dentro do polígono geográfico de um bairro específico.
- **Exportação Otimizada:** Geração de dois catálogos em formato CSV (Mapeamento de Seções e Catálogo de Bairros), prontos para serem consumidos por softwares de BI ou bancos de dados.

## 🛠️ Tecnologias Utilizadas
* **[Python 3.8+](https://www.python.org/)** - Linguagem principal do projeto.
* **[Pandas](https://pandas.pydata.org/)** - Estruturação, limpeza e manipulação tabular dos dados eleitorais.
* **[GeoPandas](https://geopandas.org/)** - Manipulação de dados geoespaciais e execução da junção espacial (Spatial Join).

## ⚙️ Pré-requisitos
Antes de começar, você precisará ter instalado em sua máquina:
* [Python 3.8+](https://www.python.org/downloads/)
* Os arquivos de dados brutos (`.csv` do TSE e `.shp` do IBGE).

## 📦 Instalação

**1. Clone o repositório:**
```bash
git clone [https://github.com/victor-azeredo/cruzamento-de-dados-geopoliticos.git](https://github.com/victor-azeredo/cruzamento-de-dados-geopoliticos.git)
cd cruzamento-de-dados-geopoliticos
```

**2. Instale as dependências necessárias:**
Com o seu ambiente virtual (venv) ativado, instale as bibliotecas listadas no projeto executando:
```bash
pip install -r requirements.txt
```
## 🚀 Como Executar
Com as dependências instaladas e os arquivos brutos posicionados nas pastas `TSE` e `IBGE`:

1. Abra o seu terminal.
2. Navegue até a pasta do código fonte:
```bash
cd CODIGO_FONTE
```
3. Execute o script:
```bash
python main.py
```
O sistema informará o progresso de leitura, as perdas durante a higienização de coordenadas e, ao final, salvará os arquivos consolidados nas pastas de resultado.
