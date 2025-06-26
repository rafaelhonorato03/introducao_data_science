# Introdução à Ciência de Dados

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-green.svg)](https://pandas.pydata.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este repositório contém os materiais e exercícios do curso de Introdução à Ciência de Dados, incluindo análises de dados, machine learning, visualização e processamento de linguagem natural.

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
├── dados/                  # Datasets e arquivos de dados
│   ├── california_housing_train.csv
│   ├── database.sqlite
│   ├── Iris.csv
│   ├── machado_de_assis.txt
│   └── outros_datasets.csv
├── notebooks/             # Jupyter notebooks com exercícios
│   ├── semana_3/
│   ├── exercicio_3_analise_dados.ipynb
│   └── exercicio_5_manipulacao_dados.ipynb
├── scripts/              # Scripts Python organizados por funcionalidade
│   ├── analise_dados/    # Análise exploratória de dados
│   ├── big_data/         # Processamento de linguagem natural
│   ├── machine_learning/ # Algoritmos de ML
│   ├── visualizacao/     # Gráficos e visualizações
│   └── web_scraping/     # Coleta de dados da web
├── resultados/           # Resultados de análises
│   └── graficos/         # Imagens geradas pelos scripts
└── requirements.txt      # Dependências do projeto
```

## 🚀 Funcionalidades

### 📊 Análise de Dados
- **Manipulação com Pandas**: Operações básicas e avançadas
- **Análises estatísticas**: Correlações, distribuições, outliers
- **Processamento de dados**: Limpeza, transformação, agregação

### 🤖 Machine Learning
- **Algoritmos de classificação**: KNN, Decision Trees, SVM
- **Algoritmos de regressão**: Linear Regression, Random Forest
- **Avaliação de modelos**: Métricas de performance, validação cruzada

### 📈 Visualização
- **Gráficos estatísticos**: Histogramas, boxplots, scatter plots
- **Dashboards interativos**: Gráficos combinados e personalizados
- **Análises visuais**: Mapas de calor, correlações, distribuições

### 🌐 Web Scraping
- **Coleta de dados**: BeautifulSoup, Requests, Selenium
- **APIs**: Integração com APIs públicas
- **Processamento**: Limpeza e estruturação de dados web

### 📝 Processamento de Linguagem Natural (NLP)
- **Análise de sentimento**: VADER para análise de sentimentos
- **Identificação de nomes próprios**: NLTK e técnicas customizadas
- **Processamento de texto**: Tokenização, contagem de palavras
- **Análise de textos literários**: Machado de Assis como exemplo

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
   pip install -r requirements.txt
   ```

### Executando os Scripts

```bash
# Análise de dados
python scripts/analise_dados/exercicio_3_analise_dados.py

# Visualização
python scripts/visualizacao/data_viz.py

# Machine Learning
python scripts/machine_learning/modelo_predicao.py

# Big Data / NLP
python scripts/big_data/big_data.py

# Web Scraping
python scripts/web_scraping/web_scraping.py
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

## 📊 Exemplos de Uso

### Análise de Sentimento
```python
# Exemplo de análise de sentimento do texto do Machado de Assis
python scripts/big_data/big_data.py
```

### Visualização de Dados
```python
# Criação de gráficos diversos
python scripts/visualizacao/data_viz.py
```

### Machine Learning
```python
# Predição de preços de casas
python scripts/machine_learning/modelo_predicao.py
```

## 🎯 Objetivos do Projeto

- ✅ Aprender fundamentos de manipulação de dados com Python
- ✅ Praticar visualização de dados com diferentes bibliotecas
- ✅ Explorar técnicas de análise exploratória de dados
- ✅ Implementar modelos básicos de machine learning
- ✅ Trabalhar com dados reais do Kaggle
- ✅ Introduzir conceitos de processamento de linguagem natural
- ✅ Desenvolver habilidades de web scraping

## 📚 Conteúdo Detalhado

### 1. Manipulação de Dados
- **carregamento_dados.py**: Diferentes formas de carregar dados
- **manipulacao_pandas.py**: Operações avançadas com Pandas
- **manipulacao_numpy.py**: Computação numérica eficiente

### 2. Visualização de Dados
- **data_viz.py**: Exemplos completos com Matplotlib e Seaborn
- Gráficos de dispersão, barras, linhas e funções matemáticas
- Personalização avançada de visualizações
- Gráficos de progresso e interativos

### 3. Machine Learning
- **introducao_ml.py**: Conceitos fundamentais de ML
- **algoritmo_classificacao.py**: Implementação de classificadores
- **modelo_predicao.py**: Predição de preços de casas

### 4. Big Data e NLP
- **big_data.py**: Análise de sentimento e nomes próprios
- Processamento de texto do Machado de Assis
- Identificação de entidades nomeadas
- Análise de frequência de palavras

### 5. Web Scraping
- **web_scraping.py**: Coleta de dados da web
- Uso de BeautifulSoup e Requests
- Manipulação de HTML e JSON

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

