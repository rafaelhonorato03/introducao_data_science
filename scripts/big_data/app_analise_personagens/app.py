import streamlit as st
# É uma boa prática importar a classe com um alias para evitar conflitos
from analisador_personagens_st import AnalisadorDePersonagens
import time
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Analisador de Livros PDF", layout="wide")

# --- FUNÇÃO DE ANÁLISE COM CACHE ---
# Esta função executa a análise pesada e é cacheada pelo Streamlit.
# Ela só será re-executada se os bytes do arquivo de entrada mudarem.
@st.cache_data(show_spinner=False)
def processar_livro(pdf_bytes):
    """Executa a análise pesada e retorna um dicionário de resultados visuais."""
    analisador = AnalisadorDePersonagens()
    analisador.analisar_livro(pdf_bytes)

    # Gera os resultados que não precisam de interação do usuário
    resultados_visuais = {
        "fig_frequencia": analisador.gerar_grafico_frequencia(),
        "fig_dispersao": analisador.gerar_grafico_dispersao(),
        "html_rede": analisador.gerar_rede_relacionamentos(),
        # Guarda o objeto analisador para gerar gráficos dinâmicos depois
        "analisador": analisador,
    }
    return resultados_visuais

# --- INTERFACE PRINCIPAL DA APLICAÇÃO ---
st.title("📚 Analisador de Personagens em Livros PDF")
st.markdown("Faça o upload de um livro em formato PDF para analisar a frequência, evolução e relacionamento entre os personagens.")

# Widget para fazer o upload do arquivo
uploaded_file = st.file_uploader("Arraste e solte seu arquivo PDF aqui", type="pdf")

# <<< CORREÇÃO PRINCIPAL AQUI >>>
# Todo o código que depende do arquivo enviado deve estar dentro deste bloco 'if'.
if uploaded_file is not None:
    
    # Cria um identificador único para o arquivo usando seu nome e tamanho.
    # Isso garante que a análise seja refeita se um novo arquivo for enviado.
    file_identifier = f"{uploaded_file.name}_{uploaded_file.size}"
    
    # Verifica se os resultados já estão na memória da sessão para o arquivo atual.
    # Se não estiverem, ou se o arquivo for diferente, executa a análise.
    if 'resultados' not in st.session_state or st.session_state.get('file_id') != file_identifier:
        with st.spinner('A análise começou... Isso pode levar vários minutos. Por favor, aguarde.'):
            start_time = time.time()
            pdf_bytes = uploaded_file.getvalue()
            
            # Chama a função cacheada para processar o livro
            st.session_state.resultados = processar_livro(pdf_bytes)
            
            # Armazena o identificador do arquivo na sessão para a próxima verificação
            st.session_state.file_id = file_identifier
            end_time = time.time()
        st.success(f'Análise do livro "{uploaded_file.name}" concluída em {end_time - start_time:.2f} segundos!')

    # --- EXIBIÇÃO DOS RESULTADOS ---
    # Pega os resultados e o objeto analisador da memória da sessão
    resultados = st.session_state.resultados
    analisador = resultados["analisador"]

    st.header("Resultados da Análise", divider='rainbow')

    # Cria as abas para organizar os resultados
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Gráficos Gerais", 
        "📈 Dispersão de Aparições", 
        "🕸️ Rede de Relacionamentos", 
        "🌉 Personagens-Ponte", 
        "🏘️ Detecção de Comunidades"
    ])

    with tab1:
        st.subheader("Frequência de Personagens")
        if resultados["fig_frequencia"]:
            st.pyplot(resultados["fig_frequencia"])
        else:
            st.warning("Não foram encontrados personagens para gerar este gráfico.")

        st.subheader("Evolução das Menções ao Longo do Livro")
        personagens_disponiveis = [p for p, f in analisador.resultados["frequencia"].most_common()]
        if personagens_disponiveis:
            personagens_selecionados = st.multiselect(
                "Selecione os personagens para visualizar a evolução:",
                options=personagens_disponiveis,
                default=personagens_disponiveis[:5]
            )
            if personagens_selecionados:
                # Gera o gráfico dinamicamente com base na seleção do usuário
                fig_evolucao_dinamica = analisador.gerar_grafico_evolucao_dinamico(personagens_selecionados)
                st.pyplot(fig_evolucao_dinamica)
    
    with tab2:
        st.subheader("Dispersão de Aparições dos Personagens")
        if resultados["fig_dispersao"]:
            st.pyplot(resultados["fig_dispersao"])
        else:
            st.warning("Não foram encontrados personagens para gerar este gráfico.")

    with tab3:
        st.subheader("Grafo Interativo de Relacionamentos")
        if resultados["html_rede"]:
            components.html(resultados["html_rede"], height=800, scrolling=True)
        else:
            st.warning("Não foram encontradas interações suficientes para gerar a rede.")

    with tab4:
        st.subheader("Personagens-Ponte da Narrativa")
        # Calcula a análise de pontes dinamicamente
        df_pontes = analisador.analisar_pontes_narrativas()
        if df_pontes is not None and not df_pontes.empty:
            st.dataframe(df_pontes, use_container_width=True)
            st.markdown("""
            **Centralidade de Intermediação:** Valores mais altos indicam personagens que funcionam como "pontes", conectando diferentes grupos e sendo cruciais para o fluxo da história.
            """)
        else:
            st.warning("Não foi possível calcular os personagens-ponte.")

    with tab5:
        st.subheader("Detecção de Comunidades de Personagens")
        top_n_comunidades = st.slider(
            "Número de personagens para analisar:", 10, 100, 50,
            help="Define quantos dos personagens mais frequentes serão usados para encontrar comunidades."
        )
        
        # Gera a rede de comunidades dinamicamente com base no slider
        html_comunidades = analisador.gerar_rede_comunidades(top_n=top_n_comunidades)
        if html_comunidades:
            components.html(html_comunidades, height=800, scrolling=True)

            # Mostra estatísticas das comunidades
            stats_comunidades = analisador.obter_estatisticas_comunidades(top_n=top_n_comunidades)
            if stats_comunidades:
                st.subheader("Estatísticas das Comunidades")
                for com_id, stats in sorted(stats_comunidades.items()):
                    principais = ", ".join([f"{p[0]} ({p[1]})" for p in stats['personagens'][:3]])
                    with st.expander(f"Comunidade {com_id} ({len(stats['personagens'])} membros) - Principais: {principais}"):
                        st.metric("Total de Menções na Comunidade", stats['frequencia_total'])
                        st.write(f"**Interações dentro do grupo:** {stats['interacoes_internas']}")
                        st.write(f"**Conexões com outros grupos:** {stats['interacoes_externas']}")
        else:
            st.warning("Não foi possível gerar a rede de comunidades.")

else:
    # Se nenhum arquivo for enviado (ou for removido), limpa os resultados da sessão.
    if 'resultados' in st.session_state:
        del st.session_state.resultados
    if 'file_id' in st.session_state:
        del st.session_state.file_id