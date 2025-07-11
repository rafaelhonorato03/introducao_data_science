# Importando bibliotecas necessárias
import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# ==========================================
# ANÁLISE E COMPARAÇÃO DE TÉCNICAS DE CONTAGEM DE PALAVRAS
# ==========================================
# Este script demonstra diferentes abordagens para contar a frequência
# de palavras em um texto, cada uma com suas vantagens e desvantagens

# Texto de exemplo para análise
sentence = "Este é um exemplo de contagem de palavras"
print(f"Texto analisado: '{sentence}'")
print()

# ==========================================
# MÉTODO 1: Usando split() + dicionário manual
# ==========================================
# Vantagens: Simples e direto
# Desvantagens: Código verboso, precisa verificar se chave existe
print("=== MÉTODO 1: Split + Dicionário Manual ===")
words = sentence.split()  # Divide o texto em palavras usando espaços como separador

# Inicializa dicionário vazio para armazenar contagens
word_count = {}
for word in words:
    # Verifica se a palavra já existe no dicionário
    if word in word_count:
        word_count[word] += 1  # Incrementa contador se palavra já existe
    else:
        word_count[word] = 1   # Inicializa contador se palavra é nova
print(f"Resultado: {word_count}")
print()

# ==========================================
# MÉTODO 2: Usando set() + count()
# ==========================================
# Vantagens: Mais eficiente para textos grandes (evita repetições)
# Desvantagens: Ainda verboso, count() é O(n) para cada palavra
print("=== MÉTODO 2: Set + Count ===")
unique_words = set(words)  # Cria conjunto com palavras únicas (elimina duplicatas)

word_count2 = {}
for word in unique_words:
    # Conta quantas vezes cada palavra aparece no texto original
    word_count2[word] = words.count(word)
print(f"Resultado: {word_count2}")
print()

# ==========================================
# MÉTODO 3: Usando Counter (RECOMENDADO)
# ==========================================
# Vantagens: Mais eficiente, código limpo, funcionalidades extras
# Desvantagens: Requer import da biblioteca collections
print("=== MÉTODO 3: Counter (Recomendado) ===")
from collections import Counter
word_count3 = Counter(words)  # Counter automaticamente conta frequências
print(f"Resultado: {word_count3}")
print()

# ==========================================
# MÉTODO 4: Usando regex + Counter
# ==========================================
# Vantagens: Mais preciso para textos complexos, remove pontuação
# Desvantagens: Mais complexo, pode ser mais lento
print("=== MÉTODO 4: Regex + Counter ===")
# \b = word boundary (fronteira de palavra)
# \w+ = uma ou mais letras/números/underscore
# \b\w+\b = palavra completa delimitada por fronteiras
words2 = re.findall(r'\b\w+\b', sentence)
word_count4 = Counter(words2)  # Conta palavras extraídas por regex
print(f"Palavras extraídas por regex: {words2}")
print(f"Resultado: {word_count4}")
print()

# ==========================================
# COMPARAÇÃO DOS RESULTADOS
# ==========================================
print("=== COMPARAÇÃO DOS RESULTADOS ===")
print("Todos os métodos produzem o mesmo resultado para este texto simples.")
print("Diferenças apareceriam em textos com pontuação, números, etc.")
print()
print("RECOMENDAÇÃO: Use Counter para a maioria dos casos!")
print("- Código mais limpo e legível")
print("- Mais eficiente internamente")
print("- Métodos úteis como .most_common(), .elements(), etc.")
print()

# ==========================================
# ANÁLISE DE SENTIMENTO DO TEXTO DO MACHADO DE ASSIS
# ==========================================
# Analisa o sentimento das sentenças do arquivo machado_de_assis.txt
print("=== ANÁLISE DE SENTIMENTO DO MACHADO DE ASSIS ===")

# Baixa recursos necessários do NLTK (execute apenas uma vez)
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    print("Baixando recursos do VADER...")
    nltk.download('vader_lexicon')

# Carrega o arquivo do Machado de Assis
arquivo_path = '../../data/raw/machado_de_assis.txt'
try:
    with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
        texto_completo = arquivo.read()
    print(f"Arquivo carregado: {arquivo_path}")
    print(f"Tamanho do texto: {len(texto_completo)} caracteres")
except FileNotFoundError:
    print(f"Arquivo {arquivo_path} não encontrado!")
    print("Tentando caminho alternativo...")
    try:
        # Tenta caminho alternativo
        arquivo_path = '../../../data/raw/machado_de_assis.txt'
        with open(arquivo_path, 'r', encoding='utf-8') as arquivo:
            texto_completo = arquivo.read()
        print(f"Arquivo carregado: {arquivo_path}")
        print(f"Tamanho do texto: {len(texto_completo)} caracteres")
    except FileNotFoundError:
        print(f"Arquivo não encontrado em nenhum caminho!")
        print("Usando texto de exemplo...")
        texto_completo = """
        O homem é um animal racional. Esta é uma afirmação filosófica muito antiga.
        Mas o que significa ser racional? Significa que o homem pensa antes de agir.
        Nem sempre isso acontece, é verdade. Às vezes agimos por impulso.
        A vida é cheia de surpresas e desafios. Alguns são bons, outros nem tanto.
        O importante é manter a esperança e seguir em frente.
        """

