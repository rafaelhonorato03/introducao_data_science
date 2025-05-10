import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sweetviz as sv

df = pd.read_csv('mcu dataset.csv')
print(df.head())

correlacao = df.select_dtypes(include='number').corr()
print(correlacao)

sns.heatmap(correlacao, annot=True, cmap='coolwarm')
plt.title('Correlação entre variáveis numéricas')
plt.tight_layout()
plt.show()

