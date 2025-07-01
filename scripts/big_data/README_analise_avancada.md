# 📚 Analisador Avançado de Personagens em PDFs

## 🚀 Visão Geral

Este projeto evoluiu de uma ferramenta básica de análise de personagens para uma **plataforma completa de análise literária** com recursos avançados de IA, visualizações interativas e interface web.

## ✨ Novas Funcionalidades Implementadas

### 🔍 Análises Avançadas

#### 1. **Mapa de Relações entre Personagens**
- **Coocorrência em janelas de palavras** (configurável: 50-200 palavras)
- **Rede de relacionamentos** usando NetworkX
- **Matriz de coocorrência** com heatmap interativo
- **Métricas de centralidade**: grau, proximidade, intermediação

#### 2. **Detecção de Sentimentos por Personagem**
- **Análise de contexto** onde cada personagem aparece
- **Classificação de sentimentos**: positivo, negativo, neutro
- **Estatísticas detalhadas** por personagem
- **Gráficos de distribuição** de sentimentos

#### 3. **Análise Temporal e por Capítulos**
- **Divisão automática em capítulos** (baseada em padrões ou seções)
- **Personagem dominante por capítulo**
- **Timeline de evolução** dos personagens
- **Gráficos de densidade** temporal

#### 4. **Análise de Coocorrência**
- **Identificação de personagens que aparecem juntos**
- **Janelas de contexto configuráveis**
- **Visualização em rede** das relações
- **Métricas de força de relacionamento**

### 🧠 Integrações com IA

#### 1. **spaCy NER Avançado**
- **Modelos multilíngues** (português + fallback multilíngue)
- **Identificação precisa** de entidades nomeadas
- **Filtros inteligentes** para reduzir falsos positivos
- **Processamento otimizado** para textos grandes

#### 2. **Análise de Sentimentos**
- **TextBlob** para análise de sentimentos em português
- **Contexto de aparição** de cada personagem
- **Métricas estatísticas** (média, mediana, desvio padrão)
- **Classificação automática** de polaridade

#### 3. **Processamento de Texto Inteligente**
- **Divisão automática em capítulos** usando regex
- **Identificação de nomes compostos**
- **Filtros para títulos** (Dr., Sr., etc.)
- **Normalização de nomes**

### 📚 Audiências Específicas

#### **Para Professores:**
- **Ferramenta didática** para preparar aulas
- **Análises comparativas** entre obras
- **Material de apoio** sobre personagens
- **Visualizações educativas**

#### **Para Leitores:**
- **Exploração interativa** de obras clássicas
- **Descoberta de detalhes** sobre personagens
- **Comparação entre livros**
- **Análise de padrões** literários

#### **Para Escritores:**
- **Análise da própria obra**
- **Verificação de distribuição** de personagens
- **Identificação de personagens** "esquecidos"
- **Otimização da estrutura** narrativa

### 🌐 Interface Web Robusta

#### **Streamlit App (`app_streamlit.py`)**
- **Upload de PDFs** via interface web
- **Configurações interativas** de análise
- **Visualizações dinâmicas** com Plotly
- **Múltiplas abas** para diferentes análises
- **Download de relatórios** em JSON

#### **Recursos da Interface:**
- **Dashboard interativo** com métricas
- **Gráficos responsivos** e interativos
- **Tabelas detalhadas** com filtros
- **Exportação de dados** e relatórios
- **Interface intuitiva** e moderna

## 🛠️ Instalação e Configuração

### 1. **Instalação Automática**
```bash
# Execute o script de instalação
python scripts/big_data/install_dependencies.py
```

### 2. **Instalação Manual**
```bash
# Pacotes básicos
pip install pandas numpy matplotlib seaborn scikit-learn

# Pacotes para PDFs
pip install PyPDF2 PyMuPDF

# Pacotes para NLP
pip install spacy textblob

# Pacotes para análises avançadas
pip install networkx

# Pacotes para interface web
pip install streamlit plotly

# Modelos spaCy
python -m spacy download pt_core_news_sm
# ou
python -m spacy download xx_ent_wiki_sm
```

## 🚀 Como Usar

### 1. **Análise Básica (Linha de Comando)**
```bash
# Execute o analisador principal
python scripts/big_data/analise_pdf_ner.py
```

### 2. **Interface Web (Recomendado)**
```bash
# Inicie a aplicação Streamlit
streamlit run scripts/big_data/app_streamlit.py
```

