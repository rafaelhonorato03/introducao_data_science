#!/usr/bin/env python3
"""
Script de configuração para o Analisador de Personagens
Instala todas as dependências necessárias
"""

import subprocess
import sys
import os

def instalar_dependencias():
    """Instala todas as dependências necessárias"""
    
    print("🔧 Instalando dependências...")
    
    # Lista de dependências
    dependencias = [
        "streamlit>=1.28.0",
        "spacy>=3.7.0", 
        "PyMuPDF>=1.23.0",
        "pandas>=2.0.0",
        "seaborn>=0.12.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
        "leia>=0.1.0",
        "networkx>=3.1",
        "pyvis>=0.3.2",
        "tqdm>=4.65.0",
        "python-louvain>=0.16",
        "scikit-learn>=1.3.0"
    ]
    
    for dep in dependencias:
        print(f"📦 Instalando {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar {dep}: {e}")
            return False
    
    return True

def baixar_modelos_spacy():
    """Baixa os modelos do Spacy necessários"""
    
    print("\n🤖 Baixando modelos do Spacy...")
    
    modelos = ["pt_core_news_sm", "en_core_web_sm"]
    
    for modelo in modelos:
        print(f"📥 Baixando modelo {modelo}...")
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", modelo])
            print(f"✅ Modelo {modelo} baixado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Erro ao baixar {modelo}: {e}")
            print("   O modelo será baixado automaticamente quando necessário.")

def verificar_instalacao():
    """Verifica se tudo foi instalado corretamente"""
    
    print("\n🔍 Verificando instalação...")
    
    modulos = [
        "streamlit", "spacy", "fitz", "pandas", "seaborn", 
        "matplotlib", "numpy", "leia", "networkx", "pyvis", 
        "tqdm", "community", "sklearn"
    ]
    
    for modulo in modulos:
        try:
            __import__(modulo)
            print(f"✅ {modulo} - OK")
        except ImportError:
            print(f"❌ {modulo} - FALHOU")
            return False
    
    return True

def main():
    """Função principal"""
    
    print("🚀 Configurando Analisador de Personagens...")
    print("=" * 50)
    
    # Instalar dependências
    if not instalar_dependencias():
        print("❌ Falha na instalação das dependências!")
        sys.exit(1)
    
    # Baixar modelos Spacy
    baixar_modelos_spacy()
    
    # Verificar instalação
    if not verificar_instalacao():
        print("❌ Algumas dependências não foram instaladas corretamente!")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Configuração concluída com sucesso!")
    print("\n📋 Para executar o aplicativo:")
    print("   cd scripts/big_data")
    print("   streamlit run app.py")
    print("\n🌐 O aplicativo estará disponível em: http://localhost:8501")

if __name__ == "__main__":
    main() 