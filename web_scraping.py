import requests
from bs4 import BeautifulSoup
import pandas as pd

html = requests.get("https://statisticstimes.com/tech/top-computer-languages.php").content
soup = BeautifulSoup(html, "html5lib")

# Buscando paragrafos
primeiros_paragrafos = soup.find_all('p')
for paragrafo in primeiros_paragrafos:
    print(paragrafo.text)

# Buscando Links
todos_links = soup.find_all('a')
for link in todos_links:
    print(link.get('href'))

# Buscando tabelas
tabela = soup.find('table', {'id': 'table_id1'}).find('tbody')
print(tabela)

# Buscando linhas da tabela
linhas = tabela.find_all('tr')
for linha in linhas:
    dados = linha.find_all('td')
    print(dados[0].text)
    print(dados[1].text)
    print(dados[2].text)
    print('------------------')

# Criando um DataFrame com os dados da tabela
linguagens = []
pontos = []
for linha in linhas:
    dados = linha.find_all('td')
    linguagens.append(dados[2].text)
    pontos.append(dados[3].text)

print(linguagens)
print(pontos)

df = pd.DataFrame({'Linguagem': linguagens, 'Pontos': pontos})
print(df)
df.to_csv('linguagens.csv', index=False)