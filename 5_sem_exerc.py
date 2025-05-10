import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dados = pd.read_csv('APPLE_iPhone_SE.csv')
print(dados.tail(10))
print(f'O arquivo tem {len(dados)} linhas e {len(dados.columns)} colunas')
print(dados.describe())
print(dados.info())
print(f' A média das notas é {dados['Ratings'].mean():.2f}')

print(dados['Ratings'].value_counts())

total_notas = dados['Ratings'].value_counts().sum()

# Visualizando a distribuição das notas
sns.histplot(data=dados, x='Ratings', kde=True, bins=5)
plt.xlabel('Notas')
plt.ylabel('Frequência')
plt.title('Distribuição das Notas')
plt.show()

# Percentual de cada nota
percentuais = dados['Ratings'].value_counts(normalize=True) * 100
print(percentuais)