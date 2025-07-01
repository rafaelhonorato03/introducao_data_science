# Análise de Personagens em PDFs

Este módulo permite identificar personagens em arquivos PDF e criar gráficos de aparição dos 20 principais nomes.

## 🚀 Funcionalidades

- **Extração de texto** de PDFs usando PyMuPDF ou PyPDF2
- **Identificação automática** de personagens baseada em capitalização
- **Gráfico de frequência** dos 20 personagens mais frequentes
- **Gráfico de dispersão** mostrando onde os personagens aparecem no texto
- **Suporte a acentos** e caracteres especiais do português
- **Filtro inteligente** de palavras comuns e números

## 📋 Pré-requisitos

Instale as dependências necessárias:

```bash
pip install -r dados/requirements_pdf.txt
```

### Dependências principais:
- `PyMuPDF` (ou `PyPDF2`) - para extração de texto de PDFs
- `pandas` - para manipulação de dados
- `matplotlib` - para criação de gráficos
- `numpy` - para operações numéricas

## 🔧 Como usar

### 1. Uso Simples

1. Coloque seu PDF na pasta `dados/`
2. Execute o script principal:

```bash
python scripts/big_data/analise_pdf_personagens.py
```

### 2. Uso Programático

```python
from big_data.analise_pdf_personagens import AnalisadorPDF

# Cria uma instância do analisador
analisador = AnalisadorPDF()

# Analisa um PDF
resultados = analisador.analisar_pdf('caminho/para/seu.pdf')

# Mostra os 20 personagens mais frequentes
for nome, freq in resultados.most_common(20):
    print(f"{nome}: {freq} aparições")
```

### 3. Exemplo Completo

Execute o script de exemplo para ver uma demonstração:

```bash
python scripts/big_data/exemplo_uso_pdf.py
```

## 📊 Resultados

O analisador gera:

1. **Lista dos 20 personagens mais frequentes** com número de aparições
2. **Gráfico de barras** (`personagens_frequencia.png`) - mostra frequência de aparição
3. **Gráfico de dispersão** (`personagens_dispersao.png`) - mostra onde no texto cada personagem aparece

### Exemplo de saída:

```
=== TOP 20 PERSONAGENS IDENTIFICADOS ===
 1. Bentinho: 45 aparições
 2. Capitu: 38 aparições
 3. Escobar: 25 aparições
 4. Dona: 20 aparições
 5. José: 15 aparições
...
```

## 🎯 Como funciona

### 1. Extração de Texto
- Usa **PyMuPDF** (mais robusto) ou **PyPDF2** como fallback
- Extrai texto de todas as páginas do PDF
- Preserva acentos e caracteres especiais

### 2. Identificação de Personagens
- Identifica palavras que começam com maiúscula
- Filtra palavras comuns (artigos, preposições, verbos)
- Remove números e siglas
- Considera apenas palavras com mais de 2 caracteres

### 3. Análise de Frequência
- Conta quantas vezes cada personagem aparece
- Ordena por frequência decrescente
- Gera estatísticas detalhadas

### 4. Criação de Gráficos
- **Gráfico de barras**: Frequência de aparição
- **Gráfico de dispersão**: Posição no texto (em porcentagem)

## ⚠️ Limitações

### Identificação de Personagens
- Baseada apenas em **capitalização**
- Pode incluir **falsos positivos**:
  - Nomes de lugares (Brasil, São Paulo)
  - Títulos (Doutor, Professor)
  - Nomes de meses (Janeiro, Fevereiro)
  - Início de frases

### Extração de PDF
- Funciona melhor com PDFs de **texto** (não escaneados)
- PDFs com **formatação complexa** podem ter problemas
- **PDFs protegidos** não podem ser processados

## 🔍 Melhorias Possíveis

### Para identificação mais precisa:
1. **Usar NLTK** com recursos de NER (Named Entity Recognition)
2. **Implementar spaCy** com modelo em português
3. **Criar lista de exclusão** personalizada
4. **Análise de contexto** para confirmar personagens

### Para extração melhor:
1. **OCR** para PDFs escaneados
2. **Preservação de formatação** (negrito, itálico)
3. **Detecção de capítulos** e seções

## 📁 Estrutura de Arquivos

```
scripts/big_data/
├── analise_pdf_personagens.py    # Analisador principal
├── exemplo_uso_pdf.py            # Exemplos de uso
└── README_analise_pdf.md         # Este arquivo

dados/
├── requirements_pdf.txt          # Dependências
└── *.pdf                        # Seus PDFs aqui

resultados/graficos/
├── personagens_frequencia.png    # Gráfico de frequência
└── personagens_dispersao.png     # Gráfico de dispersão
```

## 🛠️ Solução de Problemas

### Erro: "PyMuPDF não disponível"
```bash
pip install PyMuPDF
```

### Erro: "PDF não encontrado"
- Verifique se o PDF está na pasta `dados/`
- Verifique se o nome do arquivo está correto

### Gráficos não aparecem
- Verifique se a pasta `resultados/graficos/` existe
- Verifique permissões de escrita

### Poucos personagens identificados
- O PDF pode ter formatação que dificulta a extração
- Tente com um PDF de texto simples
- Verifique se os nomes começam com maiúscula no PDF

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Teste com o exemplo incluído
3. Verifique se o PDF não está corrompido
4. Considere usar um PDF de texto simples para teste

---

**Dica**: Para melhores resultados, use PDFs de livros ou textos literários onde os personagens são claramente identificados por nomes próprios. 