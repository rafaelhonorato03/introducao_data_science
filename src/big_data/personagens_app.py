# --- 1. IMPORTAÇÕES ---
# Bibliotecas padrão e de terceiros
import time
import streamlit as st
import streamlit.components.v1 as components

# Importação da classe de análise principal.
# É crucial que o arquivo 'analisador_personagens.py' esteja no mesmo diretório.
# O nome do arquivo foi padronizado para 'analisador_personagens'.
try:
    from analisador_personagens import AnalisadorDePersonagens
except ImportError:
    st.error("Erro: O arquivo 'analisador_personagens.py' não foi encontrado. Certifique-se de que ele está no mesmo diretório que este script.")
    st.stop()

# --- 2. CONFIGURAÇÃO DA PÁGINA E ESTILO ---
st.set_page_config(
    page_title="Analisador de Livros PDF",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. FUNÇÃO DE ANÁLISE COM CACHE ---
@st.cache_data(show_spinner=False)
def processar_livro(pdf_bytes, file_name):
    """
    Executa a análise completa do livro.
    Esta função é "cacheada": o Streamlit armazena o resultado e só a re-executa se os
    argumentos de entrada (os bytes do PDF ou seu nome) mudarem.
    """
    # A mensagem de spinner será exibida do lado de fora da função cacheada
    # para melhor controle da interface.
    analisador = AnalisadorDePersonagens()
    analisador.analisar_livro(pdf_bytes)

    # Gera os resultados estáticos (que não dependem de interação do usuário na interface)
    resultados_visuais = {
        "fig_frequencia": analisador.gerar_grafico_frequencia(),
        "fig_dispersao": analisador.gerar_grafico_dispersao(),
        "html_rede_relacionamentos": analisador.gerar_rede_relacionamentos(),
        # Guarda o objeto 'analisador' para gerar visualizações dinâmicas posteriormente
        "analisador_obj": analisador,
    }
    return resultados_visuais

# --- 4. INTERFACE PRINCIPAL DA APLICAÇÃO ---
st.title("📚 Analisador de Personagens em Livros PDF")
st.markdown("Faça o upload de um livro em formato PDF para analisar a frequência, evolução, relacionamentos e estrutura da narrativa.")

# Widget para upload do arquivo
uploaded_file = st.file_uploader("Arraste e solte seu arquivo PDF aqui ou clique para selecionar", type="pdf")

# O código a seguir só é executado se um arquivo for carregado
if uploaded_file is not None:

    # Cria um identificador único para o arquivo. Se o usuário carregar um novo
    # arquivo (mesmo com o mesmo nome), a análise será refeita.
    file_identifier = f"{uploaded_file.name}_{uploaded_file.size}"

    # Verifica se os resultados já estão na memória da sessão para o arquivo atual.
    # Isso evita reprocessar o arquivo toda vez que o usuário interage com um widget.
    if 'analysis_results' not in st.session_state or st.session_state.get('current_file_id') != file_identifier:
        with st.spinner(f'Analisando o livro "{uploaded_file.name}"... Este processo pode levar alguns minutos. Por favor, aguarde.'):
            start_time = time.time()
            pdf_bytes = uploaded_file.getvalue()

            # Chama a função principal de análise
            st.session_state.analysis_results = processar_livro(pdf_bytes, uploaded_file.name)

            # Armazena o identificador do arquivo na sessão para futuras verificações
            st.session_state.current_file_id = file_identifier
            end_time = time.time()
        st.success(f'Análise concluída em {end_time - start_time:.2f} segundos!')

    # --- 5. EXIBIÇÃO DOS RESULTADOS ---
    # Recupera os resultados e o objeto analisador da memória da sessão
    resultados = st.session_state.analysis_results
    analisador = resultados["analisador_obj"]

    st.header("Resultados da Análise", divider='rainbow')

    # Cria as abas para organizar as diferentes análises
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Gráficos Gerais",
        "📈 Dispersão e Evolução",
        "🕸️ Rede de Relacionamentos",
        "🌉 Personagens-Ponte",
        "🏘️ Detecção de Comunidades"
    ])

    # --- ABA 1: GRÁFICOS GERAIS ---
    with tab1:
        st.subheader("Frequência de Personagens")
        st.markdown("Este gráfico mostra os personagens mais mencionados no livro, indicando sua importância geral na narrativa.")
        if resultados["fig_frequencia"]:
            st.pyplot(resultados["fig_frequencia"])
        else:
            st.warning("Não foram encontrados personagens suficientes para gerar o gráfico de frequência.")

    # --- ABA 2: DISPERSÃO E EVOLUÇÃO ---
    with tab2:
        st.subheader("Dispersão de Aparições dos Personagens")
        st.markdown("Veja onde, ao longo do livro (da primeira à última palavra), cada personagem aparece. Cada traço vertical `|` marca uma menção.")
        if resultados["fig_dispersao"]:
            st.pyplot(resultados["fig_dispersao"])
        else:
            st.warning("Não foram encontrados personagens para gerar o gráfico de dispersão.")

        st.divider()

        st.subheader("Evolução das Menções ao Longo do Livro")
        st.markdown("Selecione personagens para comparar como a frequência de suas menções evolui ao longo da narrativa.")
        personagens_disponiveis = [p for p, _ in analisador.resultados["frequencia"].most_common()]
        if personagens_disponiveis:
            personagens_selecionados = st.multiselect(
                "Selecione os personagens para visualizar a evolução:",
                options=personagens_disponiveis,
                default=personagens_disponiveis[:5] # Sugere os 5 mais frequentes
            )
            if personagens_selecionados:
                # Gera o gráfico dinamicamente com base na seleção do usuário
                fig_evolucao_dinamica = analisador.gerar_grafico_evolucao_dinamico(personagens_selecionados)
                st.pyplot(fig_evolucao_dinamica)
            else:
                st.info("Selecione ao menos um personagem para gerar o gráfico de evolução.")

    # --- ABA 3: REDE DE RELACIONAMENTOS ---
    with tab3:
        st.subheader("Grafo Interativo de Relacionamentos")
        st.markdown("Explore as conexões entre os personagens. O tamanho do círculo (nó) representa a frequência do personagem, e a espessura da linha (aresta) indica a força da interação entre eles.")
        if resultados["html_rede_relacionamentos"]:
            components.html(resultados["html_rede_relacionamentos"], height=800, scrolling=True)
        else:
            st.warning("Não foram encontradas interações suficientes para gerar a rede de relacionamentos.")

    # --- ABA 4: PERSONAGENS-PONTE ---
    with tab4:
        st.subheader("Análise de Personagens-Ponte (Centralidade)")
        st.markdown("Esta análise identifica personagens que são cruciais para o fluxo da história, atuando como conectores entre diferentes grupos ou núcleos da narrativa.")
        df_pontes = analisador.analisar_pontes_narrativas()
        if df_pontes is not None and not df_pontes.empty:
            st.dataframe(df_pontes, use_container_width=True)
            st.info("""
            **Como interpretar a tabela:**
            * **Personagem:** O nome do personagem.
            * **Centralidade de Intermediação:** Um valor alto indica que o personagem atua como uma "ponte", sendo fundamental para conectar diferentes grupos e para o desenrolar da trama. Remover esses personagens poderia fragmentar a história.
            """)
        else:
            st.warning("Não foi possível calcular os personagens-ponte. Isso pode ocorrer se a rede de relacionamentos for muito simples ou desconectada.")

    # --- ABA 5: DETECÇÃO DE COMUNIDADES ---
    with tab5:
        st.subheader("Detecção de Comunidades de Personagens")
        st.markdown("Esta visualização agrupa personagens que interagem mais frequentemente entre si do que com os outros, revelando os diferentes 'núcleos sociais' ou 'clusters' da narrativa.")

        top_n = st.slider(
            "Selecione o número de personagens (por frequência) para incluir na análise de comunidades:",
            min_value=10,
            max_value=150,
            value=50,
            step=5,
            help="Ajuste este valor para focar a análise nos personagens mais relevantes ou para ter uma visão mais ampla."
        )

        # Gera e exibe o grafo de comunidades dinamicamente
        html_comunidades = analisador.gerar_rede_comunidades(top_n=top_n)
        if html_comunidades:
            components.html(html_comunidades, height=800, scrolling=True)

            # Exibe estatísticas sobre as comunidades encontradas
            stats_comunidades = analisador.obter_estatisticas_comunidades(top_n=top_n)
            if stats_comunidades:
                st.subheader("Estatísticas das Comunidades")
                for com_id, stats in sorted(stats_comunidades.items()):
                    principais = ", ".join([f"**{p[0]}** ({p[1]})" for p in stats['personagens'][:3]])
                    with st.expander(f"Comunidade {com_id} ({len(stats['personagens'])} membros) - Principais: {principais}"):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total de Menções", stats['frequencia_total'])
                        col2.metric("Interações Internas", stats['interacoes_internas'])
                        col3.metric("Conexões Externas", stats['interacoes_externas'])
        else:
            st.warning("Não foi possível gerar a rede de comunidades com os parâmetros selecionados.")

else:
    # Limpa os resultados da sessão se o usuário remover o arquivo.
    # Isso garante que, se um novo arquivo for carregado, a análise seja refeita.
    if 'analysis_results' in st.session_state:
        del st.session_state['analysis_results']
    if 'current_file_id' in st.session_state:
        del st.session_state['current_file_id']
    st.info("Aguardando o upload de um arquivo PDF para iniciar a análise.")