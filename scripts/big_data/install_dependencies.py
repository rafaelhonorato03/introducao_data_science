#!/usr/bin/env python3
# ==========================================
# SCRIPT DE INSTALAÇÃO DE DEPENDÊNCIAS
# ==========================================
# Instala automaticamente todas as dependências necessárias

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        print(f"Comando: {command}")
        print(f"Erro: {e.stderr}")
        return False

def install_package(package, description=None):
    """Instala um pacote Python"""
    if description is None:
        description = f"Instalando {package}"
    
    return run_command(f"{sys.executable} -m pip install {package}", description)

def download_spacy_model(model, description=None):
    """Baixa um modelo spaCy"""
    if description is None:
        description = f"Baixando modelo spaCy {model}"
    
    return run_command(f"{sys.executable} -m spacy download {model}", description)

def main():
    """Função principal de instalação"""
    
    print("🚀 INSTALADOR DE DEPENDÊNCIAS - ANALISADOR DE PERSONAGENS")
    print("=" * 60)
    print()
    
    # Verifica se pip está disponível
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip não está disponível. Instale o pip primeiro.")
        return False
    
    # Lista de pacotes básicos
    basic_packages = [
        "pandas>=1.3.0",
        "numpy>=1.21.0", 
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "scikit-learn>=1.0.0"
    ]
    
    # Lista de pacotes para PDFs
    pdf_packages = [
        "PyPDF2>=3.0.0",
        "PyMuPDF>=1.18.0"
    ]
    
    # Lista de pacotes para NLP
    nlp_packages = [
        "spacy>=3.4.0",
        "textblob>=0.17.0"
    ]
    
    # Lista de pacotes para análises avançadas
    advanced_packages = [
        "networkx>=2.6.0"
    ]
    
    # Lista de pacotes para interface web
    web_packages = [
        "streamlit>=1.20.0",
        "plotly>=5.0.0"
    ]
    
    # Lista de pacotes opcionais
    optional_packages = [
        "nltk>=3.6.0",
        "wordcloud>=1.8.0",
        "transformers>=4.20.0",
        "torch>=1.12.0",
        "bokeh>=2.4.0",
        "holoviews>=1.15.0",
        "python-dateutil>=2.8.0",
        "openpyxl>=3.0.0",
        "xlsxwriter>=3.0.0"
    ]
    
    print("📦 Instalando pacotes básicos...")
    for package in basic_packages:
        if not install_package(package):
            print(f"⚠️ Falha ao instalar {package}, continuando...")
    
    print("\n📄 Instalando pacotes para análise de PDFs...")
    for package in pdf_packages:
        if not install_package(package):
            print(f"⚠️ Falha ao instalar {package}, continuando...")
    
    print("\n🧠 Instalando pacotes para NLP...")
    for package in nlp_packages:
        if not install_package(package):
            print(f"⚠️ Falha ao instalar {package}, continuando...")
    
    print("\n🔬 Instalando pacotes para análises avançadas...")
    for package in advanced_packages:
        if not install_package(package):
            print(f"⚠️ Falha ao instalar {package}, continuando...")
    
    print("\n🌐 Instalando pacotes para interface web...")
    for package in web_packages:
        if not install_package(package):
            print(f"⚠️ Falha ao instalar {package}, continuando...")
    
    print("\n📚 Instalando pacotes opcionais...")
    for package in optional_packages:
        if not install_package(package):
            print(f"⚠️ Falha ao instalar {package}, continuando...")
    
    print("\n🤖 Baixando modelos spaCy...")
    
    # Tenta baixar modelo português
    if not download_spacy_model("pt_core_news_sm", "Baixando modelo spaCy português"):
        print("⚠️ Falha ao baixar modelo português, tentando modelo multilíngue...")
        if not download_spacy_model("xx_ent_wiki_sm", "Baixando modelo spaCy multilíngue"):
            print("⚠️ Falha ao baixar modelos spaCy. Execute manualmente:")
            print("python -m spacy download pt_core_news_sm")
            print("ou")
            print("python -m spacy download xx_ent_wiki_sm")
    
    print("\n📥 Baixando dados do NLTK...")
    try:
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        print("✅ Dados do NLTK baixados com sucesso!")
    except ImportError:
        print("⚠️ NLTK não está disponível, pulando download de dados...")
    except Exception as e:
        print(f"⚠️ Erro ao baixar dados do NLTK: {e}")
    
    print("\n" + "=" * 60)
    print("✅ INSTALAÇÃO CONCLUÍDA!")
    print("=" * 60)
    
    print("\n🚀 Como usar:")
    print("1. Para análise básica:")
    print("   python scripts/big_data/analise_pdf_ner.py")
    
    print("\n2. Para interface web:")
    print("   streamlit run scripts/big_data/app_streamlit.py")
    
    print("\n3. Para testar com um PDF:")
    print("   - Coloque um PDF na pasta 'dados/'")
    print("   - Execute o script de análise")
    
    print("\n📚 Recursos disponíveis:")
    print("- Identificação de personagens com NER")
    print("- Análise de coocorrência entre personagens")
    print("- Análise de sentimentos por personagem")
    print("- Análise temporal por capítulos")
    print("- Visualizações interativas")
    print("- Interface web com Streamlit")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 