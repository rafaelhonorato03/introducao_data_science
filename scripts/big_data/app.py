#
# arquivo: app.py
#
# Execute com: streamlit run app.py
#

import subprocess
import sys

# Instalar dependências necessárias se não estiverem disponíveis
try:
    import spacy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
    import spacy

try:
    import fitz
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])
    import fitz

try:
    from leia.leia import SentimentIntensityAnalyzer
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "leia"])
    from leia.leia import SentimentIntensityAnalyzer

import streamlit as st
from analisador_personagens import AnalisadorDePersonagens
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Analisador de Livros PDF")

# --- FUNÇÃO DE ANÁLISE COM CACHE ---
@st.cache_data(show_spinner=False)
def processar_livro(pdf_bytes):
    """Executa a análise pesada e retorna um dicionário de resultados visuais."""
    analisador = AnalisadorDePersonagens()
    analisador.analisar_livro(pdf_bytes)

    resultados_visuais = {
        "fig_frequencia": analisador.gerar_grafico_frequencia(),
        "fig_evolucao": analisador.gerar_grafico_evolucao(),
        "fig_sentimentos": analisador.gerar_grafico_sentimentos(),
        "fig_dispersao": analisador.gerar_grafico_dispersao(),
        "html_rede": analisador.gerar_rede_relacionamentos(),
        "analisador": analisador,  # Guarda o analisador para acesso aos dados brutos
    }
    return resultados_visuais

# --- INTERFACE DA APLICAÇÃO ---
st.title("📚 Analisador de Personagens em Livros PDF")
st.markdown("Faça o upload de um livro em formato PDF para iniciar a análise.")

uploaded_file = st.file_uploader("Arraste e solte seu arquivo PDF aqui", type="pdf")

if uploaded_file is not None:
    # Criar um identificador único baseado no nome e tamanho do arquivo
    file_identifier = f"{uploaded_file.name}_{uploaded_file.size}"
    
    # Usar st.session_state para guardar os resultados após o primeiro cálculo
    if 'resultados' not in st.session_state or st.session_state.file_id != file_identifier:
        with st.spinner('A análise começou... Isso pode levar vários minutos. Por favor, aguarde.'):
            start_time = time.time()
            pdf_bytes = uploaded_file.getvalue()
            st.session_state.resultados = processar_livro(pdf_bytes)
            st.session_state.file_id = file_identifier # Guarda o identificador do arquivo processado
            end_time = time.time()
        st.success(f'Análise do livro "{uploaded_file.name}" concluída em {end_time - start_time:.2f} segundos!')

    # --- EXIBIÇÃO DOS RESULTADOS ---
    resultados = st.session_state.resultados
    st.header("Resultados da Análise", divider='rainbow')

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Gráficos de Personagens", "📈 Dispersão de Aparições", "❤️ Análise de Sentimentos", "🕸️ Rede de Relacionamentos"])

    with tab1:
        st.subheader("Frequência de Personagens")
        if resultados["fig_frequencia"]:
            st.pyplot(resultados["fig_frequencia"])
        else:
            st.warning("Não foram encontrados personagens para gerar este gráfico.")

        st.subheader("Evolução das Menções ao Longo do Livro")
        
        # Seletor dinâmico de personagens
        if resultados["analisador"]:
            # Obter lista de personagens ordenados por frequência
            personagens_disponiveis = [p for p, f in resultados["analisador"].resultados["frequencia"].most_common()]
            
            if personagens_disponiveis:
                # Seletor múltiplo de personagens
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write("**Selecione os personagens:**")
                    personagens_selecionados = st.multiselect(
                        "Personagens para visualizar:",
                        options=personagens_disponiveis,
                        default=personagens_disponiveis[:5],  # Primeiros 5 por padrão
                        help="Escolha quais personagens deseja ver no gráfico de evolução"
                    )
                
                with col2:
                    st.write("**Controles:**")
                    col2a, col2b = st.columns(2)
                    with col2a:
                        if st.button("Selecionar Top 5", help="Seleciona os 5 personagens mais frequentes"):
                            personagens_selecionados = personagens_disponiveis[:5]
                            st.rerun()
                    
                    with col2b:
                        if st.button("Selecionar Todos", help="Seleciona todos os personagens"):
                            personagens_selecionados = personagens_disponiveis
                            st.rerun()
                
                # Gerar gráfico dinâmico
                if personagens_selecionados:
                    fig_evolucao_dinamica = resultados["analisador"].gerar_grafico_evolucao_dinamico(personagens_selecionados)
                    if fig_evolucao_dinamica:
                        st.pyplot(fig_evolucao_dinamica)
                    else:
                        st.warning("Não foi possível gerar o gráfico com os personagens selecionados.")
                else:
                    st.info("Selecione pelo menos um personagem para visualizar a evolução.")
            else:
                st.warning("Não foram encontrados personagens para gerar este gráfico.")
        else:
            st.warning("Dados do analisador não disponíveis.")

    with tab2:
        st.subheader("Dispersão de Aparições dos Personagens")
        st.markdown("**Cada barrinha vertical (|) representa uma aparição do personagem no texto.**")
        if resultados["fig_dispersao"]:
            st.pyplot(resultados["fig_dispersao"])
        else:
            st.warning("Não foram encontrados personagens para gerar este gráfico.")

    with tab3:
        st.subheader("Sentimento Médio por Personagem")
        if resultados["fig_sentimentos"]:
            st.pyplot(resultados["fig_sentimentos"])
        else:
            st.warning("Não foram encontrados dados de sentimento para gerar este gráfico.")

    with tab4:
        st.subheader("Grafo Interativo de Relacionamentos")
        if resultados["html_rede"]:
            components.html(resultados["html_rede"], height=800)
        else:
            st.warning("Não foram encontradas interações suficientes para gerar a rede de relacionamentos.")
else:
    # Limpa os resultados se não houver arquivo carregado
    if 'resultados' in st.session_state:
        del st.session_state.resultados
    if 'file_id' in st.session_state:
        del st.session_state.file_id