# 📚 Análise de Personagens em PDFs

Sistema completo para análise de personagens em arquivos PDF usando processamento de linguagem natural e análise de sentimentos.

## 🚀 Funcionalidades

- **Extração inteligente de texto** de PDFs usando PyMuPDF
- **Identificação automática de personagens** usando spaCy NER (Named Entity Recognition)
- **Análise de frequência** dos personagens mais importantes
- **Análise de sentimentos** por personagem usando LEIA (análise em português)
- **Gráficos de evolução temporal** mostrando onde os personagens aparecem no texto
- **Rede de relacionamentos** interativa entre personagens
- **Interface web** com Streamlit
- **Processamento otimizado** para arquivos grandes

## 📁 Arquivos Principais

### `analisador_personagens.py`
- Classe principal `AnalisadorDePersonagens`
- Processamento de linguagem natural com spaCy
- Análise de sentimentos com LEIA
- Geração de gráficos e visualizações
- Rede de relacionamentos com NetworkX e PyVis

### `app.py`
- Interface web interativa com Streamlit
- Upload de arquivos PDF
- Cache inteligente para otimização
- Visualizações dinâmicas e interativas
- Controles de seleção de personagens

### `big_data.py`
- Script de demonstração de técnicas de contagem de palavras
- Análise de sentimentos do texto do Machado de Assis
- Comparação de diferentes métodos de processamento de texto
- Exemplos práticos de análise de dados

## 🎯 Como Usar

### 1. Via Interface Web (Recomendado)
```bash
cd scripts/big_data
streamlit run app.py
```

### 2. Via Python Direto
```python
from analisador_personagens import AnalisadorDePersonagens

# Cria analisador
analisador = AnalisadorDePersonagens()

# Analisa PDF (bytes do arquivo)
with open("dados/seu_livro.pdf", "rb") as f:
    pdf_bytes = f.read()
analisador.analisar_livro(pdf_bytes)

# Gera visualizações
fig_freq = analisador.gerar_grafico_frequencia()
fig_evol = analisador.gerar_grafico_evolucao()
fig_sent = analisador.gerar_grafico_sentimentos()
html_rede = analisador.gerar_rede_relacionamentos()
```

### 3. Execução do Script de Demonstração
```bash
cd scripts/big_data
python big_data.py
```

## 📊 Resultados e Visualizações

### 1. Gráfico de Frequência de Personagens
- Top 25 personagens mais frequentes
- Gráfico de barras horizontal
- Ordenação por número de menções

### 2. Dispersão de Aparições dos Personagens
- Barrinhas verticais (|) mostrando cada aparição
- Visualização ponto a ponto no texto
- Contador de aparições por personagem
- Distribuição temporal precisa

### 3. Evolução Temporal dos Personagens
- Distribuição de menções ao longo do texto
- Gráfico de densidade (KDE)
- Seleção dinâmica de personagens
- Visualização da progressão da história

### 4. Análise de Sentimentos
- Sentimento médio por personagem
- Classificação: Positivo, Negativo, Neutro
- Gráfico de barras colorido por sentimento

### 5. Rede de Relacionamentos
- Grafo interativo com PyVis
- Nós representam personagens (tamanho baseado na frequência)
- Arestas representam interações entre personagens
- Visualização 3D interativa

## 🔧 Tecnologias Utilizadas

### Processamento de Linguagem Natural
- **spaCy**: Reconhecimento de entidades nomeadas (NER)
- **LEIA**: Análise de sentimentos em português
- **NLTK**: Processamento de texto adicional

### Visualização e Análise
- **Matplotlib/Seaborn**: Gráficos estáticos
- **NetworkX**: Análise de redes
- **PyVis**: Visualização interativa de grafos
- **Streamlit**: Interface web

### Manipulação de Dados
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica
- **PyMuPDF**: Extração de texto de PDFs

## ⚙️ Configurações e Otimizações

### Processamento em Chunks
- Processamento em blocos de 50.000 caracteres
- Controle de memória com garbage collection
- Cache inteligente do Streamlit

### Modelos de Linguagem
- **pt_core_news_sm**: Modelo em português (padrão)
- **en_core_web_sm**: Fallback para inglês
- Download automático de modelos

### Limpeza de Dados
- Remoção de títulos honoríficos (Sor, Lorde, etc.)
- Filtragem de nomes muito curtos (< 3 caracteres)
- Normalização de nomes próprios

## 📈 Performance

| Tamanho do PDF | Tempo Estimado | Memória |
|----------------|----------------|---------|
| < 100 páginas  | 30-60 segundos | 200MB   |
| 100-500 páginas| 1-3 minutos    | 400MB   |
| > 500 páginas  | 3-10 minutos   | 600MB   |

## 🎉 Vantagens do Sistema

- ✅ **Análise em português** nativo
- ✅ **Interface web intuitiva**
- ✅ **Visualizações interativas**
- ✅ **Processamento otimizado**
- ✅ **Cache inteligente**
- ✅ **Análise de sentimentos**
- ✅ **Rede de relacionamentos**

## 📝 Requisitos

```bash
pip install -r requirements.txt
```

### Dependências Principais
- streamlit
- pandas, numpy
- matplotlib, seaborn
- spacy, nltk
- networkx, pyvis
- PyMuPDF
- LEIA (análise de sentimentos em português)

## 🚀 Início Rápido

1. **Instale as dependências:**
   ```bash
   cd scripts/big_data
   pip install -r requirements.txt
   ```

2. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

3. **Faça upload de um PDF** na interface web

4. **Visualize os resultados** nas diferentes abas:
   - 📊 Gráficos de Personagens
   - 📈 Dispersão de Aparições
   - ❤️ Análise de Sentimentos  
   - 🕸️ Rede de Relacionamentos

## 📚 Exemplos de Uso

### Análise de Livros Clássicos
- Machado de Assis

### Casos de Uso
- Análise literária
- Estudos de personagens
- Pesquisa em humanidades digitais
- Análise de narrativas

---

**Sistema desenvolvido para análise avançada de personagens em PDFs usando técnicas de processamento de linguagem natural! 📚✨** 