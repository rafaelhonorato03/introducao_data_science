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

print(dados['minutes'][1975:1973])
dados['minutes'] = dados['minutes'].ffill() #preenchendo os valores nulos com o valor anterior
print(dados['minutes'][1975:1973])

print(dados.duplicated())
print(dados.duplicated().sum())

dados.drop_duplicates(subset=['tourney_name'], inplace=True) #removendo duplicados
print(dados.duplicated().sum())
print(dados['tourney_name'].unique())

# Deslocamento de dados

dados2 = pd.read_csv("TSLA.csv", sep=",")
print(dados2.head())
print(dados2.columns)
print(dados2.info())
print(dados2.describe())

dados2['close_yesterday'] = dados2['Close'].shift(1) #deslocando os dados para baixo
print(dados2.head(10))

dados2['delta%'] = (dados2['Close']/ dados2['close_yesterday'] - 1)*100 #calculando a variação percentual
print(dados2.head(10))

dados2.dropna(inplace=True) #removendo os valores nulos
print(dados2.head(10))

# Transformando dados categóricos em numéricos
print(dados['winner_ioc'].unique()) #mostrando os dados únicos

# Algoritmo de Machine Learning - Label Encoder
from sklearn.preprocessing import LabelEncoder
paises = dados['winner_ioc']
print(paises)

lencoder = LabelEncoder()
paises_numero = lencoder.fit_transform(paises) #transformando os dados categóricos em numéricos
print(paises_numero)

dados['paises_numero'] = paises_numero #adicionando a nova coluna ao dataframe
print(dados.head(10))
