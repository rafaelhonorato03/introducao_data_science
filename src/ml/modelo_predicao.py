import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib
matplotlib.use('Agg')  # Adicione esta linha ANTES de importar pyplot

# 1. Função para download e carregamento dos dados
def carregar_dados(dataset_name, path="./dados"):
    api = KaggleApi()
    api.authenticate()
    
    try:
        print("Baixando dataset...")
        api.dataset_download_files(dataset_name, path=path, unzip=True)
        print("Dataset baixado com sucesso!")
        return pd.read_csv(f"{path}/california_housing_train.csv")
    except Exception as e:
        print(f"Erro ao baixar dados: {e}")
        return None

# 2. Função para análise exploratória
def analise_exploratoria(dados):
    print("\nInformações do dataset:")
    print(dados.info())
    print("\nEstatísticas descritivas:")
    print(dados.describe())
    
    # Visualizações
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=dados, x='median_income', y='median_house_value')
    plt.title('Relação entre Renda Mediana e Valor Mediano das Casas')
    plt.savefig('scatter_income_vs_value.png')
    plt.close()
    
    # Correlações
    plt.figure(figsize=(10, 8))
    sns.heatmap(dados.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Mapa de Correlação entre as Variáveis')
    plt.savefig('correlation_heatmap.png')
    plt.close()

# 3. Função para pré-processamento
def preprocessar_dados(dados):
    from sklearn.preprocessing import StandardScaler
    
    # Tratando valores nulos
    dados['total_bedrooms'].fillna(dados['total_bedrooms'].mean(), inplace=True)
    
    # Criando features derivadas
    dados['rooms_per_household'] = dados['total_rooms'] / dados['households']
    dados['population_per_household'] = dados['population'] / dados['households']
    
    # Normalizando features
    scaler = StandardScaler()
    features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 
                'total_bedrooms', 'population', 'households', 'median_income',
                'rooms_per_household', 'population_per_household']
    
    dados[features] = scaler.fit_transform(dados[features])
    return dados, features

# 4. Função para treinar e avaliar modelos
def treinar_avaliar_modelos(X, y):
    from sklearn.model_selection import cross_val_score
    from sklearn.metrics import mean_squared_error, r2_score
    import numpy as np
    
    # Divisão treino/teste mais adequada
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    
    # Dicionário para armazenar os modelos
    modelos = {
        'KNN': KNeighborsRegressor(n_neighbors=3),
        'DecisionTree': DecisionTreeRegressor(random_state=1, max_depth=8),
        'RandomForest': RandomForestRegressor(random_state=1, n_jobs=-1, n_estimators=500)
    }
    
    resultados = {}
    
    for nome, modelo in modelos.items():
        # Cross-validation
        cv_scores = cross_val_score(modelo, X_train, y_train, cv=5)
        
        # Treinamento final
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        
        # Métricas
        resultados[nome] = {
            'CV_Score': cv_scores.mean(),
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'R2': r2_score(y_test, y_pred)
        }
        
        # Plotando resultados
        plot_resultados(y_test, y_pred, nome)
        
        if nome == 'RandomForest':
            plot_importancia_features(modelo, features)
    
    return resultados, modelos

# 5. Função para visualizar resultados
def plot_resultados(y_true, y_pred, modelo_nome):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('Valores Reais')
    plt.ylabel('Previsões')
    plt.title(f'Previsões vs Valores Reais - {modelo_nome}')
    plt.savefig(f'previsoes_vs_reais_{modelo_nome}.png')
    plt.close()
    
    # Plot de resíduos
    residuos = y_pred - y_true
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuos, alpha=0.5)
    plt.xlabel('Previsões')
    plt.ylabel('Resíduos')
    plt.title(f'Análise de Resíduos - {modelo_nome}')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.savefig(f'analise_de_residuos_{modelo_nome}.png')
    plt.close()

# 6. Função para plotar importância das features
def plot_importancia_features(modelo, features):
    importancia = pd.DataFrame({
        'feature': features,
        'importancia': modelo.feature_importances_
    }).sort_values('importancia', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=importancia, x='importancia', y='feature')
    plt.title('Importância das Features - Random Forest')
    plt.savefig('importancia_features_random_forest.png')
    plt.close()

# 7. Função para salvar o melhor modelo
def salvar_modelo(modelo, nome_arquivo):
    import joblib
    joblib.dump(modelo, f'{nome_arquivo}.joblib')

# Função principal
def main():
    # Carregando dados
    dados = carregar_dados("rahmadadeakbar/california-housing-train")
    if dados is None:
        return
    
    # Análise exploratória
    analise_exploratoria(dados)
    
    # Pré-processamento
    dados_prep, features = preprocessar_dados(dados)
    
    # Separando features e target
    X = dados_prep[features]
    y = dados_prep['median_house_value']
    
    # Treinamento e avaliação
    resultados, modelos = treinar_avaliar_modelos(X, y)
    
    # Imprimindo resultados
    print("\nResultados dos Modelos:")
    for modelo, metricas in resultados.items():
        print(f"\n{modelo}:")
        for metrica, valor in metricas.items():
            print(f"{metrica}: {valor:.4f}")
    
    # Salvando o melhor modelo (Random Forest)
    salvar_modelo(modelos['RandomForest'], 'modelo_california_housing')

if __name__ == "__main__":
    main()
