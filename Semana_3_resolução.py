import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests
import json
import seaborn as sns

url = 'https://db-engines.com/en/ranking'
html = requests.get(url).content
soup = bs(html, 'html5lib')

# Buscando tabelas
tabela = soup.find('table', {'class': 'dbi'}).find('tbody')
print(tabela)

# Buscando linhas da tabela
linhas=tabela.find_all('tr')
contalinhas=0
banco=[]
pontos=[]
for linha in linhas:
    contalinhas+=1
    if contalinhas>3:
        dado=linha.find_all('td')
        dado2=linha.find('a')
        pontos.append(float(dado[3].text))
        #ao pegar o dado do link, veja que ele monta um array com as informações, onde a primeira (0) é o nome do banco
        banco.append(dado2.contents[0])

dados=pd.DataFrame(banco,columns=['Banco'])
dados['Pontos']=pontos
print(dados)

sns.barplot(data=dados.head(4), x='Banco', y='Pontos')
plt.show()

dados_ex4=dados.head(10)

total=dados_ex4['Pontos'].sum()
dados_ex4['Share']=dados_ex4['Pontos']/total*100
print(dados_ex4)

plt.pie(dados_ex4['Share'],labels=dados_ex4['Banco'])
plt.show()

dados.to_csv("db-ranking.csv")


# Dados públicos JSON
site="https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='09-16-2008'&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"
resposta=requests.get(site)
dados=json.loads(resposta.text)
print(dados)
print(dados['value'][0]['cotacaoVenda'])