# Função simples para separar sentenças (baseada em pontuação)
def separar_sentencas(texto):
    """Separa o texto em sentenças usando pontuação como separador"""
    # Remove quebras de linha e espaços extras
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    texto = ' '.join(texto.split())
    
    # Separa por pontos, exclamação e interrogação
    sentencas = []
    for sentenca in re.split(r'[.!?]+', texto):
        sentenca = sentenca.strip()
        if len(sentenca) > 10:  # Só inclui sentenças com mais de 10 caracteres
            sentencas.append(sentenca)
    
    return sentencas

# Separa o texto em sentenças
sentencas = separar_sentencas(texto_completo)
print(f"Total de sentenças encontradas: {len(sentencas)}")

# Mostra algumas sentenças como exemplo
print("\nExemplos de sentenças extraídas:")
for i, sentenca in enumerate(sentencas[:5], 1):
    print(f"{i}. {sentenca[:100]}...")

# Inicializa o analisador de sentimento
sa = SentimentIntensityAnalyzer()

# Listas para armazenar resultados
lista_sentencas = []
lista_pontuacoes = []
lista_sentimentos = []

print(f"\nAnalisando sentimento de {len(sentencas)} sentenças...")
for i, sentenca in enumerate(sentencas):
    if i % 50 == 0:  # Mostra progresso a cada 50 sentenças
        print(f"Processando sentença {i+1}/{len(sentencas)}...")
    
    lista_sentencas.append(sentenca)
    
    # Analisa o sentimento da sentença
    pontuacao = sa.polarity_scores(sentenca)
    lista_pontuacoes.append(pontuacao['compound'])
    
    # Classifica o sentimento baseado na pontuação compound
    if pontuacao['compound'] > 0.05:
        sentimento = 'Positivo'
    elif pontuacao['compound'] < -0.05:
        sentimento = 'Negativo'
    else:
        sentimento = 'Neutro'
    
    lista_sentimentos.append(sentimento)

# Cria DataFrame com os resultados
df = pd.DataFrame({
    'sentenca': lista_sentencas, 
    'pontuacao': lista_pontuacoes,
    'sentimento': lista_sentimentos
})

print("\n=== RESULTADOS DA ANÁLISE ===")
print(f"Total de sentenças analisadas: {len(df)}")

# ==========================================
# ANÁLISE ESTATÍSTICA DOS SENTIMENTOS
# ==========================================
print("\n=== ESTATÍSTICAS DOS SENTIMENTOS ===")

# Conta sentenças negativas (compound < -0.05)
selecao_neg = df.pontuacao < -0.05
negativas = df[selecao_neg]
print(f"Sentenças negativas: {len(negativas)}")

# Conta sentenças positivas (compound > 0.05)
selecao_pos = df.pontuacao > 0.05
positivas = df[selecao_pos]
print(f"Sentenças positivas: {len(positivas)}")

# Conta sentenças neutras (-0.05 <= compound <= 0.05)
selecao_neu = (df.pontuacao >= -0.05) & (df.pontuacao <= 0.05)
neutras = df[selecao_neu]
print(f"Sentenças neutras: {len(neutras)}")

# ==========================================
# CRIAÇÃO DO GRÁFICO
# ==========================================
print("\n=== CRIANDO GRÁFICO ===")

# Dados para o gráfico
categorias = ['Negativas', 'Neutras', 'Positivas']
quantidades = [len(negativas), len(neutras), len(positivas)]
cores = ['#ff6b6b', '#feca57', '#48dbfb']

# Cria o gráfico de barras
plt.figure(figsize=(10, 6))
bars = plt.bar(categorias, quantidades, color=cores, alpha=0.8)

# Adiciona valores nas barras
for bar, quantidade in zip(bars, quantidades):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
             str(quantidade), ha='center', va='bottom', fontweight='bold')

# Configurações do gráfico
plt.title('Análise de Sentimento - Machado de Assis', fontsize=16, fontweight='bold')
plt.xlabel('Tipo de Sentimento', fontsize=12)
plt.ylabel('Número de Sentenças', fontsize=12)
plt.grid(True, alpha=0.3)

# Adiciona porcentagens no eixo Y secundário
total = len(df)
porcentagens = [q/total*100 for q in quantidades]
ax2 = plt.twinx()
ax2.set_ylim(0, max(porcentagens) * 1.1)
ax2.set_ylabel('Porcentagem (%)', fontsize=12)

# Salva o gráfico
plt.tight_layout()
plt.savefig('resultados/graficos/analise_sentimento_machado.png', dpi=300, bbox_inches='tight')
print("Gráfico salvo como 'resultados/graficos/analise_sentimento_machado.png'")
plt.show()

# ==========================================
# RESUMO FINAL
# ==========================================
print("\n=== RESUMO FINAL ===")
print(f"Total de sentenças analisadas: {len(df)}")
print(f"Positivas: {len(positivas)} ({len(positivas)/len(df)*100:.1f}%)")
print(f"Negativas: {len(negativas)} ({len(negativas)/len(df)*100:.1f}%)")
print(f"Neutras: {len(neutras)} ({len(neutras)/len(df)*100:.1f}%)")

