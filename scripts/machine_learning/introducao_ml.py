from sklearn import datasets
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

iris = datasets.load_iris()

# Importando o dataset
df = pd.DataFrame(iris.data, columns=iris.feature_names)
print(df.head())

# Criando alvo
df['target'] = iris.target
print(df.head())

# Criando um target names#
iris.target_names
df['target_names'] = iris.target_names[df['target']]
print(df.head())

# Determinar Features
iris_features = ['sepal length (cm)',
                 'sepal width (cm)',
                 'petal length (cm)',
                 'petal width (cm)'
                 ]

y = df.target

X = df[iris_features]
print(X.head())
print(y.head())

# Usando Scikit-learn para criar um modelo KNN
# Define - Escolhe um modelo e define parâmetro
# Fit - Treina o modelo
# Predict - Faz previsões
# Evaluate - Avalia o modelo

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X, y)
print(X.head())
print(modelo.predict(X))

print(modelo.score(X, y))