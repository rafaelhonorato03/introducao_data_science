# Introdução à Ciência de Dados

Este repositório contém os materiais e exercícios do curso de Introdução à Ciência de Dados.

## Estrutura do Projeto

```
introducao_data_science/
├── dados/                  # Diretório com datasets
│   ├── california_housing_train.csv
│   ├── database.sqlite
│   └── Iris.csv
├── notebooks/             # Jupyter notebooks com exercícios
│   └── semana_3/
├── scripts/              # Scripts Python organizados por funcionalidade
│   ├── analise_dados/
│   ├── machine_learning/
│   ├── visualizacao/
│   └── web_scraping/
├── resultados/           # Resultados de análises e visualizações
│   └── graficos/
└── requirements.txt      # Dependências do projeto
```

## Organização dos Scripts

### Análise de Dados
- `scripts/analise_dados/`: Scripts relacionados à análise exploratória de dados
  - Manipulação de dados com Pandas
  - Análises estatísticas
  - Processamento de dados

### Machine Learning
- `scripts/machine_learning/`: Scripts de modelos de machine learning
  - Algoritmos de classificação
  - Algoritmos de regressão
  - Avaliação de modelos

### Visualização
- `scripts/visualizacao/`: Scripts para criação de visualizações
  - Gráficos estatísticos
  - Dashboards
  - Análises visuais

### Web Scraping
- `scripts/web_scraping/`: Scripts para coleta de dados da web
  - Scraping de websites
  - Coleta de dados de APIs

## Como Usar

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Dependências Principais

- Python 3.8+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- jupyter

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Faça push para a branch
5. Abra um Pull Request

## 🎯 Objetivos do Projeto

- Aprender fundamentos de manipulação de dados com Python
- Praticar visualização de dados com diferentes bibliotecas
- Explorar técnicas de análise exploratória de dados
- Implementar modelos básicos de machine learning
- Trabalhar com dados reais do Kaggle

## 📚 Conteúdo

### 1. Manipulação de Dados
- **scripts_pandas.py**: Operações básicas e avançadas com Pandas
- **scripts_numpy.py**: Manipulação numérica com NumPy
- **scripsts_carga_dados.py**: Diferentes formas de carregar dados

### 2. Visualização de Dados
- **data_viz.py**: Exemplos com Matplotlib e Seaborn
- Gráficos de dispersão, barras e linhas
- Personalização de visualizações
- Mapas de calor e correlações

### 3. Web Scraping
- **web_scraping.py**: Extração de dados da web
- Uso de BeautifulSoup e Requests
- Manipulação de HTML e JSON

### 4. Machine Learning
- **sem_6_machine_learning.py**: Introdução a algoritmos de ML
- **algoritmo_aprendizado_de_maquina.py**: Implementações práticas
- KNN, Regressão Linear e outros algoritmos

### 5. Análise de Dados do Kaggle
- **sem_7_predicao.py**: Análise do dataset California Housing
- **exemplo_kaggle.py**: Como usar a API do Kaggle
- Exemplos práticos de análise exploratória

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **Matplotlib** e **Seaborn**: Visualização de dados
- **Scikit-learn**: Machine Learning
- **BeautifulSoup**: Web Scraping
- **Kaggle API**: Acesso a datasets

## 📦 Como Instalar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/introducao_data_science.git
cd introducao_data_science
```

2. Instale as dependências:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn beautifulsoup4 kaggle
```

3. Configure a API do Kaggle:
   - Crie uma conta no [Kaggle](https://www.kaggle.com)
   - Baixe o arquivo `kaggle.json` das configurações da sua conta
   - Coloque o arquivo em `~/.kaggle/kaggle.json` (Linux/Mac) ou `C:\Users\<seu-usuario>\.kaggle\kaggle.json` (Windows)

## 🚀 Como Usar

Cada script pode ser executado independentemente:

```bash
python scripts_pandas.py
python data_viz.py
python sem_7_predicao.py
```

## 📊 Exemplos de Análises

O repositório inclui diversos exemplos práticos:

- Análise de preços de casas na Califórnia
- Classificação de flores Iris
- Análise de dados do mercado financeiro
- Web scraping de dados de linguagens de programação

## 📝 Exercícios e Práticas

- **4_sem_exerc.py**: Exercícios práticos de análise de dados
- **5_sem_exerc.py**: Práticas com visualização
- Diversos exemplos comentados para estudo

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Commitar suas mudanças
4. Fazer push para a branch
5. Abrir um Pull Request

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📫 Contato

- [Rafael Amorim Honorato]
- Email: [rafael.honorato03@gmail.com]
- LinkedIn: [https://www.linkedin.com/in/rafael-honorato03/]

## 🙏 Agradecimentos

- Kaggle pela disponibilização dos datasets
- Comunidade Python e Data Science
- Todos os contribuidores do projeto

