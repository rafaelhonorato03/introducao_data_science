import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [1, 2, 3, 4, 2, 6, 7, 8, 9, 10]

plt.scatter(x, y)
plt.show()

x1 = np.arange(-100, 100, 1)

plt.plot(x1, x1**2)
plt.show()

plt.plot(x1, (x1**2) -2000)
plt.show()

dias = np.arange(1, 31)
vacinados = np.random.randint(0, 1000, 30)
contagios = np.random.randint(0, 700, 30)

#plt.style.use('classic')
#plt.style.use('dark_background')
plt.style.use('default')
plt.figure(figsize=(10, 5))
plt.bar(dias, vacinados)
plt.plot(dias, contagios, 'r')
plt.ylabel('Vacinados por dia')
plt.show()

dados = pd.DataFrame(dias, columns=['dias'])
dados['Contagios'] = contagios
dados['Vacinados'] = vacinados

dados.plot(kind='bar', x='dias', y='Vacinados')
plt.show()

## Usando seaborn
sns.barplot(data=dados, x='dias', y='Contagios')
sns.lineplot(data=dados, x='dias', y='Vacinados', color='red')
plt.show()