# Introdução à Ciência de Dados

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-green.svg)](https://pandas.pydata.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este repositório contém os materiais e exercícios do curso de Introdução à Ciência de Dados, incluindo análises de dados, machine learning, visualização e processamento de linguagem natural. O projeto foi reorganizado para facilitar o acesso, manutenção e entendimento dos arquivos e scripts.

## 📋 Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Como Usar](#como-usar)
- [Dependências](#dependências)
- [Exemplos de Uso](#exemplos-de-uso)
- [Contribuição](#contribuição)

## 📁 Estrutura do Projeto

```
introducao_data_science/
│
├── data/                    # Dados organizados por tipo
│   ├── raw/                # Dados brutos (csv, txt, pdf, sqlite, etc)
│   │   ├── california_housing_train.csv
│   │   ├── Iris.csv
│   │   ├── machado_de_assis.txt
│   │   ├── database.sqlite
│   │   ├── TSLA.csv
│   │   ├── APPLE_iPhone_SE.csv
│   │   ├── mcu dataset.csv
│   │   ├── db-ranking.csv
│   │   ├── linguagens.csv
│   │   ├── Cronicas de gelo e fogo.pdf
│   │   └── j.k._rowling_-_1_-_harry_potter_e_a_pedra_filosofal.pdf
│   ├── processed/          # Dados tratados ou intermediários
│   └── external/           # Dados externos ou de referência
│
├── notebooks/              # Jupyter notebooks para análises e experimentos
│   ├── semana_3/           # Subpasta de exercícios ou temas específicos
│   ├── exercicio_3_analise_dados.ipynb
│   ├── exercicio_3_analise_dados_gabarito.ipynb
│   ├── exercicio_5_manipulacao_dados.ipynb
│   └── exercicio_5_manipulacao_dados_gabarito.ipynb
│
├── src/                    # Scripts Python organizados por tema
│   ├── data_analysis/      # Análise de dados
│   │   ├── carregamento_dados.py
│   │   ├── exercicio_3_analise_dados.py
│   │   ├── exercicio_4_analise_basica.py
│   │   ├── exercicio_5_manipulacao_dados.py
│   │   ├── introducao_python.py
│   │   ├── manipulacao_numpy.py
│   │   └── manipulacao_pandas.py
│   ├── big_data/           # Scripts e apps de big data
│   │   ├── analisador_personagens.py
│   │   ├── analise_livros/
│   │   │   └── analise_livros/
│   │   │       ├── analise_livro.py
│   │   │       ├── dom_casmurro.pdf
│   │   │       └── requirements_local.txt
│   │   ├── app_analise_personagens/
│   │   │   └── app_analise_personagens/
│   │   │       ├── analisador_personagens_st.py
│   │   │       ├── app.py
│   │   │       └── requirements.txt
│   │   ├── app.py
│   │   ├── big_data_tecnicas.py
│   │   ├── big_data.py
│   │   └── README.md
│   ├── ml/                 # Machine Learning
│   │   ├── algoritmo_classificacao.py
│   │   ├── exemplo_classificacao.py
│   │   ├── introducao_ml.py
│   │   └── modelo_predicao.py
│   ├── visualization/      # Visualização de dados
│   │   └── data_viz.py
│   └── web_scraping/       # Web scraping
│       └── web_scraping.py
│
├── results/                # Resultados de análises
│   └── figures/            # Gráficos e imagens gerados
│       ├── analise_de_residuos_*.png
│       ├── previsoes_vs_reais_*.png
│       ├── correlation_heatmap.png
│       ├── scatter_income_vs_value.png
│       ├── grafico_*.png
│       ├── personagens_*.png
│       ├── demo_*.png
│       ├── analise_sentimento_machado.png
│       ├── rede_personagens.png
│       └── Money.png
│
├── requirements/           # Arquivos de dependências
│   └── requirements.txt
│
├── lib/                    # Bibliotecas externas
│   ├── bindings/
│   │   └── utils.js
│   ├── tom-select/
│   │   ├── tom-select.complete.min.js
│   │   └── tom-select.css
│   └── vis-9.1.2/
│       ├── vis-network.css
│       └── vis-network.min.js
│
├── scripts/                # Scripts organizados por funcionalidade (legado)
│   ├── analise_dados/
│   ├── big_data/
│   ├── machine_learning/
│   ├── visualizacao/
│   └── web_scraping/
│
├── docs/                   # Documentação e README antigo
│   └── README.md
│
├── dados/                  # Pasta legada com datasets
├── resultados/             # Pasta legada com resultados
├── introducao_data_science/ # Pasta legada
├── grid.edgelist           # Arquivo de rede
├── rede_relacionamentos.html # Visualização de rede
└── README.md               # Este arquivo
```

## 🚀 Funcionalidades

### 📊 Análise de Dados
- **Manipulação com Pandas**: Operações básicas e avançadas
- **Análises estatísticas**: Correlações, distribuições, outliers
- **Processamento de dados**: Limpeza, transformação, agregação
- **Carregamento de dados**: CSV, SQLite, TXT, PDF

### 🤖 Machine Learning
- **Algoritmos de classificação**: KNN, Decision Trees, Random Forest
- **Algoritmos de regressão**: Linear Regression
- **Avaliação de modelos**: Métricas de performance, análise de resíduos
- **Predição de preços**: Modelo para preços de casas da Califórnia

### 📈 Visualização
- **Gráficos estatísticos**: Histogramas, boxplots, scatter plots
- **Dashboards interativos**: Gráficos combinados e personalizados
- **Análises visuais**: Mapas de calor, correlações, distribuições
- **Redes de relacionamentos**: Visualização de grafos

### 🌐 Web Scraping
- **Coleta de dados**: BeautifulSoup, Requests, Selenium
- **APIs**: Integração com APIs públicas
- **Processamento**: Limpeza e estruturação de dados web

### 📝 Processamento de Linguagem Natural (NLP)
- **Análise de sentimento**: VADER para análise de sentimentos
- **Identificação de nomes próprios**: NLTK e técnicas customizadas
- **Processamento de texto**: Tokenização, contagem de palavras
- **Análise de textos literários**: Machado de Assis, Crônicas de Gelo e Fogo
- **Aplicação Streamlit**: Interface web para análise de personagens

## 🛠️ Como Usar

### Pré-requisitos
- Python 3.8 ou superior
- Git

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/introducao_data_science.git
   cd introducao_data_science
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv
   
   # Ative o ambiente virtual:
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements/requirements.txt
   ```

### Executando os Scripts

```bash
# Análise de dados
python src/data_analysis/exercicio_3_analise_dados.py
python src/data_analysis/exercicio_5_manipulacao_dados.py

# Visualização
python src/visualization/data_viz.py

# Machine Learning
python src/ml/modelo_predicao.py
python src/ml/algoritmo_classificacao.py

# Big Data / NLP
python src/big_data/big_data.py
python src/big_data/analisador_personagens.py

# Web Scraping
python src/web_scraping/web_scraping.py

# Aplicação Streamlit
cd src/big_data/app_analise_personagens/app_analise_personagens
streamlit run app.py
```

## 📦 Dependências Principais

| Biblioteca | Versão | Descrição |
|------------|--------|-----------|
| **Python** | 3.8+ | Linguagem principal |
| **pandas** | 1.3+ | Manipulação de dados |
| **numpy** | 1.21+ | Computação numérica |
| **matplotlib** | 3.4+ | Visualização básica |
| **seaborn** | 0.11+ | Visualização estatística |
| **scikit-learn** | 1.0+ | Machine Learning |
| **nltk** | 3.6+ | Processamento de linguagem natural |
| **beautifulsoup4** | 4.9+ | Web scraping |
| **requests** | 2.25+ | Requisições HTTP |
| **jupyter** | 1.0+ | Notebooks interativos |
| **streamlit** | 1.0+ | Aplicações web |
| **plotly** | 5.0+ | Gráficos interativos |
| **networkx** | 2.6+ | Análise de redes |

## 📊 Exemplos de Uso

### Análise de Sentimento
```python
# Exemplo de análise de sentimento do texto do Machado de Assis
python src/big_data/big_data.py
```

### Visualização de Dados
```python
# Criação de gráficos diversos
python src/visualization/data_viz.py
```

### Machine Learning
```python
# Predição de preços de casas
python src/ml/modelo_predicao.py
```

### Aplicação Web
```bash
# Interface web para análise de personagens
cd src/big_data/app_analise_personagens/app_analise_personagens
streamlit run app.py
```

## 🎯 Objetivos do Projeto

- ✅ Aprender fundamentos de manipulação de dados com Python
- ✅ Praticar visualização de dados com diferentes bibliotecas
- ✅ Explorar técnicas de análise exploratória de dados
- ✅ Implementar modelos básicos de machine learning
- ✅ Trabalhar com dados reais do Kaggle
- ✅ Introduzir conceitos de processamento de linguagem natural
- ✅ Desenvolver habilidades de web scraping
- ✅ Criar aplicações web interativas com Streamlit

## 📚 Conteúdo Detalhado

### 1. Manipulação de Dados
- **carregamento_dados.py**: Diferentes formas de carregar dados
- **manipulacao_pandas.py**: Operações avançadas com Pandas
- **manipulacao_numpy.py**: Computação numérica eficiente
- **exercicio_3_analise_dados.py**: Análise exploratória completa
- **exercicio_5_manipulacao_dados.py**: Manipulação e transformação

### 2. Visualização de Dados
- **data_viz.py**: Exemplos completos com Matplotlib e Seaborn
- Gráficos de dispersão, barras, linhas e funções matemáticas
- Personalização avançada de visualizações
- Gráficos de progresso e interativos
- Visualização de redes de relacionamentos

### 3. Machine Learning
- **introducao_ml.py**: Conceitos fundamentais de ML
- **algoritmo_classificacao.py**: Implementação de classificadores
- **modelo_predicao.py**: Predição de preços de casas
- **exemplo_classificacao.py**: Exemplos práticos de classificação

### 4. Big Data e NLP
- **big_data.py**: Análise de sentimento e nomes próprios
- **analisador_personagens.py**: Análise avançada de personagens
- **big_data_tecnicas.py**: Técnicas de processamento de big data
- Processamento de texto do Machado de Assis
- Identificação de entidades nomeadas
- Análise de frequência de palavras
- Aplicação Streamlit para análise interativa

### 5. Web Scraping
- **web_scraping.py**: Coleta de dados da web
- Uso de BeautifulSoup e Requests
- Manipulação de HTML e JSON

## 📁 Recomendações de Uso

- **Use as pastas temáticas em `src/`** para scripts organizados por funcionalidade
- **Salve dados brutos em `data/raw`** e dados processados em `data/processed`
- **Centralize notebooks em `notebooks/`** para análises exploratórias
- **Armazene resultados e gráficos em `results/figures`**
- **Documentação e arquivos de referência** devem ir para `docs/`

## 🤝 Contribuição

Contribuições são muito bem-vindas! Para contribuir:

1. **Fork** o projeto
2. **Crie uma branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra um Pull Request**

### Diretrizes de Contribuição
- Mantenha o código limpo e bem documentado
- Adicione comentários explicativos em português
- Teste seus scripts antes de submeter
- Siga o padrão de nomenclatura existente
- Use a estrutura de pastas recomendada

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📫 Contato

- **Autor**: Rafael Amorim Honorato
- **Email**: rafael.honorato03@gmail.com
- **LinkedIn**: [https://www.linkedin.com/in/rafael-honorato03/]
- **GitHub**: [https://github.com/seu-usuario]

## 🙏 Agradecimentos

- **Kaggle** pela disponibilização dos datasets
- **Comunidade Python** e **Data Science** pelo suporte
- **Todos os contribuidores** do projeto
- **[Thaisandre](https://dev.to/thaisandre)** pelo excelente artigo sobre NLTK e Processamento de Linguagem Natural, que serviu como referência fundamental para a implementação da análise de nomes próprios e processamento de texto neste projeto. O artigo pode ser encontrado em: [NLTK e Processamento de Linguagem Natural](https://dev.to/thaisandre/nltk-e-processamento-de-linguagem-natural-3l49)

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no repositório!** 