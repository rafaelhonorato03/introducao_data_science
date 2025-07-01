#
# arquivo: app.py
#
# Execute com: streamlit run app.py
#

import streamlit as st
from analisador_personagens import AnalisadorDePersonagens
import time
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Analisador de Livros PDF")

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
        "html_rede": analisador.gerar_rede_relacionamentos(),
    }
    return resultados_visuais

# --- INTERFACE DA APLICAÇÃO ---
st.title("📚 Analisador de Personagens em Livros PDF")
st.markdown("Faça o upload de um livro em formato PDF para iniciar a análise.")

uploaded_file = st.file_uploader("Arraste e solte seu arquivo PDF aqui", type="pdf")

if uploaded_file is not None:
    # Usar st.session_state para guardar os resultados após o primeiro cálculo
    if 'resultados' not in st.session_state or st.session_state.file_id != uploaded_file.id:
        with st.spinner('A análise começou... Isso pode levar vários minutos. Por favor, aguarde.'):
            start_time = time.time()
            pdf_bytes = uploaded_file.getvalue()
            st.session_state.resultados = processar_livro(pdf_bytes)
            st.session_state.file_id = uploaded_file.id # Guarda o ID do arquivo processado
            end_time = time.time()
        st.success(f'Análise do livro "{uploaded_file.name}" concluída em {end_time - start_time:.2f} segundos!')

    # --- EXIBIÇÃO DOS RESULTADOS ---
    resultados = st.session_state.resultados
    st.header("Resultados da Análise", divider='rainbow')

    tab1, tab2, tab3 = st.tabs(["📊 Gráficos de Personagens", "❤️ Análise de Sentimentos", "🕸️ Rede de Relacionamentos"])

    with tab1:
        st.subheader("Frequência de Personagens")
        if resultados["fig_frequencia"]:
            st.pyplot(resultados["fig_frequencia"])
        else:
            st.warning("Não foram encontrados personagens para gerar este gráfico.")

        st.subheader("Evolução das Menções ao Longo do Livro")
        if resultados["fig_evolucao"]:
            st.pyplot(resultados["fig_evolucao"])
        else:
            st.warning("Não foram encontrados personagens para gerar este gráfico.")

    with tab2:
        st.subheader("Sentimento Médio por Personagem")
        if resultados["fig_sentimentos"]:
            st.pyplot(resultados["fig_sentimentos"])
        else:
            st.warning("Não foram encontrados dados de sentimento para gerar este gráfico.")

    with tab3:
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