import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Inicializa a API do Kaggle
api = KaggleApi()
api.authenticate()

# Dataset California Housing
dataset = "rahmadadeakbar/california-housing-train"

print("Baixando dataset...")
api.dataset_download_files(dataset, path="./dados", unzip=True)
print("Dataset baixado com sucesso!")

# Lendo o arquivo CSV
dados = pd.read_csv("./dados/california_housing_train.csv")

# Mostrando as primeiras linhas
print("\nPrimeiras linhas do dataset:")
print(dados.head())

# Informações básicas sobre o dataset
print("\nInformações do dataset:")
print(dados.info())

# Estatísticas descritivas
print("\nEstatísticas descritivas:")
print(dados.describe())

# Criando um gráfico de dispersão entre median_house_value e median_income
plt.figure(figsize=(10, 6))
sns.scatterplot(data=dados, x='median_income', y='median_house_value')
plt.title('Relação entre Renda Mediana e Valor Mediano das Casas')
plt.xlabel('Renda Mediana')
plt.ylabel('Valor Mediano das Casas')
plt.show()

# Criando um mapa de calor das correlações
plt.figure(figsize=(10, 8))
sns.heatmap(dados.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Mapa de Correlação entre as Variáveis')
plt.show()

# Iniciando processo de machine learning
y = dados['median_house_value']

# Escolhendo as features
features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
X = dados[features]

modelo = KNeighborsRegressor(3)
modelo.fit(X, y)
print(dados.head())
print(X.head())

modelo.predict(X.head(5))
predicao = modelo.predict(X)

print(predicao)

mean = mean_absolute_error(y, predicao)
print(mean)

treino_x, validacao_x, treino_y, validacao_y = train_test_split(X, y, test_size=0.8, random_state=1)
treino_x.shape

modelo_2 = KNeighborsRegressor(3)
modelo_2.fit(treino_x, treino_y)
predicao_2 = modelo_2.predict(validacao_x)
