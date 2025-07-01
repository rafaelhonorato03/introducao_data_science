#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Streamlit para Análise de Personagens em PDFs
Interface web simples e intuitiva para análise de personagens
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os
from analise_personagens_pdf import AnalisadorPDF

# Configuração da página
st.set_page_config(
    page_title="Análise de Personagens em PDFs",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """
    Função principal do app Streamlit
    """
    # Título principal
    st.title("📚 Análise de Personagens em PDFs")
    st.markdown("---")
    
    # Sidebar com configurações
    st.sidebar.header("⚙️ Configurações")
    
    # Seleção de modo de análise
    modo_analise = st.sidebar.selectbox(
        "Modo de Análise",
        ["Rápida (Recomendado)", "Equilibrada", "Completa"],
        help="Escolha o modo baseado no tamanho do seu PDF"
    )
    
    # Configurações baseadas no modo
    if modo_analise == "Rápida (Recomendado)":
        max_palavras = 25000
        max_personagens = 200
        amostra_texto = True
        descricao = "Ideal para arquivos grandes (> 200 páginas)"
    elif modo_analise == "Equilibrada":
        max_palavras = 50000
        max_personagens = 500
        amostra_texto = True
        descricao = "Ideal para arquivos médios (50-200 páginas)"
    else:  # Completa
        max_palavras = 100000
        max_personagens = 1000
        amostra_texto = False
        descricao = "Ideal para arquivos pequenos (< 50 páginas)"
    
    st.sidebar.info(f"**{modo_analise}**: {descricao}")
    
    # Configurações avançadas
    with st.sidebar.expander("🔧 Configurações Avançadas"):
        max_palavras = st.slider("Máximo de palavras", 10000, 200000, max_palavras, 5000)
        max_personagens = st.slider("Máximo de personagens", 100, 2000, max_personagens, 100)
        amostra_texto = st.checkbox("Usar amostra de páginas", value=amostra_texto)
        
        if amostra_texto:
            st.info("📊 Usará apenas uma amostra inteligente do texto")
        else:
            st.warning("⚠️ Processará todo o texto (pode ser lento para arquivos grandes)")
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload do PDF")
        
        # Verifica PDFs na pasta dados
        pdfs_disponiveis = list(Path("dados").glob("*.pdf"))
        
        if pdfs_disponiveis:
            st.success(f"✅ {len(pdfs_disponiveis)} PDF(s) encontrado(s) na pasta 'dados'")
            
            # Seleção do PDF
            pdf_escolhido = st.selectbox(
                "Escolha um PDF para analisar:",
                pdfs_disponiveis,
                format_func=lambda x: x.name
            )
            
            if st.button("🚀 Iniciar Análise", type="primary"):
                with st.spinner("Analisando PDF..."):
                    # Cria analisador
                    analisador = AnalisadorPDF(
                        max_palavras=max_palavras,
                        max_personagens=max_personagens,
                        amostra_texto=amostra_texto
                    )
                    
                    # Executa análise
                    resultados = analisador.analisar_pdf(str(pdf_escolhido), salvar_graficos=True)
                    
                    if resultados:
                        st.success("✅ Análise concluída!")
                        
                        # Mostra resultados
                        mostrar_resultados(analisador, resultados)
                    else:
                        st.error("❌ Erro na análise do PDF")
        else:
            st.warning("⚠️ Nenhum PDF encontrado na pasta 'dados'")
            st.info("Para usar o app:")
            st.markdown("1. Coloque um PDF na pasta `dados/`")
            st.markdown("2. Recarregue a página")
            st.markdown("3. Selecione o PDF e inicie a análise")
    
    with col2:
        st.header("📊 Estatísticas")
        
        if 'analisador' in locals() and hasattr(analisador, 'palavras'):
            st.metric("Palavras Processadas", f"{len(analisador.palavras):,}")
            st.metric("Personagens Únicos", len(set(analisador.nomes_proprios)))
            st.metric("Total de Aparições", f"{sum(analisador.freq_nomes.values()):,}")
            
            if analisador.freq_nomes:
                mais_frequente = analisador.freq_nomes.most_common(1)[0]
                st.metric("Personagem Mais Frequente", f"{mais_frequente[0]} ({mais_frequente[1]})")
        
        st.header("💡 Dicas")
        st.info("""
        **Para melhores resultados:**
        - Use modo "Rápida" para livros grandes
        - Use modo "Completa" para contos/novelas curtas
        - PDFs com texto extraível funcionam melhor
        """)

def mostrar_resultados(analisador, resultados):
    """
    Mostra os resultados da análise
    """
    st.header("🏆 Resultados da Análise")
    
    # Top 20 personagens
    st.subheader("Top 20 Personagens Mais Frequentes")
    
    if analisador.freq_nomes:
        # Cria DataFrame para exibição
        mais_comuns = analisador.freq_nomes.most_common(20)
        df_personagens = pd.DataFrame(mais_comuns, columns=['Personagem', 'Frequência'])
        df_personagens['Posição'] = range(1, len(df_personagens) + 1)
        df_personagens = df_personagens[['Posição', 'Personagem', 'Frequência']]
        
        # Calcula percentual
        total_aparicoes = sum(analisador.freq_nomes.values())
        df_personagens['% do Total'] = (df_personagens['Frequência'] / total_aparicoes * 100).round(1)
        
        # Exibe tabela
        st.dataframe(df_personagens, use_container_width=True)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Gráfico de Frequência")
            if os.path.exists("resultados/graficos/personagens_frequencia.png"):
                st.image("resultados/graficos/personagens_frequencia.png", use_column_width=True)
            else:
                st.warning("Gráfico não encontrado")
        
        with col2:
            st.subheader("📍 Gráfico de Dispersão")
            if os.path.exists("resultados/graficos/personagens_dispersao.png"):
                st.image("resultados/graficos/personagens_dispersao.png", use_column_width=True)
            else:
                st.warning("Gráfico não encontrado")
        
        # Estatísticas detalhadas
        with st.expander("📈 Estatísticas Detalhadas"):
            st.write(f"**Total de palavras no texto:** {len(analisador.palavras):,}")
            st.write(f"**Personagens únicos encontrados:** {len(set(analisador.nomes_proprios))}")
            st.write(f"**Total de aparições de personagens:** {total_aparicoes:,}")
            
            if analisador.freq_nomes:
                st.write(f"**Personagem mais frequente:** {mais_comuns[0][0]} ({mais_comuns[0][1]} aparições)")
                st.write(f"**Personagem menos frequente (top 20):** {mais_comuns[-1][0]} ({mais_comuns[-1][1]} aparições)")
    else:
        st.warning("Nenhum personagem encontrado")

if __name__ == "__main__":
    main() 