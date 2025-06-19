import pandas as pd
import re

# Analisando e comparando técnicas de contagem de palavras
sentence = "Este é um exemplo de contagem de palavras"
words = sentence.split()

# Método split
word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1
print(word_count)

# Método set
unique_words = set(words)
word_count2 = {}
for word in unique_words:
    word_count2[word] = words.count(word)
print(word_count2)

# Método Counter
from collections import Counter
word_count3 = Counter(words)
print(word_count3)

# Método re.findall
words2 = re.findall(r'\b\w+\b', sentence)
word_count4 = Counter(words)
print(word_count4)