print("\nDICA: O VADER funciona melhor com:")
print("- Textos informais (redes sociais)")
print("- Frases com pontuação (!, ?)")
print("- Palavras em maiúsculo")
print("- Emojis e abreviações")
print("\nPara textos literários como Machado de Assis, os resultados podem ser mais neutros.")

# ==========================================
# ANÁLISE DE NOMES PRÓPRIOS MAIS FREQUENTES
# ==========================================
print("\n=== ANÁLISE DE NOMES PRÓPRIOS ===")

# Lê o texto do Machado de Assis
with open('dados/machado_de_assis.txt', 'r', encoding='utf-8') as f:
    texto = f.read()

# ----------- MÉTODO SIMPLIFICADO -----------
import re
from collections import Counter

# Função simples para tokenizar (dividir em palavras)
def tokenizar_simples(texto):
    """Divide o texto em palavras de forma simples"""
    # Remove caracteres especiais e quebras de linha
    texto_limpo = re.sub(r'[^\w\s]', ' ', texto)
    texto_limpo = texto_limpo.replace('\n', ' ').replace('\r', ' ')
    
    # Divide em palavras
    palavras = texto_limpo.split()
    
    # Filtra palavras muito curtas e números
    palavras_filtradas = [palavra for palavra in palavras if len(palavra) > 2 and not palavra.isdigit()]
    
    return palavras_filtradas

# Função para identificar possíveis nomes próprios
def identificar_nomes_proprios(palavras):
    """Identifica possíveis nomes próprios baseado em capitalização"""
    nomes_proprios = []
    
    for palavra in palavras:
        # Verifica se a palavra começa com maiúscula e tem mais de 2 caracteres
        if palavra[0].isupper() and len(palavra) > 2 and palavra.isalpha():
            nomes_proprios.append(palavra)
    
    return nomes_proprios

print("Processando o texto...")
palavras = tokenizar_simples(texto)
print(f"Total de palavras encontradas: {len(palavras)}")

print("Identificando nomes próprios...")
nomes_proprios = identificar_nomes_proprios(palavras)
print(f"Total de possíveis nomes próprios: {len(nomes_proprios)}")

# Conta a frequência dos nomes próprios
freq_nomes = Counter(nomes_proprios)
mais_comuns = freq_nomes.most_common(20)

print("\n20 possíveis nomes próprios mais frequentes:")
for nome, freq in mais_comuns:
    print(f"{nome}: {freq}")

# Plota os 20 nomes próprios mais frequentes
print("\nCriando gráfico dos nomes próprios...")
plt.figure(figsize=(12, 6))
nomes = [nome for nome, freq in mais_comuns]
frequencias = [freq for nome, freq in mais_comuns]

plt.bar(range(len(nomes)), frequencias, color='skyblue', alpha=0.7)
plt.xlabel('Nomes Próprios')
plt.ylabel('Frequência')
plt.title('20 nomes próprios mais frequentes - Machado de Assis')
plt.xticks(range(len(nomes)), nomes, rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ----------- ANÁLISE DE DISPERSÃO SIMPLIFICADA -----------
print("\nCriando análise de dispersão...")

# Função para encontrar posições das palavras no texto
def encontrar_posicoes(texto, palavras_busca):
    """Encontra as posições das palavras no texto"""
    texto_lower = texto.lower()
    posicoes = {}
    
    for palavra in palavras_busca:
        posicoes[palavra] = []
        palavra_lower = palavra.lower()
        start = 0
        
        while True:
            pos = texto_lower.find(palavra_lower, start)
            if pos == -1:
                break
            posicoes[palavra].append(pos)
            start = pos + 1
    
    return posicoes

# Encontra posições dos nomes mais comuns
nomes_mais_comuns = [nome for nome, freq in mais_comuns[:10]]  # Top 10 para visualização
posicoes = encontrar_posicoes(texto, nomes_mais_comuns)

# Cria gráfico de dispersão
plt.figure(figsize=(15, 8))
for i, nome in enumerate(nomes_mais_comuns):
    if posicoes[nome]:
        plt.scatter(posicoes[nome], [i] * len(posicoes[nome]), 
                   label=nome, alpha=0.7, s=20)

plt.xlabel('Posição no texto')
plt.ylabel('Nomes Próprios')
plt.title('Dispersão dos nomes próprios no texto - Machado de Assis')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n=== RESUMO DA ANÁLISE ===")
print(f"Total de palavras no texto: {len(palavras)}")
print(f"Possíveis nomes próprios encontrados: {len(nomes_proprios)}")
print(f"Tipos únicos de nomes próprios: {len(set(nomes_proprios))}")
print(f"Nome próprio mais frequente: {mais_comuns[0][0]} ({mais_comuns[0][1]} ocorrências)")

print("\nDICA: Esta análise é simplificada. Para resultados mais precisos:")
print("- Use NLTK com recursos completos")
print("- Use spaCy com modelo em português")
print("- Considere o contexto do texto para filtrar falsos positivos")