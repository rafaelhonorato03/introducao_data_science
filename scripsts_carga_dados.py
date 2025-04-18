import csv
import pandas as pd

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

