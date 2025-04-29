import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sweetviz as sv


# Gerando dados fictícios
minutos_por_dia = np.random.randint(0, 60, 30)
print(minutos_por_dia)

# Plotando os dados

ax = sns.histplot(minutos_por_dia)
ax.set(xlabel='Minutos por dia',
       ylabel='Frequência')
plt.show()

# Carregando dados de um csv do Github
arquivo = 'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2021.csv'
dados = pd.read_csv(arquivo, sep=',')
print(dados.head())
print(dados.columns)
print(dados.info())

# Plotando os dados
#eda = sv.analyze(dados)
#eda.show_html('eda.html') - Esta dando erro, pois a versão não é compatível com o Nunpy

# Analise de correlação de Pearson
mask = np.triu(np.ones_like(dados.corr(), dtype=bool))
plt.figure(figsize=(20, 20))
sns.heatmap(dados.corr(), mask=mask, cmap='coolwarm', annot=True, fmt='.2f')
plt.show()