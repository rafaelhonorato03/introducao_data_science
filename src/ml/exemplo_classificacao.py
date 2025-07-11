import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def baixar_dataset_kaggle():
    # Inicializa a API do Kaggle
    api = KaggleApi()
    api.authenticate()
    
    # Dataset California Housing
    dataset = "rahmadadeakbar/california-housing-train"
    
    print("Baixando dataset...")
    api.dataset_download_files(dataset, path="./dados", unzip=True)
    print("Dataset baixado com sucesso!")
    
    # Lendo o arquivo CSV
    df = pd.read_csv("./dados/california_housing_train.csv")
    print("\nPrimeiras linhas do dataset:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    # Cria a pasta dados se não existir
    import os
    os.makedirs("dados", exist_ok=True)
    
    # Baixa e carrega o dataset
    df = baixar_dataset_kaggle()
    
    # Mostra algumas informações sobre o dataset
    print("\nInformações do dataset:")
    print(df.info()) 