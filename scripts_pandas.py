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
# Listas separadas para estados, anos e populações
dados = {'estados':[
    "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
    "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
    "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí",
    "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
    "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
],
'anos' :[
    2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031,
    2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043,
    2044, 2045, 2046
],
'populacoes': [
    894470, 3351543, 861773, 4207714, 14930634, 9240580, 3094325, 4064052,
    7206589, 7153262, 3567234, 2839188, 21411923, 9207715, 4059905, 11937148,
    9674793, 3281480, 17463349, 3560903, 11422973, 1815278, 652713, 7338473,
    46649132, 2318822, 1590248
]}

# Exibindo DataFrame
df1 = pd.DataFrame(dados)
print(df1)
print(df1.head(2))
print(df1.tail(2))
print(df1.sample(5))
print(df1.info())
print(df1.describe())

df2 = pd.DataFrame(dados, columns=['anos', 'estados', 'populacoes'])
print(df2)

print(df2['estados'])

df2['estimativa'] = 50
print(df2)

df2['estimativa'] = np.arrange(1, 27)
print(df2)