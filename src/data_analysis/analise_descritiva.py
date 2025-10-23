from tkinter import X
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Dados retirados de: https://dados.educacao.sp.gov.br/dataset/quantidade-de-alunos-por-tipo-de-ensino-da-rede-estadual

fonte = r'C:\Users\tabat\Documents\GitHub\introducao_data_science\data\raw\Quantidade de alunos por tipo de ensino da rede estadual_2023_2°SEMESTRE.csv'

df = pd.read_csv(fonte, sep=';')
print(df.head())

df.info()
print(df.describe())

# Analisando Ensino Médio
total_ensino_medio = df['ENSINO MEDIO'].sum()
print(f'Temos no ensino Médio um total de: {total_ensino_medio:.0f} matrículas')

filtro_escolas= df[df['ENSINO MEDIO'] > 0]
sns.displot(filtro_escolas['ENSINO MEDIO'])
plt.show()

# Analisando Anos Iniciais
total_ensino_anos_iniciais = df['ANOS INICIAIS'].sum()
print(f'Temos no anos inciais um total de: {total_ensino_anos_iniciais:.0f} matrículas')

filtro_escolas = df[df['ANOS INICIAIS'] > 0]
sns.displot(filtro_escolas['ANOS INICIAIS'])
plt.show()

# Agrupamento
alunos = [total_ensino_medio, total_ensino_anos_iniciais]
periodo = ['Ensino Médio', 'Anos Iniciais']

sns.catplot(x=alunos, y=periodo, kind='bar')
plt.show()

sns.stripplot(x=total_ensino_medio, y=total_ensino_anos_iniciais, hue=periodo)
plt.show()