# -*- coding: utf-8 -*-
"""
Módulo Unificado para Análise de Personagens em Textos.

Este arquivo contém a classe `AnalisadorDePersonagens`, que encapsula toda a lógica
de processamento de texto de PDFs, análise de NLP, e geração de visualizações.
Foi projetado para ser importado por uma interface de usuário, como um script
Streamlit ou um programa de linha de comando.

Dependências principais:
- spacy: Para reconhecimento de entidades (personagens).
- fitz (PyMuPDF): Para extração de texto de PDFs.
- pandas, seaborn, matplotlib: Para manipulação de dados e criação de gráficos.
- leia: Para análise de sentimentos em português.
- networkx, pyvis: Para análise e visualização de redes de relacionamentos.
- python-louvain: Para detecção de comunidades em redes.
"""

# --- IMPORTAÇÕES ---
import os
import re
import gc
import time
from itertools import combinations
from collections import Counter, defaultdict
from pathlib import Path

# Bibliotecas de processamento e análise
import spacy
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
import networkx as nx
from leia.leia import SentimentIntensityAnalyzer

# Bibliotecas de visualização
import seaborn as sns
import matplotlib.pyplot as plt
from pyvis.network import Network

# Módulo de detecção de comunidades
try:
    import community.community_louvain as community_louvain
except ImportError:
    print("Aviso: A biblioteca 'python-louvain' não foi encontrada. A funcionalidade de detecção de comunidades não estará disponível.")
    community_louvain = None


# --- CLASSE DE LÓGICA DE ANÁLISE ---

