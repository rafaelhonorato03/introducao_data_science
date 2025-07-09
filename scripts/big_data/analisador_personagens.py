import spacy
import fitz
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
from leia.leia import SentimentIntensityAnalyzer
import networkx as nx
from pyvis.network import Network
from tqdm import tqdm
import gc
from pathlib import Path
import re
from itertools import combinations
import os
import streamlit as st
try:
    import community.community_louvain as community_louvain
except ImportError:
    try:
        from community import community_louvain
    except ImportError:
        # Fallback: tentar instalar e importar
        import subprocess
        import sys
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-louvain"])
            import community.community_louvain as community_louvain
        except:
            # Se não conseguir instalar, definir como None para evitar erros
            community_louvain = None

class AnalisadorDePersonagens:
    """
    Classe de lógica de análise
    """
    def __init__(self):
        self.nlp = self.carregar_modelo_spacy()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.resultados = {
            "frequencia": Counter(), "sentimentos": defaultdict(list),
            "posicoes": defaultdict(list), "relacionamentos": Counter()
        }
        self.total_caracteres = 0

    @staticmethod
    def carregar_modelo_spacy():
        """Carrega o modelo Spacy (para ser cacheado pelo Streamlit)."""
        import subprocess
        import sys
        
        try:
            return spacy.load("pt_core_news_sm")
        except OSError:
            try:
                # Tenta baixar o modelo se não estiver disponível
                subprocess.check_call([sys.executable, "-m", "spacy", "download", "pt_core_news_sm"])
                return spacy.load("pt_core_news_sm")
            except:
                # Se falhar, usa o modelo em inglês como fallback
                try:
                    return spacy.load("en_core_web_sm")
                except OSError:
                    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
                    return spacy.load("en_core_web_sm")

    def _limpar_nome(self, nome_texto):
        titulos = ['Sor', 'Lorde', 'Lady', 'Rei', 'Rainha', 'Senhor', 'Senhora', 'Príncipe', 'Princesa']
        for titulo in titulos:
            nome_texto = re.sub(r'\b' + titulo + r'\b', '', nome_texto, flags=re.IGNORECASE)
        return nome_texto.strip()

    def analisar_livro(self, pdf_bytes, tamanho_chunk=50000):
        """Processa o livro a partir de bytes de arquivo."""
        try:
            doc_pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
            texto_completo = "".join([page.get_text() for page in doc_pdf])
            self.total_caracteres = len(texto_completo)
            doc_pdf.close()
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo PDF: {e}")

        for i in range(0, self.total_caracteres, tamanho_chunk):
            chunk_texto = texto_completo[i:i+tamanho_chunk]
            doc_nlp = self.nlp(chunk_texto)
            for sent in doc_nlp.sents:
                personagens_na_frase = {self._limpar_nome(ent.text) for ent in sent.ents if ent.label_ == "PER" and len(self._limpar_nome(ent.text)) > 2}
                if not personagens_na_frase: continue
                
                for p in personagens_na_frase:
                    self.resultados["frequencia"][p] += 1
                    self.resultados["posicoes"][p].append(i + sent.start_char)

                sentimento = self.sentiment_analyzer.polarity_scores(sent.text)['compound']
                for p in personagens_na_frase: self.resultados["sentimentos"][p].append(sentimento)
                
                if len(personagens_na_frase) > 1:
                    for par in combinations(sorted(list(personagens_na_frase)), 2):
                        self.resultados["relacionamentos"][par] += 1
            gc.collect()

    def gerar_grafico_frequencia(self, top_n=25):
        mais_comuns = self.resultados["frequencia"].most_common(top_n)
        if not mais_comuns: return None
        df = pd.DataFrame(mais_comuns, columns=['Personagem', 'Frequência'])
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='Frequência', y='Personagem', data=df, palette='viridis', ax=ax)
        ax.set_title(f'Top {top_n} Personagens Mais Frequentes', fontsize=16)
        plt.tight_layout()
        return fig

    def gerar_grafico_evolucao(self, top_n=10):
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais: return None
        fig, ax = plt.subplots(figsize=(12, 7))
        for personagem in personagens_principais:
            posicoes_norm = [(p / self.total_caracteres) * 100 for p in self.resultados["posicoes"][personagem]]
            if posicoes_norm: sns.kdeplot(posicoes_norm, label=personagem, fill=True, alpha=0.2, ax=ax)
        ax.set_title('Evolução dos Personagens ao Longo do Livro', fontsize=16)
        ax.set_xlabel('Posição no Texto (%)')
        ax.legend()
        plt.tight_layout()
        return fig

    def gerar_grafico_evolucao_dinamico(self, personagens_selecionados):
        """Gera gráfico de evolução para personagens selecionados dinamicamente."""
        if not personagens_selecionados: return None
        
        # Filtrar apenas personagens que existem nos dados
        personagens_validos = [p for p in personagens_selecionados if p in self.resultados["posicoes"]]
        if not personagens_validos: return None
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Cores para diferentes personagens
        cores = plt.cm.Set3(np.linspace(0, 1, len(personagens_validos)))
        
        for i, personagem in enumerate(personagens_validos):
            posicoes_norm = [(p / self.total_caracteres) * 100 for p in self.resultados["posicoes"][personagem]]
            if posicoes_norm:
                sns.kdeplot(posicoes_norm, label=personagem, fill=True, alpha=0.3, 
                           color=cores[i], ax=ax, linewidth=2)
        
        ax.set_title(f'Evolução dos Personagens Selecionados ao Longo do Livro', fontsize=16, fontweight='bold')
        ax.set_xlabel('Posição no Texto (%)', fontsize=12)
        ax.set_ylabel('Densidade de Menções', fontsize=12)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig

    def gerar_grafico_sentimentos(self, top_n=25):
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        sentimentos_medios = {p: sum(self.resultados["sentimentos"][p]) / len(self.resultados["sentimentos"][p]) for p in personagens_principais if self.resultados["sentimentos"][p]}
        if not sentimentos_medios: return None
        df = pd.DataFrame(list(sentimentos_medios.items()), columns=['Personagem', 'Sentimento Médio']).sort_values('Sentimento Médio', ascending=False)
        cores = ['#2ca02c' if s > 0.05 else '#d62728' if s < -0.05 else '#7f7f7f' for s in df['Sentimento Médio']]
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='Sentimento Médio', y='Personagem', data=df, palette=cores, ax=ax)
        ax.set_title('Análise de Sentimento Médio por Personagem', fontsize=16)
        ax.set_xlim(-1, 1)
        ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
        plt.tight_layout()
        return fig

    def gerar_grafico_dispersao(self, top_n=15):
        
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais: return None
        
        # Criar figura com subplots - um para cada personagem
        n_personagens = len(personagens_principais)
        fig, axes = plt.subplots(n_personagens, 1, figsize=(14, 2 * n_personagens))
        
        # Se só há um personagem, axes não é uma lista
        if n_personagens == 1:
            axes = [axes]
        
        # Cores para diferentes personagens
        cores = plt.cm.tab10(np.linspace(0, 1, n_personagens))
        
        for i, personagem in enumerate(personagens_principais):
            ax = axes[i]
            posicoes = self.resultados["posicoes"][personagem]
            
            if posicoes:
                # Normalizar posições para porcentagem do texto
                posicoes_norm = [(p / self.total_caracteres) * 100 for p in posicoes]
                
                # Criar barrinhas verticais (|) para cada aparição
                for pos in posicoes_norm:
                    ax.axvline(x=pos, ymin=0.3, ymax=0.7, color=cores[i], linewidth=1.5, alpha=0.8)
                
                # Configurar eixo
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 1)
                ax.set_yticks([])  # Remove ticks do eixo Y
                ax.set_ylabel(personagem, fontsize=12, fontweight='bold', rotation=0, ha='right', va='center')
                
                # Adicionar grid sutil
                ax.grid(True, alpha=0.2, axis='x')
                
                # Adicionar título apenas no primeiro gráfico
                if i == 0:
                    ax.set_title('Dispersão de Aparições dos Personagens ao Longo do Livro', 
                               fontsize=16, fontweight='bold', pad=20)
                
                # Adicionar rótulos de porcentagem apenas no último gráfico
                if i == n_personagens - 1:
                    ax.set_xlabel('Posição no Texto (%)', fontsize=12)
                    # Adicionar algumas marcas de porcentagem
                    ax.set_xticks([0, 25, 50, 75, 100])
                    ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
                else:
                    ax.set_xticks([])  # Remove ticks do eixo X para gráficos intermediários
                
                # Adicionar contador de aparições
                ax.text(102, 0.5, f'({len(posicoes)}x)', fontsize=10, va='center', 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.7))
            else:
                # Caso não haja posições para o personagem
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 1)
                ax.set_yticks([])
                ax.set_ylabel(personagem, fontsize=12, fontweight='bold', rotation=0, ha='right', va='center')
                ax.text(50, 0.5, 'Nenhuma aparição', ha='center', va='center', 
                       fontsize=10, style='italic', color='gray')
        
        plt.tight_layout()
        return fig

    def gerar_rede_relacionamentos(self, top_n=30):
        """Modificado para salvar em um arquivo temporário e ler o HTML de volta."""
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais: return None
        
        # Calcular tamanhos normalizados para limitar o tamanho das bolhas
        frequencias = [self.resultados["frequencia"][p] for p in personagens_principais]
        max_freq = max(frequencias) if frequencias else 1
        min_freq = min(frequencias) if frequencias else 1
        
        # Normalizar tamanhos entre 10 e 50 (valores menores = bolhas menores)
        def normalizar_tamanho(freq):
            if max_freq == min_freq:
                return 20  # tamanho padrão se todas as frequências forem iguais
            return 10 + (freq - min_freq) / (max_freq - min_freq) * 40
        
        G = nx.Graph()
        for personagem in personagens_principais:
            freq = self.resultados["frequencia"][personagem]
            tamanho_normalizado = normalizar_tamanho(freq)
            G.add_node(personagem, size=tamanho_normalizado, title=f"{personagem}\nMenções: {freq}")

        # Normalizar pesos das arestas para controlar a espessura das linhas
        pesos_arestas = [peso for par, peso in self.resultados["relacionamentos"].items() 
                        if par[0] in G and par[1] in G]
        max_peso = max(pesos_arestas) if pesos_arestas else 1
        min_peso = min(pesos_arestas) if pesos_arestas else 1
        
        def normalizar_peso(peso):
            if max_peso == min_peso:
                return 1.0  # peso padrão se todos os pesos forem iguais
            return 0.5 + (peso - min_peso) / (max_peso - min_peso) * 2.5
        
        for par, peso in self.resultados["relacionamentos"].items():
            p1, p2 = par
            if p1 in G and p2 in G:
                peso_normalizado = normalizar_peso(peso)
                G.add_edge(p1, p2, weight=peso_normalizado, title=f"Interações: {peso}")

        G.remove_nodes_from(list(nx.isolates(G)))
        
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        
        # Configurações personalizadas para controlar melhor o tamanho das bolhas e espessura das linhas
        net.set_options("""
        var options = {
          "nodes": {
            "font": { "size": 14 },
            "scaling": {
              "min": 10,
              "max": 50,
              "label": {
                "enabled": true,
                "min": 12,
                "max": 16
              }
            }
          },
          "edges": { 
            "color": { "inherit": true }, 
            "smooth": false,
            "width": {
              "min": 0.5,
              "max": 3
            },
            "scaling": {
              "min": 0.5,
              "max": 3,
              "label": {
                "enabled": true,
                "min": 8,
                "max": 12
              }
            }
          },
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -100,
              "centralGravity": 0.01,
              "springLength": 200,
              "springConstant": 0.09,
              "avoidOverlap": 1
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """)
        
        caminho_arquivo_html = "rede_temp.html"
        net.write_html(caminho_arquivo_html)

        with open(caminho_arquivo_html, 'r', encoding='utf-8') as f:
            html_content = f.read()

        os.remove(caminho_arquivo_html)
            
        return html_content

    def analisar_pontes_narrativas(self, top_n = 10):
        """ Calcula e retorna os personagens com maior centralidade de intermediação. """
        # Gerando grafo
        G = nx.Graph()
        # Buscando muitos personagens
        personagens_principais = {p for p, f in self.resultados["frequencia"].most_common(50)}

        for par, peso in self.resultados["relacionamentos"].items():
            p1, p2 = par
            if p1 in personagens_principais and p2 in personagens_principais:
                G.add_edge(p1, p2, weight=peso)
        
        if G.number_of_nodes() == 0:
            return None
        
        # Calculando a centralidade de intermediação
        # O 'weight' faz com que as conexões mais fortes (mais interações) sejam caminhos 'mais curtos'
        betweenness = nx.betweenness_centrality(G, weight='weight', normalized=True)

        # Criar um DataFrame para fácil visualização no streamlit
        df_pontes = pd.DataFrame(list(betweenness.items()), columns=['Personagem', 'Centralidade de Intermediação'])
        df_pontes = df_pontes.sort_values('Centralidade de Intermediação', ascending=False).head(top_n)

        return df_pontes
    
    def gerar_rede_comunidades(self, top_n=50):
        """Gera rede de comunidades usando algoritmo Louvain."""
        personagens_principais = {p for p, f in self.resultados["frequencia"].most_common(top_n)}
        if not personagens_principais: 
            return None
        
        G = nx.Graph()
        # Adicionando nós primeiro
        for p in personagens_principais:
            G.add_node(p)

        # Adicionando as arestas
        for par, peso in self.resultados["relacionamentos"].items():
            p1, p2 = par
            if p1 in G and p2 in G:
                G.add_edge(p1, p2, weight=peso)
        
        G.remove_nodes_from(list(nx.isolates(G)))
        if G.number_of_nodes() == 0: 
            return None

        # Detecção de comunidades
        if community_louvain is None:
            st.warning("Módulo python-louvain não disponível. Instalando...")
            return None
        
        try:
            partition = community_louvain.best_partition(G, weight='weight')
        except Exception as e:
            st.error(f"Erro na detecção de comunidades: {e}")
            return None

        # Contar número de comunidades
        num_comunidades = len(set(partition.values()))
        
        # Adicionando informações da comunidade e o tamanho aos nós do grafo
        max_freq = self.resultados["frequencia"].most_common(1)[0][1] if self.resultados["frequencia"] else 1
        
        for node in G.nodes():
            freq = self.resultados["frequencia"][node]
            # Normalizar tamanho entre 15 e 50
            tamanho_normalizado = 15 + (freq / max_freq) * 35
            
            G.nodes[node]['group'] = partition[node]  # O group é usado para colorir
            G.nodes[node]['size'] = tamanho_normalizado
            G.nodes[node]['title'] = f"{node}<br>Menções: {freq}<br>Comunidade: {partition[node]}"

        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        
        # Configurações personalizadas para melhor visualização
        net.set_options(f"""
        var options = {{
          "nodes": {{
            "font": {{ "size": 14, "color": "#ffffff" }},
            "scaling": {{
              "min": 15,
              "max": 50,
              "label": {{
                "enabled": true,
                "min": 12,
                "max": 16
              }}
            }}
          }},
          "edges": {{ 
            "color": {{ "inherit": true }}, 
            "smooth": false,
            "width": {{
              "min": 0.5,
              "max": 3
            }}
          }},
          "physics": {{
            "forceAtlas2Based": {{
              "gravitationalConstant": -100,
              "centralGravity": 0.01,
              "springLength": 200,
              "springConstant": 0.09,
              "avoidOverlap": 1
            }},
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }},
          "groups": {{
            "0": {{ "color": "#ff7675" }},
            "1": {{ "color": "#74b9ff" }},
            "2": {{ "color": "#55a3ff" }},
            "3": {{ "color": "#a29bfe" }},
            "4": {{ "color": "#fd79a8" }},
            "5": {{ "color": "#fdcb6e" }},
            "6": {{ "color": "#6c5ce7" }},
            "7": {{ "color": "#00b894" }},
            "8": {{ "color": "#e17055" }},
            "9": {{ "color": "#636e72" }}
          }}
        }}
        """)

        caminho_arquivo_html = "rede_comunidades.html"
        net.write_html(caminho_arquivo_html)
        
        with open(caminho_arquivo_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        os.remove(caminho_arquivo_html)
        
        # Adicionar informações sobre as comunidades detectadas
        if st:
            st.info(f"🔍 **Detectadas {num_comunidades} comunidades** de personagens no texto.")
        
        return html_content
    
    def obter_estatisticas_comunidades(self, top_n=50):
        """Retorna estatísticas detalhadas das comunidades detectadas."""
        personagens_principais = {p for p, f in self.resultados["frequencia"].most_common(top_n)}
        if not personagens_principais: 
            return None
        
        G = nx.Graph()
        for p in personagens_principais:
            G.add_node(p)

        for par, peso in self.resultados["relacionamentos"].items():
            p1, p2 = par
            if p1 in G and p2 in G:
                G.add_edge(p1, p2, weight=peso)
        
        G.remove_nodes_from(list(nx.isolates(G)))
        if G.number_of_nodes() == 0: 
            return None

        if community_louvain is None:
            return None
        
        try:
            partition = community_louvain.best_partition(G, weight='weight')
        except Exception:
            return None

        # Calcular estatísticas por comunidade
        comunidades_stats = {}
        for node, comunidade in partition.items():
            if comunidade not in comunidades_stats:
                comunidades_stats[comunidade] = {
                    'personagens': [],
                    'frequencia_total': 0,
                    'interacoes_internas': 0,
                    'interacoes_externas': 0
                }
            
            freq = self.resultados["frequencia"][node]
            comunidades_stats[comunidade]['personagens'].append((node, freq))
            comunidades_stats[comunidade]['frequencia_total'] += freq

        # Calcular interações internas e externas
        for par, peso in self.resultados["relacionamentos"].items():
            p1, p2 = par
            if p1 in partition and p2 in partition:
                if partition[p1] == partition[p2]:
                    comunidades_stats[partition[p1]]['interacoes_internas'] += peso
                else:
                    comunidades_stats[partition[p1]]['interacoes_externas'] += peso
                    comunidades_stats[partition[p2]]['interacoes_externas'] += peso

        # Ordenar personagens por frequência em cada comunidade
        for comunidade in comunidades_stats:
            comunidades_stats[comunidade]['personagens'].sort(key=lambda x: x[1], reverse=True)

        return comunidades_stats