# 📚 Analisador de Personagens em Livros PDF

Um aplicativo Streamlit para análise avançada de personagens em livros em formato PDF, utilizando técnicas de Processamento de Linguagem Natural (NLP) e Análise de Redes Sociais.

## 🚀 Funcionalidades

### 📊 Análises Disponíveis

1. **Frequência de Personagens**
   - Top personagens mais mencionados
   - Gráficos de barras interativos
2. **Evolução Temporal**
   - Distribuição das menções ao longo do livro
   - Gráficos de densidade (KDE)
   - Seleção dinâmica de personagens
3. **Dispersão de Aparições**
   - Visualização da posição de cada menção no texto
   - Barrinhas verticais representando aparições
4. **Análise de Sentimentos**
   - Sentimento médio associado a cada personagem
   - Código de cores (verde=positivo, vermelho=negativo)
5. **Rede de Relacionamentos**
   - Grafo interativo de conexões entre personagens
   - Tamanho dos nós baseado na frequência
   - Espessura das arestas baseada nas interações
6. **Personagens-Ponte** ⭐ **NOVO!**
   - Análise de centralidade de intermediação
   - Identificação de personagens conectores da narrativa

## 🛠️ Instalação

```bash
# Instalar dependências (recomenda-se usar o requirements.txt da raiz do projeto)
pip install -r ../../requirements/requirements.txt

# Baixar modelos do Spacy
python -m spacy download pt_core_news_sm
python -m spacy download en_core_web_sm
```

## 🎯 Como Usar

1. **Execute o aplicativo Streamlit:**
   ```bash
   cd src/big_data/apps
   streamlit run streamlit_app.py
   ```

2. **Acesse no navegador:**
   ```
   http://localhost:8501
   ```

3. **Faça upload de um PDF:**
   - Arraste e solte um arquivo PDF
   - Aguarde a análise (pode demorar alguns minutos)

4. **Explore os resultados:**
   - Navegue pelas abas para ver diferentes análises
   - Use os controles interativos para personalizar visualizações

## 📋 Requisitos

- Python 3.8+
- 4GB+ RAM (recomendado)
- Conexão com internet (para download de modelos)

## 🔧 Dependências Principais

- **Streamlit**: Interface web
- **Spacy**: Processamento de linguagem natural
- **PyMuPDF**: Leitura de arquivos PDF
- **NetworkX**: Análise de redes
- **Pyvis**: Visualização de grafos
- **Leia**: Análise de sentimentos em português
- **Python-Louvain**: Detecção de comunidades

## 📊 Exemplos de Análise

### Personagens-Ponte
Esta nova funcionalidade identifica personagens que funcionam como "pontes" na narrativa:

- **Centralidade de Intermediação**: Mede quantas vezes um personagem aparece no caminho mais curto entre outros personagens
- **Conectores Narrativos**: Personagens que ligam diferentes grupos de personagens
- **Fluxo da História**: Essenciais para o desenvolvimento da trama

### Interpretação dos Resultados

- **Valores altos**: Personagem é ponte entre diferentes grupos
- **Valores baixos**: Personagem mais isolado ou em grupo específico
- **Zero**: Personagem não conecta outros grupos

## 🐛 Solução de Problemas

### Erro de Importação do Community
```bash
pip install python-louvain
```

### Modelos Spacy Não Encontrados
```bash
python -m spacy download pt_core_news_sm
python -m spacy download en_core_web_sm
```

### PDF Muito Grande
- O aplicativo processa PDFs de qualquer tamanho
- Para PDFs muito grandes (>100MB), pode demorar vários minutos
- Use a barra de progresso para acompanhar

## 🔄 Cache e Performance

- **Cache Inteligente**: Resultados são salvos para evitar reprocessamento
- **Identificação por Arquivo**: Cada arquivo tem cache único
- **Limpeza Automática**: Cache é limpo quando arquivo é removido

## 📁 Estrutura da Pasta `big_data`

```
src/big_data/
├── apps/
│   ├── streamlit_app.py           # App principal do Streamlit
│   ├── personagem_analyzer.py     # Lógica de análise otimizada para Streamlit
│   └── ... (outros arquivos da app)
├── nlp_analysis/
│   ├── analisador_personagens.py  # Análise completa com sentimentos
│   ├── big_data_tecnicas.py       # Técnicas auxiliares de NLP
│   └── ...
├── text_processing/
│   ├── livro_analyzer.py          # Análise de livros (ex: Dom Casmurro)
│   ├── dom_casmurro.pdf           # Exemplo de PDF
│   └── requirements.txt           # Dependências específicas
└── README.md
```

## 📈 Melhorias Futuras

- [ ] Análise por capítulos
- [ ] Detecção de diálogos
- [ ] Comparação entre livros
- [ ] Exportação de resultados
- [ ] Análise de cenas
- [ ] Interface mais responsiva

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Se encontrar problemas ou tiver sugestões:

1. Verifique a seção de solução de problemas
2. Abra uma issue no GitHub
3. Consulte a documentação das dependências

---

**Desenvolvido com ❤️ para análise de literatura** 