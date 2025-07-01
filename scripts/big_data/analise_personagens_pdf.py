# ==============================================================================
# ANALISADOR AVANÇADO DE LIVROS EM PDF - VERSÃO FINAL (VALIDADA)
#
# Utiliza SpaCy para NLP, LeIA para Sentimento e NetworkX/Pyvis para Grafos
#
# Autor: Gemini (adaptado da sua ideia original)
# Data: 30 de junho de 2025
# ==============================================================================

import spacy
import fitz  # PyMuPDF
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from leia.leia import SentimentIntensityAnalyzer  # <-- A FORMA CORRETA, VALIDADA PELO SEU SISTEMA
import networkx as nx
from pyvis.network import Network
from tqdm import tqdm
import gc
from pathlib import Path
import re

class AnalisadorDePersonagensAvancado:
    """
    Uma classe para realizar uma análise NLP completa de um livro em PDF,
    focando em personagens, seus sentimentos e relacionamentos.
    """
    def __init__(self):
        print("Inicializando o analisador avançado...")
        print("Carregando modelo de linguagem SpaCy (pt_core_news_lg). Isso pode levar um momento...")
        try:
            self.nlp = spacy.load("pt_core_news_lg")
        except OSError:
            print("ERRO: Modelo 'pt_core_news_lg' não encontrado.")
            print("Por favor, execute no seu terminal: python -m spacy download pt_core_news_lg")
            exit()
            
        self.sentiment_analyzer = SentimentIntensityAnalyzer()  # <-- A FORMA CORRETA, VALIDADA PELO SEU SISTEMA
        self.resultados = {
            "frequencia": Counter(),
            "sentimentos": defaultdict(list),
            "posicoes": defaultdict(list),
            "relacionamentos": Counter()
        }
        self.total_caracteres = 0
        print("Analisador pronto.")

    def _limpar_nome(self, nome_texto):
        """Normaliza nomes de personagens para contagem consistente."""
        titulos = ['Sor', 'Lorde', 'Lady', 'Rei', 'Rainha', 'Senhor', 'Senhora', 'Príncipe', 'Princesa']
        for titulo in titulos:
            nome_texto = re.sub(r'\b' + titulo + r'\b', '', nome_texto, flags=re.IGNORECASE)
        return nome_texto.strip()

    def analisar_livro(self, caminho_pdf, tamanho_chunk=50000):
        """
        Processa o livro em chunks para analisar personagens, sentimentos e relações.
        """
        print(f"Abrindo e processando o livro: {caminho_pdf}")
        try:
            doc_pdf = fitz.open(caminho_pdf)
            texto_completo = "".join([page.get_text() for page in doc_pdf])
            self.total_caracteres = len(texto_completo)
            doc_pdf.close()
        except Exception as e:
            print(f"Erro ao ler o arquivo PDF: {e}")
            return

        print(f"Total de caracteres no livro: {self.total_caracteres}")
        print("Iniciando a análise NLP. Isso pode levar vários minutos dependendo do tamanho do livro e do seu computador.")

        for i in tqdm(range(0, self.total_caracteres, tamanho_chunk), desc="Analisando o Texto"):
            chunk_texto = texto_completo[i:i+tamanho_chunk]
            doc_nlp = self.nlp(chunk_texto)

            personagens_no_chunk = []
            for ent in doc_nlp.ents:
                if ent.label_ == "PER":
                    nome_limpo = self._limpar_nome(ent.text)
                    if len(nome_limpo) > 2:
                        personagens_no_chunk.append(nome_limpo)
                        posicao_global = i + ent.start_char
                        self.resultados["posicoes"][nome_limpo].append(posicao_global)
            
            self.resultados["frequencia"].update(personagens_no_chunk)

            for sent in doc_nlp.sents:
                personagens_na_frase = {self._limpar_nome(ent.text) for ent in sent.ents if ent.label_ == "PER" and len(self._limpar_nome(ent.text)) > 2}
                
                if not personagens_na_frase:
                    continue

                sentimento = self.sentiment_analyzer.polarity_scores(sent.text)['compound']
                for personagem in personagens_na_frase:
                    self.resultados["sentimentos"][personagem].append(sentimento)

                if len(personagens_na_frase) > 1:
                    from itertools import combinations
                    for par in combinations(sorted(list(personagens_na_frase)), 2):
                        self.resultados["relacionamentos"][par] += 1
            
            gc.collect()
        
        print("Análise concluída com sucesso!")

    def gerar_grafico_frequencia(self, top_n=25, caminho_salvar="resultados/grafico_frequencia.png"):
        """Gera e salva um gráfico de barras com os personagens mais frequentes."""
        print(f"Gerando gráfico de frequência para os Top {top_n} personagens...")
        mais_comuns = self.resultados["frequencia"].most_common(top_n)
        if not mais_comuns:
            print("Nenhum personagem encontrado para gerar gráfico de frequência.")
            return
        df = pd.DataFrame(mais_comuns, columns=['Personagem', 'Frequência'])
        
        plt.figure(figsize=(15, 10))
        sns.barplot(x='Frequência', y='Personagem', data=df, palette='viridis')
        plt.title(f'Top {top_n} Personagens Mais Frequentes', fontsize=16)
        plt.xlabel('Número de Menções', fontsize=12)
        plt.ylabel('Personagem', fontsize=12)
        plt.tight_layout()
        
        Path(caminho_salvar).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(caminho_salvar, dpi=300)
        plt.close()
        print(f"Gráfico de frequência salvo em: {caminho_salvar}")

    def gerar_grafico_evolucao(self, top_n=10, caminho_salvar="resultados/grafico_evolucao.png"):
        """Gera um gráfico de densidade para mostrar a evolução das menções ao longo do livro."""
        print(f"Gerando gráfico de evolução para os Top {top_n} personagens...")
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais:
            print("Nenhum personagem encontrado para gerar gráfico de evolução.")
            return

        plt.figure(figsize=(15, 8))
        for personagem in personagens_principais:
            posicoes_norm = [(p / self.total_caracteres) * 100 for p in self.resultados["posicoes"][personagem]]
            if posicoes_norm:
                sns.kdeplot(posicoes_norm, label=personagem, fill=True, alpha=0.2)
        
        plt.title('Evolução dos Personagens ao Longo do Livro (Densidade de Menções)', fontsize=16)
        plt.xlabel('Posição no Texto (%)', fontsize=12)
        plt.ylabel('Densidade', fontsize=12)
        plt.legend()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        Path(caminho_salvar).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(caminho_salvar, dpi=300)
        plt.close()
        print(f"Gráfico de evolução salvo em: {caminho_salvar}")

    def gerar_grafico_sentimentos(self, top_n=25, caminho_salvar="resultados/grafico_sentimentos.png"):
        """Calcula o sentimento médio e gera um gráfico de barras."""
        print(f"Gerando gráfico de sentimentos para os Top {top_n} personagens...")
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        
        sentimentos_medios = {}
        for p in personagens_principais:
            scores = self.resultados["sentimentos"][p]
            if scores:
                sentimentos_medios[p] = sum(scores) / len(scores)
        
        if not sentimentos_medios:
            print("Não há dados de sentimento para gerar o gráfico.")
            return

        df = pd.DataFrame(list(sentimentos_medios.items()), columns=['Personagem', 'Sentimento Médio']).sort_values('Sentimento Médio', ascending=False)
        cores = ['#2ca02c' if s > 0.05 else '#d62728' if s < -0.05 else '#7f7f7f' for s in df['Sentimento Médio']]
        
        plt.figure(figsize=(15, 10))
        sns.barplot(x='Sentimento Médio', y='Personagem', data=df, palette=cores)
        plt.title('Análise de Sentimento Médio por Personagem', fontsize=16)
        plt.xlabel('Sentimento Médio (Negativo < 0 < Positivo)', fontsize=12)
        plt.ylabel('Personagem', fontsize=12)
        plt.xlim(-1, 1)
        plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
        plt.tight_layout()
        
        Path(caminho_salvar).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(caminho_salvar, dpi=300)
        plt.close()
        print(f"Gráfico de sentimentos salvo em: {caminho_salvar}")

    def gerar_rede_relacionamentos(self, top_n=30, caminho_salvar="resultados/rede_relacionamentos.html"):
        """Gera um grafo interativo de relacionamentos."""
        print(f"Gerando rede de relacionamentos para os Top {top_n} personagens...")
        personagens_principais = [p for p, f in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais:
            print("Nenhum personagem encontrado para gerar a rede de relacionamentos.")
            return

        G = nx.Graph()
        for personagem in personagens_principais:
            G.add_node(personagem, size=self.resultados["frequencia"][personagem], title=f"{personagem}\nMenções: {self.resultados['frequencia'][personagem]}")

        for par, peso in self.resultados["relacionamentos"].items():
            p1, p2 = par
            if p1 in G and p2 in G:
                G.add_edge(p1, p2, weight=peso, title=f"Interações: {peso}")

        G.remove_nodes_from(list(nx.isolates(G)))

        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
        net.from_nx(G)
        
        net.set_options("""
        var options = {
          "nodes": { "font": { "size": 18 } },
          "edges": { "color": { "inherit": true }, "smooth": false },
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -100, "centralGravity": 0.01,
              "springLength": 200, "springConstant": 0.09, "avoidOverlap": 1
            },
            "minVelocity": 0.75, "solver": "forceAtlas2Based"
          }
        }
        """)

        Path(caminho_salvar).parent.mkdir(parents=True, exist_ok=True)
        net.save_graph(caminho_salvar)
        print(f"Rede de relacionamentos interativa salva em: {caminho_salvar}")
        print("Abra este arquivo HTML em seu navegador!")

    def executar_analise_completa(self, caminho_pdf):
        """Orquestra a execução de todas as etapas da análise."""
        self.analisar_livro(caminho_pdf)
        if not self.resultados["frequencia"]:
            print("\nAnálise não encontrou personagens. Encerrando.")
            return
        self.gerar_grafico_frequencia(top_n=25)
        self.gerar_grafico_sentimentos(top_n=25)
        self.gerar_grafico_evolucao(top_n=10)
        self.gerar_rede_relacionamentos(top_n=30)
        print("\n\nAnálise completa! Verifique a pasta 'resultados' para os gráficos e a rede interativa.")

# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================
if __name__ == "__main__":
    caminho_da_pasta = r"C:\Users\tabat\Documents\GitHub\introducao_data_science\dados"
    
    pasta_dados = Path(caminho_da_pasta)

    if not pasta_dados.is_dir():
        print(f"ERRO: O diretório especificado não foi encontrado em '{caminho_da_pasta}'")
        print("Por favor, verifique se o caminho está correto.")
    else:
        print(f"Procurando por arquivos PDF em: {caminho_da_pasta}")
        pdfs_encontrados = list(pasta_dados.glob("*.pdf"))

        if not pdfs_encontrados:
            print(f"ERRO: Nenhum arquivo PDF foi encontrado no diretório '{caminho_da_pasta}'.")
            print("Por favor, adicione um livro em formato PDF a esta pasta.")
        else:
            primeiro_pdf = pdfs_encontrados[0]
            print(f"Arquivo PDF encontrado para análise: {primeiro_pdf.name}\n")
            
            analisador = AnalisadorDePersonagensAvancado()
            analisador.executar_analise_completa(str(primeiro_pdf))