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