#
# arquivo: analisador_personagens.py
#
# ==============================================================================
# MÓDULO DE ANÁLISE NLP (CORREÇÃO PARA PYVIS)
# ==============================================================================

import spacy
import fitz  # PyMuPDF
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from leia.leia import SentimentIntensityAnalyzer
import networkx as nx
from pyvis.network import Network
from tqdm import tqdm
import gc
from pathlib import Path
import re
from itertools import combinations
import os # Importado para manipulação de arquivos temporários

class AnalisadorDePersonagens:
    """
    Classe de lógica de análise. Modificada para retornar objetos para o Streamlit.
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
        try:
            return spacy.load("pt_core_news_lg")
        except OSError:
            raise OSError("Modelo 'pt_core_news_lg' não encontrado. Por favor, execute no seu terminal: python -m spacy download pt_core_news_lg")

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

    def gerar_rede_relacionamentos(self, top_n=30):
        """Modificado para salvar em um arquivo temporário e ler o HTML de volta."""
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais: return None
        
        G = nx.Graph()
        for personagem in personagens_principais:
            G.add_node(personagem, size=self.resultados["frequencia"][personagem], title=f"{personagem}\nMenções: {self.resultados['frequencia'][personagem]}")

        for par, peso in self.resultados["relacionamentos"].items():
            p1, p2 = par
            if p1 in G and p2 in G: G.add_edge(p1, p2, weight=peso, title=f"Interações: {peso}")

        G.remove_nodes_from(list(nx.isolates(G)))
        
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        
        # --- CORREÇÃO APLICADA AQUI ---
        # 1. Salva o grafo em um arquivo HTML com nome fixo.
        caminho_arquivo_html = "rede_temp.html"
        net.write_html(caminho_arquivo_html)

        # 2. Lê o conteúdo do arquivo de volta para uma variável.
        with open(caminho_arquivo_html, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. (Opcional) Remove o arquivo temporário se não quiser que ele fique na pasta.
        # os.remove(caminho_arquivo_html)
            
        # 4. Retorna o conteúdo HTML para ser renderizado pelo Streamlit.
        return html_content