import spacy
import fitz  # PyMuPDF
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
from leia.leia import SentimentIntensityAnalyzer # <-- Dependência para análise de sentimentos
import networkx as nx
from pyvis.network import Network
from tqdm import tqdm
import gc
from pathlib import Path
import re
from itertools import combinations
import os
import community.community_louvain as community_louvain
import time

# --- CLASSE DE LÓGICA DE ANÁLISE ---
class AnalisadorDePersonagens:
    """
    Classe completa de lógica de análise, incluindo sentimentos.
    """
    def __init__(self):
        print("Inicializando o analisador...")
        self.nlp = self.carregar_modelo_spacy()
        self.sentiment_analyzer = SentimentIntensityAnalyzer() # <-- Inicializa o analisador de sentimentos
        self.resultados = {
            "frequencia": Counter(), "sentimentos": defaultdict(list),
            "posicoes": defaultdict(list), "relacionamentos": Counter()
        }
        self.total_caracteres = 0
        print("Analisador pronto.")

    @staticmethod
    def carregar_modelo_spacy():
        """Carrega o modelo Spacy pt_core_news_sm."""
        print("Carregando modelo spaCy 'pt_core_news_sm'...")
        try:
            return spacy.load("pt_core_news_sm")
        except OSError:
            print("Modelo não encontrado. Baixando...")
            import subprocess
            subprocess.check_call(["python", "-m", "spacy", "download", "pt_core_news_sm"])
            return spacy.load("pt_core_news_sm")

    def _limpar_nome(self, nome_texto):
        """Remove títulos honoríficos dos nomes para agrupar melhor os personagens."""
        titulos = ['Sor', 'Lorde', 'Lady', 'Rei', 'Rainha', 'Senhor', 'Senhora', 'Príncipe', 'Princesa']
        for titulo in titulos:
            nome_texto = re.sub(r'\b' + titulo + r'\b', '', nome_texto, flags=re.IGNORECASE)
        return nome_texto.strip()

    def analisar_livro(self, caminho_pdf, tamanho_chunk=50000):
        """Processa o livro a partir de um caminho de arquivo PDF."""
        print(f"Lendo o arquivo: {caminho_pdf}")
        try:
            with fitz.open(caminho_pdf) as doc_pdf:
                texto_completo = "".join([page.get_text() for page in doc_pdf])
            self.total_caracteres = len(texto_completo)
            print(f"Leitura concluída. Total de {self.total_caracteres} caracteres.")
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo PDF: {e}")

        # Usando tqdm para mostrar uma barra de progresso no terminal
        print("Analisando o texto...")
        for i in tqdm(range(0, self.total_caracteres, tamanho_chunk), desc="Processando chunks de texto"):
            chunk_texto = texto_completo[i:i+tamanho_chunk]
            doc_nlp = self.nlp(chunk_texto)
            for sent in doc_nlp.sents:
                # Identifica personagens (entidades PER) na frase
                personagens_na_frase = {self._limpar_nome(ent.text) for ent in sent.ents if ent.label_ == "PER" and len(self._limpar_nome(ent.text)) > 2}
                if not personagens_na_frase:
                    continue
                
                # Calcula o sentimento da frase
                sentimento = self.sentiment_analyzer.polarity_scores(sent.text)['compound']

                # Armazena os dados
                for p in personagens_na_frase:
                    self.resultados["frequencia"][p] += 1
                    self.resultados["posicoes"][p].append(i + sent.start_char)
                    self.resultados["sentimentos"][p].append(sentimento) # <-- Armazena o sentimento

                # Registra as interações entre personagens na mesma frase
                if len(personagens_na_frase) > 1:
                    for par in combinations(sorted(list(personagens_na_frase)), 2):
                        self.resultados["relacionamentos"][par] += 1
            gc.collect()
        print("Análise principal concluída.")

    # --- MÉTODOS DE GERAÇÃO DE GRÁFICOS (salvando em arquivos) ---
    
    def gerar_grafico_frequencia(self, top_n=25, salvar_em="grafico_frequencia.png"):
        print("Gerando gráfico de frequência...")
        mais_comuns = self.resultados["frequencia"].most_common(top_n)
        if not mais_comuns: return
        df = pd.DataFrame(mais_comuns, columns=['Personagem', 'Frequência'])
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='Frequência', y='Personagem', data=df, palette='viridis', ax=ax)
        ax.set_title(f'Top {top_n} Personagens Mais Frequentes', fontsize=16)
        plt.tight_layout()
        fig.savefig(salvar_em)
        plt.close(fig)
        print(f"Gráfico salvo em: {salvar_em}")

    def gerar_grafico_sentimentos(self, top_n=25, salvar_em="grafico_sentimentos.png"):
        print("Gerando gráfico de sentimentos...")
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        sentimentos_medios = {p: np.mean(self.resultados["sentimentos"][p]) for p in personagens_principais if self.resultados["sentimentos"][p]}
        if not sentimentos_medios: return
        df = pd.DataFrame(list(sentimentos_medios.items()), columns=['Personagem', 'Sentimento Médio']).sort_values('Sentimento Médio', ascending=False)
        cores = ['#2ca02c' if s > 0.05 else '#d62728' if s < -0.05 else '#7f7f7f' for s in df['Sentimento Médio']]
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='Sentimento Médio', y='Personagem', data=df, palette=cores, ax=ax)
        ax.set_title('Análise de Sentimento Médio por Personagem', fontsize=16)
        ax.set_xlim(-1, 1)
        ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
        plt.tight_layout()
        fig.savefig(salvar_em)
        plt.close(fig)
        print(f"Gráfico salvo em: {salvar_em}")

    def gerar_grafico_dispersao(self, top_n=15, salvar_em="grafico_dispersao.png"):
        print("Gerando gráfico de dispersão...")
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais: return
        n_personagens = len(personagens_principais)
        fig, axes = plt.subplots(n_personagens, 1, figsize=(14, 2 * n_personagens), sharex=True)
        if n_personagens == 1: axes = [axes]
        cores = plt.cm.tab10(np.linspace(0, 1, n_personagens))
        for i, personagem in enumerate(personagens_principais):
            ax = axes[i]
            posicoes = self.resultados["posicoes"][personagem]
            if posicoes:
                posicoes_norm = [(p / self.total_caracteres) * 100 for p in posicoes]
                ax.vlines(posicoes_norm, ymin=0, ymax=1, color=cores[i], alpha=0.7, linewidth=1.5)
            ax.set_yticks([])
            ax.set_ylabel(personagem, rotation=0, ha='right', va='center', fontweight='bold')
            ax.set_xlim(0, 100)
            if i == 0: ax.set_title('Dispersão de Aparições dos Personagens', fontsize=16, pad=20)
        axes[-1].set_xlabel('Posição no Texto (%)')
        plt.tight_layout()
        fig.savefig(salvar_em)
        plt.close(fig)
        print(f"Gráfico salvo em: {salvar_em}")

    def gerar_rede_relacionamentos(self, top_n=30, salvar_em="rede_relacionamentos.html"):
        print("Gerando rede de relacionamentos...")
        G = nx.Graph()
        personagens_principais = {p for p, f in self.resultados["frequencia"].most_common(top_n)}
        for p in personagens_principais:
            G.add_node(p, size=self.resultados["frequencia"][p], title=f"Menções: {self.resultados['frequencia'][p]}")
        for par, peso in self.resultados["relacionamentos"].items():
            if par[0] in G and par[1] in G:
                G.add_edge(par[0], par[1], weight=peso, title=f"Interações: {peso}")
        G.remove_nodes_from(list(nx.isolates(G)))
        if G.number_of_nodes() == 0: return

        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True)
        net.from_nx(G)
        net.write_html(salvar_em)
        print(f"Rede interativa salva em: {salvar_em}")

    def gerar_rede_comunidades(self, top_n=50, salvar_em="rede_comunidades.html"):
        print("Gerando rede de comunidades...")
        G = nx.Graph()
        personagens_principais = {p for p, f in self.resultados["frequencia"].most_common(top_n)}
        for p in personagens_principais:
             G.add_node(p)
        for par, peso in self.resultados["relacionamentos"].items():
            if par[0] in G and par[1] in G:
                G.add_edge(par[0], par[1], weight=peso)
        G.remove_nodes_from(list(nx.isolates(G)))
        if G.number_of_nodes() == 0: return

        partition = community_louvain.best_partition(G, weight='weight')
        num_comunidades = len(set(partition.values()))
        print(f"Detectadas {num_comunidades} comunidades.")

        for node in G.nodes():
            G.nodes[node]['group'] = partition[node]
            G.nodes[node]['size'] = self.resultados["frequencia"][node]
        
        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True)
        net.from_nx(G)
        net.write_html(salvar_em)
        print(f"Rede de comunidades salva em: {salvar_em}")
    
    def analisar_pontes_narrativas(self, top_n=10):
        print("Analisando personagens-ponte...")
        G = nx.Graph()
        personagens_principais = {p for p, f in self.resultados["frequencia"].most_common(50)}
        for par, peso in self.resultados["relacionamentos"].items():
            if par[0] in personagens_principais and par[1] in personagens_principais:
                G.add_edge(par[0], par[1], weight=1/peso) # Inverso do peso para centralidade
        if G.number_of_nodes() == 0: return None
        
        betweenness = nx.betweenness_centrality(G, weight='weight', normalized=True)
        df_pontes = pd.DataFrame(list(betweenness.items()), columns=['Personagem', 'Centralidade'])
        df_pontes = df_pontes.sort_values('Centralidade', ascending=False).head(top_n)
        
        print("--- Personagens-Ponte (Maior Centralidade) ---")
        print(df_pontes)
        print("---------------------------------------------")
        return df_pontes

# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    # --- CONFIGURAÇÃO ---
    # Coloque o nome do seu arquivo PDF aqui
    NOME_ARQUIVO_PDF = "dom_casmurro.pdf"  # Arquivo na mesma pasta

    if not os.path.exists(NOME_ARQUIVO_PDF):
        print(f"ERRO: Arquivo '{NOME_ARQUIVO_PDF}' não encontrado.")
        print("Por favor, coloque o PDF na mesma pasta do script ou atualize a variável NOME_ARQUIVO_PDF.")
        print("Exemplo de uso: NOME_ARQUIVO_PDF = 'caminho/para/seu/arquivo.pdf'")
    else:
        start_time = time.time()
        
        # 1. Iniciar a análise
        analisador = AnalisadorDePersonagens()
        analisador.analisar_livro(NOME_ARQUIVO_PDF)
        
        # 2. Gerar todos os resultados
        analisador.gerar_grafico_frequencia()
        analisador.gerar_grafico_sentimentos() # <-- Gráfico de sentimentos incluído
        analisador.gerar_grafico_dispersao()
        analisador.gerar_rede_relacionamentos()
        analisador.gerar_rede_comunidades()
        analisador.analisar_pontes_narrativas()

        end_time = time.time()
        print(f"\nAnálise completa concluída em {end_time - start_time:.2f} segundos.")
        print("Verifique os arquivos .png e .html gerados na pasta.")