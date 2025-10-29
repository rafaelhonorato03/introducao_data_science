import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

caminho = r'data\raw\Birthweight_reduced_kg_R.csv'

df = pd.read_csv(caminho)
print(df)

print(df.info())
print(df.describe())

sns.boxplot(data= df, hue= 'smoker', y= 'Length')
plt.show()

sns.boxplot(data= df, hue= 'smoker', y= 'Birthweight')
plt.show()

sns.boxplot(data= df, y= 'mage')
plt.show()

sns.scatterplot(data=df, x = 'Gestation', y='Birthweight', hue='smoker')
plt.show()

sns.scatterplot(data=df, x = 'Birthweight', y='Length', hue='smoker')
plt.show()

altura = df['Length'].mean()
desvio = df['Length'].std()

print(f'A média das alturas é: {altura: .2f}, com um desvio de: {desvio: .2f}.')