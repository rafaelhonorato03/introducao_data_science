# Importando bibliotecas necessárias
import pandas as pd
import re

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

