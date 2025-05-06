from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

dados = pd.DataFrame({
    'idade': [25, 34, 22, 45, 52, 23, 40, 60, 48, 33],
    'renda': [5000, 7000, 3000, 10000, 12000, 3200, 9500, 15000, 11000, 6500]
})

# KMeans com 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
dados['cluster'] = kmeans.fit_predict(dados)
print(dados)

# Visualização
plt.scatter(dados['idade'], dados['renda'], c=dados['cluster'], cmap='viridis')
plt.xlabel('Idade')
plt.ylabel('Renda')
plt.title('Agrupamento de Clientes')
plt.show()

# Área (m²) e preços (mil R$)
area = np.array([50, 60, 70, 80, 100]).reshape(-1, 1)
preco = np.array([150, 180, 210, 240, 300])

# Modelo de regressão
modelo = LinearRegression()
modelo.fit(area, preco)

# Previsão
nova_area = np.array([[90]])
previsao = modelo.predict(nova_area)

print(f'Preço previsto para casa com 90m²: R${previsao[0]:.2f} mil')

# Visualização
plt.scatter(area, preco, color='blue')
plt.plot(area, modelo.predict(area), color='red')
plt.scatter(nova_area, previsao, color='green', marker='x')
plt.xlabel('Área (m²)')
plt.ylabel('Preço (mil R$)')
plt.title('Regressão Linear: Área vs Preço')
plt.show()