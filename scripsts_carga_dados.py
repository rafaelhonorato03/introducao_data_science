import csv
import pandas as pd
import matplotlib.pyplot as plt

# Abrindo o arquivo com a codificação correta
with open('machado_de_assis.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.readlines()

print(conteudo)
for linha in conteudo:
    print(linha)

# Brincando com o texto
x = ''
for linha in conteudo:
    if linha != '':
        x += linha

cidade = input('Por qual cidade você quer substituir a cidade natal de Machado de Assis?' )

print(x)
x = x.replace('Rio de Janeiro', cidade)
print(x)

arquivo_novo = open('machado_de_assis_novo.txt', 'w')
arquivo_novo.writelines(x)
arquivo_novo.close()

# trabalhando com csv
with open('TSLA.csv', 'r') as f:
    leitor = csv.reader(f, delimiter = ',')
    for coluna in leitor:
        data = coluna[0]
        abertura = coluna[1]
        altura_max = coluna[2]
        fechamento = coluna[4]
        print('Data: ', data, 'Abertura: ', abertura, 'Altura Maxima: ', altura_max, 'Fechamento: ', fechamento)

arquivo_tesla = 'TSLA.csv'
dados_tesla = pd.read_csv(arquivo_tesla, skiprows=1, names=['Date', 'Open', 'High', 'Low'], nrows=5)
print(dados_tesla.head(10))

# Utilizando APIs
arquivo = 'https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/2010_alcohol_consumption_by_country.csv'

dados = pd.read_csv(arquivo, sep=',')
print(dados.head())
print(dados.columns)
print(dados.info())
print(dados.describe())

# Ordenando os dados pelos maiores consumos e selecionando os 10 primeiros
top_10_paises = dados.sort_values(by='alcohol', ascending=False).head(10)

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.bar(top_10_paises['location'], top_10_paises['alcohol'], color='skyblue')
plt.title('Top 10 Países com Maior Consumo de Álcool (2010)', fontsize=14)
plt.xlabel('Países', fontsize=12)
plt.ylabel('Consumo de Álcool (litros per capita)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Exibindo o gráfico
plt.show()


