import pandas as pd
import numpy as np

series1 = pd.Series([1, 2, -3, 4, 5])
print(series1)
print(series1.values)
print(series1.index)
print(series1.dtype)

series2 = pd.Series([1, 2, -3, 4, 5], index= ['a', 'b', 'c', 'd', 'e'])
print(series2)

series2['b'] = 1000
print(series2)

print(series1[series1 > 3])

# Algebra
print(series1)
print(series1*2)


#DataFrame

estados_populacao = {
    "Acre": 894470,
    "Alagoas": 3351543,
    "Amapá": 861773,
    "Amazonas": 4207714,
    "Bahia": 14930634,
    "Ceará": 9240580,
    "Distrito Federal": 3094325,
    "Espírito Santo": 4064052,
    "Goiás": 7206589,
    "Maranhão": 7153262,
    "Mato Grosso": 3567234,
    "Mato Grosso do Sul": 2839188,
    "Minas Gerais": 21411923,
    "Pará": 9207715,
    "Paraíba": 4059905,
    "Paraná": 11937148,
    "Pernambuco": 9674793,
    "Piauí": 3281480,
    "Rio de Janeiro": 17463349,
    "Rio Grande do Norte": 3560903,
    "Rio Grande do Sul": 11422973,
    "Rondônia": 1815278,
    "Roraima": 652713,
    "Santa Catarina": 7338473,
    "São Paulo": 46649132,
    "Sergipe": 2318822,
    "Tocantins": 1590248
}

# Exibindo o dicionário
print(estados_populacao)