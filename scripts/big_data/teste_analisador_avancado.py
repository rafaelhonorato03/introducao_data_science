#!/usr/bin/env python3
# ==========================================
# SCRIPT DE TESTE DO ANALISADOR AVANÇADO
# ==========================================
# Testa todas as funcionalidades implementadas

import sys
import os
from pathlib import Path
import json

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todas as dependências estão disponíveis"""
    print("🔍 Testando importações...")
    
    try:
        import pandas as pd
        print("✅ pandas")
    except ImportError:
        print("❌ pandas")
        return False
    
    try:
        import numpy as np
        print("✅ numpy")
    except ImportError:
        print("❌ numpy")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib")
    except ImportError:
        print("❌ matplotlib")
        return False
    
    try:
        import networkx as nx
        print("✅ networkx")
    except ImportError:
        print("❌ networkx")
        return False
    
    try:
        from textblob import TextBlob
        print("✅ textblob")
    except ImportError:
        print("❌ textblob")
        return False
    
    try:
        import spacy
        print("✅ spacy")
    except ImportError:
        print("❌ spacy")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit")
    except ImportError:
        print("❌ streamlit")
        return False
    
    try:
        import plotly.express as px
        print("✅ plotly")
    except ImportError:
        print("❌ plotly")
        return False
    
    return True

def test_analisador_import():
    """Testa se o analisador pode ser importado"""
    print("\n🔍 Testando importação do analisador...")
    
    try:
        from analise_pdf_ner import AnalisadorPDFNER
        print("✅ AnalisadorPDFNER importado com sucesso")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar AnalisadorPDFNER: {e}")
        return False

def test_analisador_initialization():
    """Testa a inicialização do analisador"""
    print("\n🔍 Testando inicialização do analisador...")
    
    try:
        from analise_pdf_ner import AnalisadorPDFNER
        analisador = AnalisadorPDFNER()
        print("✅ Analisador inicializado com sucesso")
        
        # Verifica se as variáveis estão definidas
        assert hasattr(analisador, 'texto_completo')
        assert hasattr(analisador, 'freq_personagens')
        assert hasattr(analisador, 'capitulos')
        assert hasattr(analisador, 'analise_sentimentos')
        assert hasattr(analisador, 'rede_personagens')
        assert hasattr(analisador, 'coocorrencias')
        assert hasattr(analisador, 'analise_temporal')
        
        print("✅ Todas as variáveis de análise estão definidas")
        return True
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        return False

def test_text_processing():
    """Testa o processamento de texto"""
    print("\n🔍 Testando processamento de texto...")
    
    try:
        from analise_pdf_ner import AnalisadorPDFNER
        analisador = AnalisadorPDFNER()
        
        # Texto de teste
        texto_teste = """
        José Gabriel era um homem simples que vivia na cidade. Maria Clara, sua esposa, sempre o apoiava.
        Pedro Santos, o vizinho, frequentemente visitava a família. Ana Beatriz, filha de José Gabriel e Maria Clara,
        adorava brincar com Carlos Eduardo, filho de Pedro Santos. Dona Rosa Silva, a professora de Ana Beatriz,
        sempre elogiava seu comportamento. Dr. João Silva, o médico da família, era muito atencioso.
        José Gabriel trabalhava com Sr. Antônio Santos na loja. Maria Clara conversava com Dona Clara Costa na feira.
        Pedro Santos e Carlos Eduardo iam pescar com Tio José Pereira. Ana Beatriz estudava com sua amiga Beatriz Oliveira.
        """
        
        # Simula extração de texto
        analisador.texto_completo = texto_teste
        
        # Testa divisão em capítulos
        capitulos = analisador.dividir_em_capitulos()
        print(f"✅ Divisão em capítulos: {len(capitulos)} seções criadas")
        
        # Testa identificação de personagens
        if analisador.nlp:
            personagens = analisador.identificar_personagens_ner()
            print(f"✅ Identificação de personagens: {len(personagens)} encontrados")
        else:
            print("⚠️ spaCy não disponível, pulando teste de NER")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no processamento de texto: {e}")
        return False

def test_advanced_analysis():
    """Testa as análises avançadas"""
    print("\n🔍 Testando análises avançadas...")
    
    try:
        from analise_pdf_ner import AnalisadorPDFNER
        analisador = AnalisadorPDFNER()
        
        # Texto de teste com personagens
        texto_teste = """
        José Gabriel era um homem simples que vivia na cidade. Maria Clara, sua esposa, sempre o apoiava.
        Pedro Santos, o vizinho, frequentemente visitava a família. Ana Beatriz, filha de José Gabriel e Maria Clara,
        adorava brincar com Carlos Eduardo, filho de Pedro Santos. Dona Rosa Silva, a professora de Ana Beatriz,
        sempre elogiava seu comportamento. Dr. João Silva, o médico da família, era muito atencioso.
        José Gabriel trabalhava com Sr. Antônio Santos na loja. Maria Clara conversava com Dona Clara Costa na feira.
        Pedro Santos e Carlos Eduardo iam pescar com Tio José Pereira. Ana Beatriz estudava com sua amiga Beatriz Oliveira.
        José Gabriel, Maria Clara, Pedro Santos, Ana Beatriz, Carlos Eduardo, Dona Rosa Silva, Dr. João Silva, 
        Sr. Antônio Santos, Dona Clara Costa, Tio José Pereira e Beatriz Oliveira formavam uma comunidade unida.
        """
        
        analisador.texto_completo = texto_teste
        
        # Simula personagens identificados
        analisador.freq_personagens = {
            'José Gabriel': 5,
            'Maria Clara': 4,
            'Pedro Santos': 3,
            'Ana Beatriz': 3,
            'Carlos Eduardo': 2,
            'Dona Rosa Silva': 2,
            'Dr. João Silva': 2,
            'Sr. Antônio Santos': 1,
            'Dona Clara Costa': 1,
            'Tio José Pereira': 1,
            'Beatriz Oliveira': 1
        }
        
        # Testa análise de coocorrências
        coocorrencias = analisador.analisar_coocorrencias(janela_palavras=50)
        print(f"✅ Análise de coocorrências: {len(coocorrencias)} personagens analisados")
        
        # Testa criação da rede
        rede = analisador.criar_rede_personagens()
        if rede:
            print(f"✅ Rede de personagens: {rede.number_of_nodes()} nós, {rede.number_of_edges()} arestas")
        
        # Testa análise de sentimentos
        sentimentos = analisador.analisar_sentimentos_personagens()
        print(f"✅ Análise de sentimentos: {len(sentimentos)} personagens analisados")
        
        # Testa análise por capítulos
        temporal = analisador.analisar_personagens_por_capitulo()
        print(f"✅ Análise temporal: {len(temporal)} capítulos analisados")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas análises avançadas: {e}")
        return False

def test_visualizations():
    """Testa a criação de visualizações"""
    print("\n🔍 Testando criação de visualizações...")
    
    try:
        from analise_pdf_ner import AnalisadorPDFNER
        analisador = AnalisadorPDFNER()
        
        # Simula dados para visualização
        analisador.freq_personagens = {
            'José Gabriel': 5,
            'Maria Clara': 4,
            'Pedro Santos': 3,
            'Ana Beatriz': 3,
            'Carlos Eduardo': 2
        }
        
        # Testa gráfico de frequência
        fig_freq = analisador.criar_grafico_frequencia(5)
        if fig_freq:
            print("✅ Gráfico de frequência criado")
        
        # Testa gráfico de dispersão
        analisador.texto_completo = "José Gabriel era um homem simples. Maria Clara, sua esposa. Pedro Santos, o vizinho."
        fig_disp = analisador.criar_grafico_dispersao(5)
        if fig_disp:
            print("✅ Gráfico de dispersão criado")
        
        # Testa rede de personagens
        analisador.coocorrencias = {
            'José Gabriel': {'Maria Clara': 2, 'Pedro Santos': 1},
            'Maria Clara': {'José Gabriel': 2, 'Ana Beatriz': 1},
            'Pedro Santos': {'José Gabriel': 1, 'Carlos Eduardo': 1}
        }
        analisador.criar_rede_personagens()
        fig_rede = analisador.visualizar_rede_personagens()
        if fig_rede:
            print("✅ Visualização da rede criada")
        
        # Testa gráfico de sentimentos
        analisador.analise_sentimentos = {
            'José Gabriel': {'media': 0.2, 'positivo': 3, 'negativo': 1, 'neutro': 1, 'total_contextos': 5},
            'Maria Clara': {'media': 0.1, 'positivo': 2, 'negativo': 1, 'neutro': 1, 'total_contextos': 4}
        }
        fig_sent = analisador.criar_grafico_sentimentos()
        if fig_sent:
            print("✅ Gráfico de sentimentos criado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na criação de visualizações: {e}")
        return False

def test_report_generation():
    """Testa a geração de relatórios"""
    print("\n🔍 Testando geração de relatórios...")
    
    try:
        from analise_pdf_ner import AnalisadorPDFNER
        analisador = AnalisadorPDFNER()
        
        # Simula dados completos
        analisador.texto_completo = "Texto de teste com personagens."
        analisador.freq_personagens = {'José Gabriel': 5, 'Maria Clara': 4}
        analisador.capitulos = [{'numero': 1, 'titulo': 'Capítulo 1', 'texto': 'Texto do capítulo'}]
        analisador.analise_sentimentos = {'José Gabriel': {'media': 0.2}}
        analisador.coocorrencias = {'José Gabriel': {'Maria Clara': 2}}
        
        # Testa geração de relatório
        relatorio = analisador.gerar_relatorio_completo()
        
        if relatorio and 'metadata' in relatorio:
            print("✅ Relatório completo gerado")
            print(f"   - Personagens: {relatorio['personagens']['total_identificados']}")
            print(f"   - Capítulos: {relatorio['metadata']['total_capitulos']}")
        else:
            print("❌ Erro na geração do relatório")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na geração de relatórios: {e}")
        return False

def test_streamlit_app():
    """Testa se a aplicação Streamlit pode ser importada"""
    print("\n🔍 Testando aplicação Streamlit...")
    
    try:
        # Tenta importar a aplicação
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Verifica se o arquivo existe
        app_file = Path("app_streamlit.py")
        if app_file.exists():
            print("✅ Arquivo da aplicação Streamlit encontrado")
            
            # Tenta importar funções principais
            try:
                from app_streamlit import main, exibir_resultados, exibir_pagina_inicial
                print("✅ Funções da aplicação Streamlit importadas")
                return True
            except ImportError as e:
                print(f"⚠️ Erro ao importar funções: {e}")
                return False
        else:
            print("❌ Arquivo da aplicação Streamlit não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste da aplicação Streamlit: {e}")
        return False

def main():
    """Função principal de teste"""
    
    print("🧪 TESTE COMPLETO DO ANALISADOR AVANÇADO")
    print("=" * 50)
    
    # Lista de testes
    testes = [
        ("Importações", test_imports),
        ("Importação do Analisador", test_analisador_import),
        ("Inicialização", test_analisador_initialization),
        ("Processamento de Texto", test_text_processing),
        ("Análises Avançadas", test_advanced_analysis),
        ("Visualizações", test_visualizations),
        ("Geração de Relatórios", test_report_generation),
        ("Aplicação Streamlit", test_streamlit_app)
    ]
    
    # Executa testes
    resultados = []
    for nome, teste in testes:
        print(f"\n{'='*20} {nome} {'='*20}")
        try:
            resultado = teste()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro inesperado em {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo dos resultados
    print(f"\n{'='*50}")
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    sucessos = 0
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
        if resultado:
            sucessos += 1
    
    print(f"\nTotal: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("\n🎉 TODOS OS TESTES PASSARAM! O analisador está funcionando perfeitamente.")
        print("\n🚀 Próximos passos:")
        print("1. Execute: python scripts/big_data/analise_pdf_ner.py")
        print("2. Ou inicie a interface web: streamlit run scripts/big_data/app_streamlit.py")
    else:
        print(f"\n⚠️ {len(resultados) - sucessos} teste(s) falharam. Verifique as dependências.")
        print("\n💡 Dica: Execute o script de instalação:")
        print("python scripts/big_data/install_dependencies.py")
    
    return sucessos == len(resultados)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 