### 3. **Uso Programático**
```python
from analise_pdf_ner import AnalisadorPDFNER

# Inicializa o analisador
analisador = AnalisadorPDFNER()

# Executa análise completa
resultados = analisador.analisar_pdf("caminho/para/arquivo.pdf", analise_completa=True)

# Acessa resultados
print(f"Personagens encontrados: {len(analisador.freq_personagens)}")
print(f"Relações identificadas: {analisador.rede_personagens.number_of_edges()}")
print(f"Análise de sentimentos: {len(analisador.analise_sentimentos)}")
```

## 📊 Saídas e Visualizações

### **Gráficos Gerados:**
1. **Frequência de personagens** (barras)
2. **Dispersão temporal** (linha do tempo)
3. **Rede de relacionamentos** (grafo)
4. **Análise de sentimentos** (barras coloridas)
5. **Evolução temporal** (linhas)
6. **Matriz de coocorrência** (heatmap)

### **Arquivos de Saída:**
- `resultados/graficos/` - Todos os gráficos em PNG
- `resultados/relatorio_completo.json` - Dados estruturados
- Relatórios interativos via Streamlit

### **Dados Estruturados:**
```json
{
  "metadata": {
    "data_analise": "2024-01-01T12:00:00",
    "total_caracteres": 150000,
    "total_palavras": 25000,
    "total_capitulos": 15
  },
  "personagens": {
    "total_identificados": 45,
    "top_10": {"Capitu": 150, "Bentinho": 120, ...},
    "frequencias_completas": {...}
  },
  "analise_temporal": {...},
  "analise_sentimentos": {...},
  "coocorrencias": {...}
}
```

## 🔧 Configurações Avançadas

### **Parâmetros de Análise:**
- **Janela de coocorrência**: 50-200 palavras (padrão: 100)
- **Top N personagens**: 5-30 (padrão: 15)
- **Análise completa**: inclui todas as análises avançadas
- **Modelo spaCy**: português ou multilíngue

### **Otimizações:**
- **Processamento em lotes** para textos grandes
- **Cache de resultados** para análises repetidas
- **Configuração de memória** para spaCy
- **Paralelização** de análises independentes

## 📈 Métricas e Análises

### **Métricas de Personagens:**
- **Frequência de aparição**
- **Posição no texto** (dispersão)
- **Coocorrência** com outros personagens
- **Sentimento médio** do contexto

### **Métricas de Rede:**
- **Centralidade de grau**
- **Centralidade de proximidade**
- **Centralidade de intermediação**
- **Densidade da rede**

### **Métricas Temporais:**
- **Personagem dominante** por capítulo
- **Evolução** ao longo da obra
- **Picos de aparição**
- **Distribuição** por seções

## 🎯 Casos de Uso

### **Análise de Obras Clássicas:**
- **Dom Casmurro**: análise de Capitu vs. Bentinho
- **Hamlet**: rede de personagens da corte
- **Harry Potter**: evolução dos personagens principais

### **Análise Acadêmica:**
- **Teses e dissertações** sobre literatura
- **Pesquisas** em análise de texto
- **Estudos comparativos** entre autores

### **Análise Criativa:**
- **Escritores** analisando próprias obras
- **Editores** verificando estrutura
- **Críticos literários** explorando padrões

## 🔮 Próximos Passos

### **Funcionalidades Futuras:**
1. **Integração com GPT** para resumos automáticos
2. **Clustering de personagens** por comportamento
3. **Análise de diálogos** e interações
4. **Comparação entre obras** do mesmo autor
5. **API REST** para integração com outros sistemas
6. **Banco de dados** para armazenar análises
7. **Sistema de usuários** e projetos
8. **Análise de múltiplos idiomas**

### **Melhorias Técnicas:**
1. **Processamento distribuído** para textos muito grandes
2. **Modelos de IA mais avançados** (transformers)
3. **Interface mais robusta** (React/Vue)
4. **Backend escalável** (FastAPI/Flask)
5. **Cache inteligente** e otimizações

## 🤝 Contribuição

Este projeto está em constante evolução. Contribuições são bem-vindas:

1. **Reporte bugs** e problemas
2. **Sugira novas funcionalidades**
3. **Contribua com código**
4. **Melhore a documentação**
5. **Teste com diferentes obras**

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

**🎉 Transforme a análise literária em uma experiência interativa e científica!** 