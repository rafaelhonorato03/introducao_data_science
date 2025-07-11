# -*- coding: utf-8 -*-
"""
Script Unificado para Análise de Texto e Visualização de Redes.

Este script combina técnicas de Processamento de Linguagem Natural (PLN) e
Análise de Redes para extrair insights de um texto.

Fluxo de Trabalho:
1.  Carrega um texto e o divide em sentenças.
2.  Realiza uma análise de sentimento em todo o texto e plota os resultados.
3.  Identifica as palavras (substantivos/nomes) mais frequentes.
4.  Constrói uma rede onde os nós são as palavras e as arestas representam
    a coocorrência (aparição na mesma sentença).
5.  Visualiza a rede completa e a rede "ego" do nó mais central (hub).
"""

# --- 1. IMPORTAÇÃO DAS BIBLIOTECAS ---
import re
import pandas as pd
import nltk
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from operator import itemgetter

# --- 2. CONFIGURAÇÕES E CARREGAMENTO DE DADOS ---

# Tenta baixar os recursos necessários do NLTK se não existirem
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Baixando o léxico 'vader_lexicon' do NLTK...")
    nltk.download('vader_lexicon')

# Função para carregar o texto de um arquivo
def carregar_texto(caminho_arquivo):
    """Tenta carregar um arquivo de texto. Se falhar, retorna um texto de exemplo."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            print(f"Arquivo '{caminho_arquivo}' carregado com sucesso.")
            return f.read()
    except FileNotFoundError:
        print(f"AVISO: Arquivo '{caminho_arquivo}' não encontrado.")
        print("Usando um texto de exemplo para demonstração.")
        return """
        Capitu e Bentinho eram amigos de infância. Suas famílias moravam perto,
        e a amizade floresceu em amor. Bentinho, prometido ao seminário,
        sentia-se dividido. José Dias, o agregado da família, sempre opinava
        sobre o futuro de Bentinho. A mãe de Bentinho, Dona Glória, era devota
        e insistia na promessa. Escobar, amigo de seminário de Bentinho,
        tornou-se uma figura central em sua vida, casando-se com Sancha.
        A relação entre Escobar e Capitu sempre foi uma fonte de ciúmes para
        Bentinho, culminando na trágica desconfiança que marcou sua vida.
        José Dias observava tudo com seus olhos atentos. Capitu, com seus
        olhos de ressaca, permaneceu um mistério.
        """

# Função para dividir o texto em sentenças limpas
def separar_sentencas(texto):
    """Usa regex para dividir o texto em sentenças, removendo ruídos."""
    texto = texto.replace('\n', ' ').strip()
    # Separa por pontuação final, mantendo sentenças com conteúdo
    sentencas = re.split(r'[.!?]+', texto)
    return [s.strip() for s in sentencas if len(s.strip()) > 10]

# Carrega o texto principal para análise
# TENTE COLOCAR AQUI O CAMINHO PARA O SEU ARQUIVO .txt
TEXTO_ANALISE = carregar_texto('machado_de_assis.txt')
SENTENCAS = separar_sentencas(TEXTO_ANALISE)

# --- 3. ANÁLISE DE SENTIMENTO (DO SCRIPT DE TEXTO) ---

def analisar_e_plotar_sentimento(sentencas):
    """Realiza a análise de sentimento e gera um gráfico de barras."""
    print("\n--- INICIANDO ANÁLISE DE SENTIMENTO ---")
    sa = SentimentIntensityAnalyzer()
    sentimentos = [sa.polarity_scores(s)['compound'] for s in sentencas]

    # Classificação
    positivas = sum(1 for score in sentimentos if score > 0.05)
    negativas = sum(1 for score in sentimentos if score < -0.05)
    neutras = len(sentimentos) - positivas - negativas

    # Visualização
    categorias = ['Positivas', 'Neutras', 'Negativas']
    quantidades = [positivas, neutras, negativas]
    cores = ['#48dbfb', '#feca57', '#ff6b6b']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categorias, quantidades, color=cores)
    plt.title('Análise de Sentimento do Texto', fontsize=16)
    plt.ylabel('Número de Sentenças', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adiciona rótulos de contagem nas barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center')

    print(f"Análise concluída: {positivas} positivas, {negativas} negativas, {neutras} neutras.")
    plt.show()

# --- 4. CONSTRUÇÃO E ANÁLISE DA REDE (UNIFICANDO OS DOIS SCRIPTS) ---

def construir_e_visualizar_rede(sentencas, top_n=25):
    """
    Constrói e visualiza uma rede de coocorrência de palavras.
    """
    print(f"\n--- CONSTRUINDO REDE COM AS {top_n} PALAVRAS MAIS IMPORTANTES ---")
    
    # Identifica possíveis nomes/substantivos (palavras capitalizadas)
    palavras = re.findall(r'\b[A-Z][a-z]+\b', TEXTO_ANALISE)
    
    # Usa Counter (a melhor técnica do script 2) para contar a frequência
    contador_palavras = Counter(palavras)
    
    # Seleciona os N mais comuns como nós da nossa rede
    nos_principais = [palavra for palavra, freq in contador_palavras.most_common(top_n)]
    print(f"Nós principais da rede: {', '.join(nos_principais)}")

    # Cria o grafo
    G = nx.Graph()
    G.add_nodes_from(nos_principais)

    # Constrói as arestas baseadas na coocorrência nas mesmas sentenças
    # Usando defaultdict para contar as coocorrências
    coocorrencias = defaultdict(int)
    for sentenca in sentencas:
        palavras_na_sentenca = set(re.findall(r'\b[A-Z][a-z]+\b', sentenca))
        # Filtra para manter apenas os nós principais
        palavras_relevantes = [p for p in palavras_na_sentenca if p in nos_principais]
        
        # Gera pares de palavras que aparecem juntas
        from itertools import combinations
        for par in combinations(sorted(palavras_relevantes), 2):
            coocorrencias[par] += 1
            
    # Adiciona as arestas ao grafo com pesos
    for par, peso in coocorrencias.items():
        G.add_edge(par[0], par[1], weight=peso)
        
    # --- Visualização 1: Rede Completa (do script de grafos) ---
    print("\nVisualizando a rede de coocorrência completa...")
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42, k=0.9) # Layout para melhor dispersão

    # Desenha os nós (tamanho proporcional à frequência)
    tamanhos_nos = [contador_palavras[no] * 20 for no in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=tamanhos_nos, node_color='skyblue', alpha=0.8)

    # Desenha as arestas (espessura proporcional ao peso)
    pesos_arestas = [G[u][v]['weight'] * 0.5 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=pesos_arestas, edge_color='gray', alpha=0.6)

    # Desenha os rótulos dos nós
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title('Rede de Coocorrência de Palavras', fontsize=18)
    plt.box(False)
    plt.show()

    # --- Análise e Visualização 2: Ego Graph do Hub (do script de grafos) ---
    if not G.nodes:
        print("Não foi possível gerar a rede. Poucos dados.")
        return
        
    # Encontra o nó com maior grau (o "hub" mais importante)
    node_and_degree = G.degree(weight='weight')
    (hub_principal, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    print(f"\nO 'hub' principal da rede é '{hub_principal}' (nó mais influente).")
    
    # Cria um "ego graph" para o hub, mostrando apenas suas conexões diretas
    hub_ego = nx.ego_graph(G, hub_principal, radius=1)

    # Visualização do ego graph
    print(f"Visualizando a rede 'ego' do hub '{hub_principal}'...")
    plt.figure(figsize=(10, 8))
    pos_ego = nx.spring_layout(hub_ego, seed=42)
    
    # Desenha o ego graph
    nx.draw(hub_ego, pos_ego, node_color='lightblue', node_size=500, with_labels=True, width=1.5, edge_color='grey')
    
    # Destaca o nó central (o hub)
    options = {'node_size': 1500, 'node_color': 'salmon'}
    nx.draw_networkx_nodes(hub_ego, pos_ego, nodelist=[hub_principal], **options)
    
    plt.title(f'Rede Ego de "{hub_principal}"', fontsize=16)
    plt.box(False)
    plt.show()


# --- 5. EXECUÇÃO DO FLUXO DE TRABALHO ---
if __name__ == "__main__":
    # Etapa 1: Análise de Sentimento
    analisar_e_plotar_sentimento(SENTENCAS)
    
    # Etapa 2: Construção e Análise da Rede
    construir_e_visualizar_rede(SENTENCAS, top_n=20)
    
    print("\n--- FIM DA ANÁLISE ---")