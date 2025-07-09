import sys
import spacy
import fitz
from leia_br.leia_br import SentimentIntensityAnalyzer
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
        "html_comunidades": analisador.gerar_rede_comunidades(),
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

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Gráficos de Personagens", "📈 Dispersão de Aparições", "❤️ Análise de Sentimentos", "🕸️ Rede de Relacionamentos", "🌉 Personagens-Ponte", "🏘️ Detecção de Comunidades"])

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

    with tab5:
        st.subheader("Personagens-Ponte da Narrativa")
        st.markdown("**Estes personagens são os principais conectores da narrativa, ligando diferentes núcleos de personagens.**")
        
        if resultados["analisador"]:
            df_pontes = resultados["analisador"].analisar_pontes_narrativas()
            if df_pontes is not None and not df_pontes.empty:
                st.dataframe(df_pontes, use_container_width=True)
                
                # Adicionar informações adicionais sobre a análise
                st.markdown("---")
                st.markdown("**Sobre a Centralidade de Intermediação:**")
                st.markdown("""
                - **Valores mais altos** indicam personagens que são "pontes" entre diferentes grupos
                - **Personagens centrais** aparecem em muitas cenas com diferentes conjuntos de personagens
                - **Conectores narrativos** são essenciais para o fluxo da história
                """)
            else:
                st.warning("Não foram encontrados dados suficientes para analisar personagens-ponte.")
        else:
            st.warning("Dados do analisador não disponíveis.")

    with tab6:
        st.subheader("Detecção de Comunidades de Personagens")
        st.markdown("**Esta análise identifica grupos naturais de personagens que interagem mais entre si do que com outros grupos.**")
        
        # Controles para personalizar a análise
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**Configurações:**")
            top_n_comunidades = st.slider(
                "Top N personagens para análise:",
                min_value=10,
                max_value=100,
                value=50,
                help="Número de personagens mais frequentes a incluir na análise de comunidades"
            )
            
            if st.button("🔄 Regenerar Comunidades", help="Regenera a análise de comunidades com as novas configurações"):
                if resultados["analisador"]:
                    html_comunidades = resultados["analisador"].gerar_rede_comunidades(top_n_comunidades)
                    if html_comunidades:
                        st.session_state.html_comunidades_temp = html_comunidades
                        st.success("Comunidades regeneradas com sucesso!")
                    else:
                        st.error("Erro ao gerar comunidades.")
        
        with col2:
            st.write("**Sobre a Detecção de Comunidades:**")
            st.markdown("""
            - **Algoritmo Louvain**: Identifica grupos naturalmente formados
            - **Cores diferentes**: Cada cor representa uma comunidade
            - **Tamanho dos nós**: Baseado na frequência de menções
            - **Espessura das arestas**: Baseada na força das interações
            """)
        
        # Exibir a rede de comunidades
        if 'html_comunidades_temp' in st.session_state:
            html_comunidades = st.session_state.html_comunidades_temp
        else:
            html_comunidades = resultados["html_comunidades"]
        
        if html_comunidades:
            st.markdown("---")
            st.subheader("Rede de Comunidades Interativa")
            components.html(html_comunidades, height=800)
            
            # Estatísticas das comunidades
            if resultados["analisador"]:
                stats_comunidades = resultados["analisador"].obter_estatisticas_comunidades(top_n_comunidades)
                if stats_comunidades:
                    st.markdown("---")
                    st.subheader("📊 Estatísticas das Comunidades")
                    
                    # Criar expander para cada comunidade
                    for comunidade_id, stats in stats_comunidades.items():
                        with st.expander(f"🏘️ Comunidade {comunidade_id} - {len(stats['personagens'])} personagens"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Frequência Total", stats['frequencia_total'])
                            
                            with col2:
                                st.metric("Interações Internas", stats['interacoes_internas'])
                            
                            with col3:
                                st.metric("Interações Externas", stats['interacoes_externas'])
                            
                            # Lista de personagens da comunidade
                            st.write("**Personagens da comunidade:**")
                            personagens_texto = ", ".join([f"{p} ({f})" for p, f in stats['personagens'][:10]])
                            if len(stats['personagens']) > 10:
                                personagens_texto += f" e mais {len(stats['personagens']) - 10}..."
                            st.write(personagens_texto)
                            
                            # Coesão da comunidade
                            total_interacoes = stats['interacoes_internas'] + stats['interacoes_externas']
                            if total_interacoes > 0:
                                coesao = (stats['interacoes_internas'] / total_interacoes) * 100
                                st.progress(coesao / 100)
                                st.caption(f"Coesão da comunidade: {coesao:.1f}%")
            
            # Informações adicionais sobre as comunidades
            st.markdown("---")
            st.markdown("**Como interpretar as comunidades:**")
            st.markdown("""
            - **Personagens da mesma cor** pertencem à mesma comunidade
            - **Comunidades bem definidas** indicam grupos coesos na narrativa
            - **Personagens isolados** podem ser protagonistas ou antagonistas
            - **Pontes entre comunidades** são personagens que conectam diferentes grupos
            - **Coesão alta** indica que a comunidade é bem definida e coesa
            """)
        else:
            st.warning("Não foram encontrados dados suficientes para gerar a rede de comunidades.")
            st.info("💡 **Dica**: Tente aumentar o número de personagens ou verificar se há interações suficientes no texto.")
else:
    # Limpa os resultados se não houver arquivo carregado
    if 'resultados' in st.session_state:
        del st.session_state.resultados
    if 'file_id' in st.session_state:
        del st.session_state.file_id