# 📚 Análise de Personagens em PDFs

Sistema completo para análise de personagens em arquivos PDF, otimizado para funcionar com arquivos de qualquer tamanho.

## 🚀 Funcionalidades

- **Extração inteligente de texto** de PDFs
- **Identificação automática de personagens** usando análise de nomes próprios
- **Análise de frequência** dos personagens mais importantes
- **Gráficos de dispersão** mostrando onde os personagens aparecem no texto
- **Interface web** com Streamlit
- **Otimizado para arquivos grandes** com amostragem inteligente

## 📁 Arquivos Principais

### `analise_personagens_pdf.py`
- Classe principal `AnalisadorPDF`
- Algoritmo otimizado para arquivos grandes
- Configurações ajustáveis
- Geração de gráficos

### `app_streamlit_limpo.py`
- Interface web interativa
- Configurações visuais
- Exibição de resultados em tempo real

## ⚙️ Configurações

### Modos de Análise

#### Rápida (Recomendado)
- **Para:** Arquivos grandes (> 200 páginas)
- **Configuração:** 25k palavras, 200 personagens, amostra de páginas
- **Tempo:** 30-60 segundos

#### Equilibrada
- **Para:** Arquivos médios (50-200 páginas)
- **Configuração:** 50k palavras, 500 personagens, amostra de páginas
- **Tempo:** 60-120 segundos

#### Completa
- **Para:** Arquivos pequenos (< 50 páginas)
- **Configuração:** 100k palavras, 1000 personagens, texto completo
- **Tempo:** 10-30 segundos

## 🎯 Como Usar

### 1. Via Python
```python
from analise_personagens_pdf import AnalisadorPDF

# Cria analisador
analisador = AnalisadorPDF(
    max_palavras=50000,
    max_personagens=500,
    amostra_texto=True
)

# Analisa PDF
resultados = analisador.analisar_pdf("dados/seu_livro.pdf")

# Mostra top 20 personagens
analisador.mostrar_top_personagens(20)
```

### 2. Via Interface Web
```bash
cd scripts/big_data
streamlit run app_streamlit_limpo.py
```

### 3. Execução Direta
```bash
cd scripts/big_data
python analise_personagens_pdf.py
```

## 📊 Resultados

### Top 20 Personagens
O sistema mostra os 20 personagens mais frequentes em formato de tabela:

```
==================================================
🏆 TOP 20 PERSONAGENS MAIS FREQUENTES
==================================================
Pos  Personagem               Freq     % do Total
--------------------------------------------------
1    José Gabriel             45       12.3%
2    Maria Clara              38       10.4%
3    Pedro Santos             32        8.7%
...
```

### Gráficos Gerados
- **`personagens_frequencia.png`**: Gráfico de barras com frequência
- **`personagens_dispersao.png`**: Gráfico de dispersão com traços verticais

## 🔧 Amostragem Inteligente

Para arquivos grandes, o sistema usa amostragem inteligente:

- **Primeiras 20 páginas**: Captura introdução e personagens principais
- **20 páginas do meio**: Captura desenvolvimento da história
- **Últimas 20 páginas**: Captura conclusão e resolução

Isso garante que mesmo livros muito grandes sejam analisados de forma eficiente.

## 📈 Performance

| Tamanho do PDF | Modo | Tempo | Memória |
|----------------|------|-------|---------|
| < 50 páginas   | Completa | 10-30s | 100MB |
| 50-200 páginas | Equilibrada | 30-60s | 200MB |
| > 200 páginas  | Rápida | 60-120s | 300MB |

## 🎉 Vantagens

- ✅ **Não trava** com arquivos grandes
- ✅ **Uso controlado de memória**
- ✅ **Tempo de execução previsível**
- ✅ **Interface web intuitiva**
- ✅ **Configurações flexíveis**
- ✅ **Resultados organizados**

## 📝 Requisitos

```bash
pip install streamlit pandas matplotlib PyMuPDF PyPDF2 tqdm
```

## 🚀 Início Rápido

1. Coloque um PDF na pasta `dados/`
2. Execute: `streamlit run app_streamlit_limpo.py`
3. Selecione o PDF e clique em "Iniciar Análise"
4. Visualize os resultados!

---

**Desenvolvido para análise eficiente de personagens em qualquer tipo de PDF! 📚✨** 