class AnalisadorDePersonagens:
    """
    Classe unificada para extrair, analisar e visualizar dados de personagens de um texto.
    """
    def __init__(self):
        """Inicializa o analisador, carregando os modelos necessários."""
        self.nlp = self._carregar_modelo_spacy()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.resultados = self._inicializar_resultados()
        self.total_caracteres = 0

    @staticmethod
    def _carregar_modelo_spacy():
        """
        Carrega o modelo de linguagem do spaCy, que deve ser pré-instalado.
        """
        modelo = "pt_core_news_sm"
        try:
            return spacy.load(modelo)
        except OSError:
            # Em um ambiente de deploy, este erro significa que o modelo
            # não foi instalado corretamente via requirements.txt
            raise RuntimeError(
                f"O modelo spaCy '{modelo}' não foi encontrado. "
                f"Certifique-se de que ele está listado corretamente em seu arquivo requirements.txt."
            )

    def _inicializar_resultados(self):
        """Retorna a estrutura de dados para armazenar os resultados da análise."""
        return {
            "frequencia": Counter(),
            "sentimentos": defaultdict(list),
            "posicoes": defaultdict(list),
            "relacionamentos": Counter()
        }

    def _limpar_nome(self, nome_texto):
        """Remove títulos e excesso de espaços para agrupar nomes de personagens."""
        titulos = [
            'Sor', 'Lorde', 'Lady', 'Rei', 'Rainha', 'Senhor', 'Senhora',
            'Príncipe', 'Princesa', 'Dom', 'Dona'
        ]
        # Expressão regular para remover os títulos como palavras inteiras
        padrao = r'\b(' + '|'.join(titulos) + r')\b'
        nome_limpo = re.sub(padrao, '', nome_texto, flags=re.IGNORECASE)
        return nome_limpo.strip()

    def analisar_livro(self, pdf_input, tamanho_chunk=100000):
        """
        Processa um livro a partir de bytes de um arquivo PDF ou de um caminho de arquivo.
        
        Args:
            pdf_input (bytes or str): Os bytes do arquivo PDF ou o caminho para ele.
            tamanho_chunk (int): O tamanho dos blocos de texto a serem processados por vez.
        """
        self.resultados = self._inicializar_resultados()
        texto_completo = ""
        try:
            if isinstance(pdf_input, bytes):
                # Processa a partir de bytes (ideal para Streamlit)
                doc_pdf = fitz.open(stream=pdf_input, filetype="pdf")
            else:
                # Processa a partir de um caminho de arquivo (ideal para linha de comando)
                doc_pdf = fitz.open(pdf_input)
            
            with doc_pdf:
                texto_completo = "".join([page.get_text() for page in doc_pdf])
            
            self.total_caracteres = len(texto_completo)
            if self.total_caracteres == 0:
                raise ValueError("O PDF parece estar vazio ou não contém texto extraível.")

        except Exception as e:
            raise ValueError(f"Erro ao ler ou processar o arquivo PDF: {e}")

        # Processamento em chunks para otimizar o uso de memória
        for i in range(0, self.total_caracteres, tamanho_chunk):
            chunk_texto = texto_completo[i:i + tamanho_chunk]
            doc_nlp = self.nlp(chunk_texto)
            
            for sent in doc_nlp.sents:
                personagens_na_frase = {
                    self._limpar_nome(ent.text) for ent in sent.ents 
                    if ent.label_ == "PER" and len(self._limpar_nome(ent.text).split()) < 4 and len(self._limpar_nome(ent.text)) > 2
                }
                
                if not personagens_na_frase:
                    continue
                
                # Análise de sentimento da frase
                sentimento = self.sentiment_analyzer.polarity_scores(sent.text)['compound']
                
                # Armazenamento dos dados
                for p in personagens_na_frase:
                    posicao_absoluta = i + sent.start_char
                    self.resultados["frequencia"][p] += 1
                    self.resultados["posicoes"][p].append(posicao_absoluta)
                    self.resultados["sentimentos"][p].append(sentimento)
                
                # Registro de relacionamentos (coocorrência na mesma frase)
                if len(personagens_na_frase) > 1:
                    for par in combinations(sorted(list(personagens_na_frase)), 2):
                        self.resultados["relacionamentos"][par] += 1
            
            gc.collect() # Libera memória após processar cada chunk

    # --- MÉTODOS DE GERAÇÃO DE GRÁFICOS (RETORNANDO OBJETOS FIG/HTML) ---
    
    def gerar_grafico_frequencia(self, top_n=25):
        """Gera um gráfico de barras com a frequência dos personagens."""
        mais_comuns = self.resultados["frequencia"].most_common(top_n)
        if not mais_comuns: return None
        
        df = pd.DataFrame(mais_comuns, columns=['Personagem', 'Frequência'])
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='Frequência', y='Personagem', data=df, palette='viridis', ax=ax)
        ax.set_title(f'Top {top_n} Personagens Mais Frequentes', fontsize=16)
        plt.tight_layout()
        return fig

    def gerar_grafico_dispersao(self, top_n=15):
        """Gera um gráfico de dispersão para mostrar onde os personagens aparecem no texto."""
        personagens_principais = [p for p, _ in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais: return None

        n_personagens = len(personagens_principais)
        fig, axes = plt.subplots(n_personagens, 1, figsize=(14, 2 * n_personagens), sharex=True)
        if n_personagens == 1: axes = [axes]

        cores = plt.cm.viridis(np.linspace(0, 1, n_personagens))
        for i, personagem in enumerate(personagens_principais):
            ax = axes[i]
            posicoes_norm = [(p / self.total_caracteres) * 100 for p in self.resultados["posicoes"].get(personagem, [])]
            
            if posicoes_norm:
                ax.vlines(posicoes_norm, ymin=0, ymax=1, color=cores[i], alpha=0.7)
            
            ax.set_yticks([])
            ax.set_ylabel(personagem, rotation=0, ha='right', va='center', fontweight='bold')
            ax.set_xlim(0, 100)
        
        if axes.size > 0:
            axes[0].set_title('Dispersão de Aparições dos Personagens', fontsize=16, pad=20)
            axes[-1].set_xlabel('Posição no Texto (%)')
        
        plt.tight_layout()
        return fig

    def gerar_grafico_evolucao_dinamico(self, personagens_selecionados):
        """Gera um gráfico de densidade (KDE) para a evolução de personagens selecionados."""
        if not personagens_selecionados: return None
        
        fig, ax = plt.subplots(figsize=(14, 8))
        cores = plt.cm.tab10(np.linspace(0, 1, len(personagens_selecionados)))
        
        for i, personagem in enumerate(personagens_selecionados):
            posicoes_norm = [(p / self.total_caracteres) * 100 for p in self.resultados["posicoes"].get(personagem, [])]
            if posicoes_norm:
                sns.kdeplot(posicoes_norm, label=personagem, fill=True, alpha=0.3, color=cores[i], ax=ax, linewidth=2)
        
        ax.set_title('Evolução das Menções ao Longo do Livro', fontsize=16)
        ax.set_xlabel('Posição no Texto (%)', fontsize=12)
        ax.set_ylabel('Densidade de Menções', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
        
    def gerar_grafico_sentimentos(self, top_n=25):
        """Gera um gráfico de barras com o sentimento médio associado a cada personagem."""
        personagens_principais = [p for p, _ in self.resultados["frequencia"].most_common(top_n)]
        sentimentos_medios = {p: np.mean(self.resultados["sentimentos"][p]) for p in personagens_principais if self.resultados["sentimentos"].get(p)}
        
        if not sentimentos_medios: return None
        
        df = pd.DataFrame(list(sentimentos_medios.items()), columns=['Personagem', 'Sentimento Médio']).sort_values('Sentimento Médio', ascending=False)
        cores = ['#2ca02c' if s > 0.05 else '#d62728' if s < -0.05 else '#7f7f7f' for s in df['Sentimento Médio']]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='Sentimento Médio', y='Personagem', data=df, palette=cores, ax=ax)
        ax.set_title('Análise de Sentimento Médio por Personagem', fontsize=16)
        ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
        ax.set_xlim(-1, 1)
        plt.tight_layout()
        return fig

    def _criar_grafo_base(self, top_n):
        """Helper para criar um grafo NetworkX com os personagens e relacionamentos."""
        personagens_principais = {p for p, _ in self.resultados["frequencia"].most_common(top_n)}
        if not personagens_principais:
            return None

        G = nx.Graph()
        # Adiciona nós com tamanho baseado na frequência
        for p in personagens_principais:
            freq = self.resultados["frequencia"][p]
            G.add_node(p, size=np.log1p(freq) * 5, title=f"Menções: {freq}")
        
        # Adiciona arestas com peso baseado na força da interação
        for par, peso in self.resultados["relacionamentos"].items():
            if par[0] in G and par[1] in G:
                G.add_edge(par[0], par[1], weight=peso, title=f"Interações: {peso}")
        
        G.remove_nodes_from(list(nx.isolates(G))) # Remove personagens sem conexão
        return G if G.number_of_nodes() > 0 else None

    def gerar_rede_relacionamentos(self, top_n=30):
        """Gera um grafo interativo da rede de relacionamentos."""
        G = self._criar_grafo_base(top_n)
        if not G: return None
        
        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        net.set_options("""
        var options = {
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -100,
              "centralGravity": 0.01,
              "springLength": 200
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """)
        return net.generate_html(notebook=False)

    def gerar_rede_comunidades(self, top_n=50):
        """Gera um grafo interativo com detecção de comunidades (grupos)."""
        if not community_louvain:
            print("Função 'gerar_rede_comunidades' desabilitada pois 'python-louvain' não está instalado.")
            return None

        G = self._criar_grafo_base(top_n)
        if not G: return None

        partition = community_louvain.best_partition(G, weight='weight')
        for node, comm_id in partition.items():
            G.nodes[node]['group'] = comm_id
            G.nodes[node]['title'] += f"<br>Comunidade: {comm_id}"

        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        return net.generate_html(notebook=False)
        
    def analisar_pontes_narrativas(self, top_n=10):
        """Identifica personagens-ponte através da centralidade de intermediação."""
        G = self._criar_grafo_base(top_n=50) # Usa um grafo maior para a análise de centralidade
        if not G: return None

        # Calcula a centralidade
        betweenness = nx.betweenness_centrality(G, weight='weight', normalized=True)
        
        df_pontes = pd.DataFrame(list(betweenness.items()), columns=['Personagem', 'Centralidade de Intermediação'])
        return df_pontes.sort_values('Centralidade de Intermediação', ascending=False).head(top_n)

    def obter_estatisticas_comunidades(self, top_n=50):
        """Calcula e retorna estatísticas detalhadas para cada comunidade detectada."""
        if not community_louvain: return None

        G = self._criar_grafo_base(top_n)
        if not G: return None

        partition = community_louvain.best_partition(G, weight='weight')
        stats = defaultdict(lambda: {
            'personagens': [], 'frequencia_total': 0, 
            'interacoes_internas': 0, 'interacoes_externas': 0
        })

        for node, comm_id in partition.items():
            freq = self.resultados["frequencia"][node]
            stats[comm_id]['personagens'].append((node, freq))
            stats[comm_id]['frequencia_total'] += freq

        for p1, p2, data in G.edges(data=True):
            peso = data.get('weight', 1)
            comm1, comm2 = partition[p1], partition[p2]
            if comm1 == comm2:
                stats[comm1]['interacoes_internas'] += peso
            else:
                stats[comm1]['interacoes_externas'] += peso
                stats[comm2]['interacoes_externas'] += peso
        
        for comm_id in stats:
            stats[comm_id]['personagens'].sort(key=lambda x: x[1], reverse=True)

        return stats


# --- BLOCO DE EXECUÇÃO (PARA TESTES E USO EM LINHA DE COMANDO) ---

if __name__ == '__main__':
    print("Executando o analisador em modo de linha de comando...")
    
    # Coloque o nome do arquivo PDF na mesma pasta ou o caminho completo
    NOME_ARQUIVO_PDF = "dom_casmurro.pdf" 
    
    if not os.path.exists(NOME_ARQUIVO_PDF):
        print(f"ERRO: Arquivo '{NOME_ARQUIVO_PDF}' não encontrado.")
    else:
        start_time = time.time()
        
        # 1. Inicia e executa a análise
        analisador = AnalisadorDePersonagens()
        print(f"Analisando '{NOME_ARQUIVO_PDF}'...")
        analisador.analisar_livro(NOME_ARQUIVO_PDF)
        print("Análise do texto concluída.")
        
        # 2. Gera e salva todos os resultados
        output_dir = Path("resultados_analise")
        output_dir.mkdir(exist_ok=True)
        print(f"Salvando resultados na pasta: '{output_dir}'")
        
        # Gráficos Matplotlib
        for nome_metodo, nome_arquivo in [
            ('gerar_grafico_frequencia', 'frequencia.png'),
            ('gerar_grafico_dispersao', 'dispersao.png'),
            ('gerar_grafico_sentimentos', 'sentimentos.png')
        ]:
            fig = getattr(analisador, nome_metodo)()
            if fig:
                fig.savefig(output_dir / nome_arquivo)
                plt.close(fig)
        
        # Grafos HTML
        for nome_metodo, nome_arquivo in [
            ('gerar_rede_relacionamentos', 'rede_relacionamentos.html'),
            ('gerar_rede_comunidades', 'rede_comunidades.html')
        ]:
            html_content = getattr(analisador, nome_metodo)()
            if html_content:
                with open(output_dir / nome_arquivo, 'w', encoding='utf-8') as f:
                    f.write(html_content)

        # DataFrame CSV
        df_pontes = analisador.analisar_pontes_narrativas()
        if df_pontes is not None:
            df_pontes.to_csv(output_dir / "personagens_ponte.csv", index=False)
            
        end_time = time.time()
        print(f"\nAnálise completa em {end_time - start_time:.2f} segundos.")