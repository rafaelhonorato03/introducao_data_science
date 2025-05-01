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
# Seleciona apenas colunas numéricas
dados_numericos = dados.select_dtypes(include=[np.number])

# Agora sim calcula a máscara da correlação
mask = np.triu(np.ones_like(dados_numericos.corr(), dtype=bool))

plt.figure(figsize=(12, 8))
sns.heatmap(dados_numericos.corr(),
            mask=mask,
            square=True,
            cmap='coolwarm',
            annot=False,
            fmt='.2f')
plt.tight_layout()
plt.show()

# Analise exploratória
print(dados.describe(include='all'))
print(dados.isnull())
print(dados.isnull().sum())

# Analisando uma coluna
print(dados['winner_entry'].value_counts())
print(dados['winner_entry'].unique())

dados.dropna(subset=['loser_entry'], inplace=True)
dados.dropna(axis=1, how= 'all')

print(dados['winner_entry'].unique())
dados['winner_entry'].fillna(value= 'x', inplace=True) #substituindo por x
print(dados['winner_entry'].unique())

dados['w_ace'].unique()
dados['loser_ht'].unique()

dados.fillna(value={'w_ace': 0,
                    'loser_ht': dados['loser_ht'].mean()},
                    inplace=True) #substituindo por 0 e pela média

dados['w_ace'].unique()
dados['loser_ht'].unique()
