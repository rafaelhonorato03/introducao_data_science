# Introdução à Ciência de Dados

Este repositório foi reorganizado para facilitar o acesso, manutenção e entendimento dos arquivos e scripts. Abaixo está a nova estrutura e o propósito de cada pasta:

## Estrutura de Pastas

```
introducao_data_science/
│
├── data/
│   ├── raw/         # Dados brutos (csv, txt, pdf, sqlite, etc)
│   ├── processed/   # Dados tratados ou intermediários
│   └── external/    # Dados externos ou de referência
│
├── notebooks/       # Notebooks Jupyter para análises e experimentos
│   └── semana_3/    # Subpasta de exercícios ou temas específicos
│
├── src/             # Scripts Python organizados por tema
│   ├── data_analysis/      # Análise de dados
│   ├── big_data/           # Scripts e apps de big data
│   │   ├── analise_livros/
│   │   └── app_analise_personagens/
│   ├── ml/                 # Machine Learning
│   ├── visualization/      # Visualização de dados
│   └── web_scraping/       # Web scraping
│
├── results/
│   └── figures/     # Gráficos e imagens gerados
│
├── requirements/    # Arquivos de dependências (requirements*.txt)
│
├── docs/            # Documentação, PDFs de referência, README antigo
│
└── README.md        # Este arquivo
```

## Recomendações
- Use as pastas temáticas em `src/` para scripts.
- Salve dados brutos em `data/raw` e dados processados em `data/processed`.
- Centralize notebooks em `notebooks/`.
- Armazene resultados e gráficos em `results/figures`.
- Documentação e arquivos de referência devem ir para `docs/`.

---

Sinta-se à vontade para adaptar a estrutura conforme o crescimento do projeto! 