# Importando bibliotecas necessárias
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
import PyPDF2
import fitz  # PyMuPDF - alternativa mais robusta
import os
from pathlib import Path
import numpy as np
import networkx as nx
from textblob import TextBlob
import seaborn as sns
from datetime import datetime
import json

# ==========================================
# ANÁLISE DE PERSONAGENS EM PDFs COM NER (spaCy)
# ==========================================
# Este script usa spaCy com Named Entity Recognition (NER)
# para identificar personagens de forma muito mais precisa
# AGORA COM ANÁLISES AVANÇADAS: coocorrência, sentimentos, capítulos

class AnalisadorPDFNER:
    def __init__(self):
        """Inicializa o analisador de PDFs com NER"""
        self.texto_completo = ""
        self.palavras = []
        self.personagens_ner = []
        self.freq_personagens = Counter()
        self.nlp = None
        
        # Novas variáveis para análises avançadas
        self.capitulos = []
        self.analise_sentimentos = {}
        self.rede_personagens = None
        self.coocorrencias = {}
        self.analise_temporal = {}
        
        # Inicializa o modelo spaCy
        self.inicializar_spacy()
        
    def inicializar_spacy(self):
        """
        Inicializa o modelo spaCy para português
        """
        try:
            import spacy
            
            # Tenta carregar o modelo português
            try:
                self.nlp = spacy.load("pt_core_news_sm")
                # Aumenta o limite de tamanho do texto para 10 milhões de caracteres
                self.nlp.max_length = 10000000
                print("✓ Modelo spaCy português carregado (pt_core_news_sm)")
                print(f"✓ Limite de texto aumentado para {self.nlp.max_length:,} caracteres")
            except OSError:
                print("Modelo português não encontrado. Baixando...")
                try:
                    spacy.cli.download("pt_core_news_sm")
                    self.nlp = spacy.load("pt_core_news_sm")
                    # Aumenta o limite de tamanho do texto
                    self.nlp.max_length = 10000000
                    print("✓ Modelo spaCy português baixado e carregado")
                    print(f"✓ Limite de texto aumentado para {self.nlp.max_length:,} caracteres")
                except Exception as e:
                    print(f"Erro ao baixar modelo português: {e}")
                    print("Tentando modelo multilíngue...")
                    try:
                        self.nlp = spacy.load("xx_ent_wiki_sm")
                        # Aumenta o limite de tamanho do texto
                        self.nlp.max_length = 10000000
                        print("✓ Modelo spaCy multilíngue carregado")
                        print(f"✓ Limite de texto aumentado para {self.nlp.max_length:,} caracteres")
                    except OSError:
                        print("Baixando modelo multilíngue...")
                        spacy.cli.download("xx_ent_wiki_sm")
                        self.nlp = spacy.load("xx_ent_wiki_sm")
                        # Aumenta o limite de tamanho do texto
                        self.nlp.max_length = 10000000
                        print("✓ Modelo spaCy multilíngue baixado e carregado")
                        print(f"✓ Limite de texto aumentado para {self.nlp.max_length:,} caracteres")
                        
        except ImportError:
            print("❌ spaCy não está instalado!")
            print("Instale com: pip install spacy")
            print("E depois baixe o modelo: python -m spacy download pt_core_news_sm")
            self.nlp = None
    
    def extrair_texto_pdf(self, caminho_pdf):
        """
        Extrai texto de um arquivo PDF usando PyMuPDF (mais robusto)
        """
        try:
            # Tenta usar PyMuPDF primeiro (mais robusto)
            doc = fitz.open(caminho_pdf)
            texto = ""
            
            for pagina in doc:
                texto += pagina.get_text()
            
            doc.close()
            print(f"✓ Texto extraído usando PyMuPDF: {len(texto)} caracteres")
            
        except ImportError:
            print("PyMuPDF não disponível, tentando PyPDF2...")
            try:
                # Fallback para PyPDF2
                with open(caminho_pdf, 'rb') as arquivo:
                    leitor = PyPDF2.PdfReader(arquivo)
                    texto = ""
                    
                    for pagina in leitor.pages:
                        texto += pagina.extract_text()
                
                print(f"✓ Texto extraído usando PyPDF2: {len(texto)} caracteres")
                
            except Exception as e:
                print(f"❌ Erro ao extrair texto: {e}")
                return None
        
        self.texto_completo = texto
        return texto
    
    def identificar_personagens_ner(self):
        """
        Identifica personagens usando spaCy NER
        """
        if not self.nlp:
            print("❌ spaCy não disponível. Use o método básico.")
            return []
        
        print("Analisando texto com spaCy NER...")
        
        # Processa o texto com spaCy
        doc = self.nlp(self.texto_completo)
        
        # Lista para armazenar entidades encontradas
        entidades = []
        
        # Tipos de entidades que podem ser personagens (PER para português, PERSON para multilíngue)
        tipos_personagem = ['PERSON', 'PER']  # Person, Personagem
        
        # Extrai entidades nomeadas
        for ent in doc.ents:
            # Verifica se é uma entidade de pessoa
            if ent.label_ in tipos_personagem:
                nome = ent.text.strip()
                
                # Filtra nomes muito curtos ou que são apenas títulos
                if len(nome) > 2 and not self.eh_titulo(nome):
                    entidades.append(nome)
        
        # Remove duplicatas e conta frequência
        self.personagens_ner = entidades
        self.freq_personagens = Counter(entidades)
        
        print(f"✓ Personagens identificados com NER: {len(entidades)}")
        print(f"✓ Tipos únicos de personagens: {len(set(entidades))}")
        
        return entidades
    
    def eh_titulo(self, nome):
        """
        Verifica se o nome é apenas um título (Dr., Sr., etc.)
        """
        titulos = {
            'dr', 'dra', 'doutor', 'doutora', 'sr', 'sra', 'senhor', 'senhora',
            'prof', 'professor', 'professora', 'padre', 'frei', 'bispo',
            'dom', 'dona', 'tio', 'tia', 'primo', 'prima'
        }
        
        palavras = nome.lower().split()
        return len(palavras) == 1 and palavras[0] in titulos
    
    def identificar_nomes_compostos_ner(self):
        """
        Identifica nomes compostos usando NER + regex
        """
        if not self.nlp:
            return []
        
        nomes_compostos = []
        
        # Processa o texto com spaCy
        doc = self.nlp(self.texto_completo)
        
        # Busca por padrões de nomes compostos
        padroes = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # José Gabriel
            r'\b[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+\b',  # José Gabriel Silva
            r'\b[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+\b',  # José Gabriel Silva Santos
        ]
        
        for padrao in padroes:
            matches = re.finditer(padrao, self.texto_completo)
            for match in matches:
                nome_composto = match.group()
                
                # Verifica se o nome composto é reconhecido como PERSON pelo NER
                doc_nome = self.nlp(nome_composto)
                for ent in doc_nome.ents:
                    if ent.label_ in ['PERSON', 'PER'] and ent.text == nome_composto:
                        nomes_compostos.append(nome_composto)
                        break
        
        return nomes_compostos
    
    def analise_completa_ner(self):
        """
        Executa análise completa usando apenas NER (spaCy) e nomes compostos reconhecidos pelo NER.
        Menor risco de falsos positivos.
        """
        if not self.nlp:
            print("❌ spaCy não disponível. Use o analisador básico.")
            return Counter()
        
        print("=== ANÁLISE COMPLETA COM NER (MENOR RISCO) ===")
        
        # 1. Identificação principal com NER
        personagens_ner = self.identificar_personagens_ner()
        
        # 2. Identificação de nomes compostos reconhecidos pelo NER
        nomes_compostos = self.identificar_nomes_compostos_ner()
        
        # 3. Combina resultados
        todos_personagens = personagens_ner + nomes_compostos
        
        # 4. Remove duplicatas e filtra
        personagens_filtrados = []
        for personagem in todos_personagens:
            # Remove personagens que aparecem apenas uma vez (provavelmente falsos positivos)
            if todos_personagens.count(personagem) > 1:
                personagens_filtrados.append(personagem)
        
        # 5. Conta frequência final
        self.freq_personagens = Counter(personagens_filtrados)
        
        print(f"✓ Análise NER: {len(personagens_ner)} personagens")
        print(f"✓ Nomes compostos: {len(nomes_compostos)} personagens")
        print(f"✓ Total final: {len(personagens_filtrados)} personagens válidos")
        
        return self.freq_personagens
    
    def encontrar_posicoes_personagens(self, personagens_principais):
        """
        Encontra as posições de aparição dos personagens principais no texto
        """
        texto_lower = self.texto_completo.lower()
        posicoes = {}
        
        for personagem in personagens_principais:
            posicoes[personagem] = []
            personagem_lower = personagem.lower()
            start = 0
            
            while True:
                pos = texto_lower.find(personagem_lower, start)
                if pos == -1:
                    break
                posicoes[personagem].append(pos)
                start = pos + 1
        
        return posicoes
    
    def criar_grafico_frequencia(self, top_n=20):
        """
        Cria gráfico de barras com os personagens mais frequentes
        """
        mais_comuns = self.freq_personagens.most_common(top_n)
        
        if not mais_comuns:
            print("❌ Nenhum personagem encontrado para criar gráfico")
            return None
        
        # Prepara dados para o gráfico
        nomes = [nome for nome, freq in mais_comuns]
        frequencias = [freq for nome, freq in mais_comuns]
        
        # Cria o gráfico
        plt.figure(figsize=(14, 8))
        bars = plt.bar(range(len(nomes)), frequencias, color='lightcoral', alpha=0.7)
        
        # Adiciona valores nas barras
        for bar, freq in zip(bars, frequencias):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                     str(freq), ha='center', va='bottom', fontweight='bold')
        
        # Configurações do gráfico
        plt.xlabel('Personagens', fontsize=12)
        plt.ylabel('Frequência de Aparição', fontsize=12)
        plt.title(f'Top {top_n} Personagens Mais Frequentes (NER)', fontsize=14, fontweight='bold')
        plt.xticks(range(len(nomes)), nomes, rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()
    
    def criar_grafico_dispersao(self, top_n=20):
        """
        Cria gráfico de dispersão mostrando onde os personagens aparecem no texto
        Agora usa barrinhas verticais (plt.vlines) ao invés de bolinhas.
        Personagens ordenados do mais frequente para o menos frequente.
        """
        mais_comuns = self.freq_personagens.most_common(top_n)
        
        if not mais_comuns:
            print("❌ Nenhum personagem encontrado para criar gráfico de dispersão")
            return None
        
        # Encontra posições dos personagens principais
        personagens_principais = [nome for nome, freq in mais_comuns]
        posicoes = self.encontrar_posicoes_personagens(personagens_principais)
        
        # Cria gráfico de dispersão com barrinhas verticais
        plt.figure(figsize=(18, 10))
        
        for i, personagem in enumerate(personagens_principais):
            if posicoes[personagem]:
                posicoes_norm = [pos/len(self.texto_completo)*100 for pos in posicoes[personagem]]
                # Barrinhas verticais
                plt.vlines(posicoes_norm, i-0.4, i+0.4, color='tab:blue', alpha=0.7, linewidth=2)
        
        # Ordena personagens do mais frequente (topo) para o menos frequente (base)
        plt.yticks(range(len(personagens_principais)), personagens_principais)
        plt.xlabel('Posição no texto (%)', fontsize=12)
        plt.ylabel('Personagens (ordenados por frequência)', fontsize=12)
        plt.title('Dispersão dos Personagens no Texto (NER)', fontsize=14, fontweight='bold')
        plt.grid(True, axis='x', alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()
    
    def debug_personagem(self, nome_personagem):
        """
        Função para debugar por que uma personagem específica pode estar sendo contada incorretamente
        """
        if not self.nlp:
            print("❌ spaCy não disponível para debug")
            return
        
        print(f"\n=== DEBUG: {nome_personagem} ===")
        
        # Busca todas as ocorrências da personagem no texto
        texto_lower = self.texto_completo.lower()
        nome_lower = nome_personagem.lower()
        
        # Encontra todas as posições
        posicoes = []
        start = 0
        while True:
            pos = texto_lower.find(nome_lower, start)
            if pos == -1:
                break
            posicoes.append(pos)
            start = pos + 1
        
        print(f"Ocorrências encontradas por busca simples: {len(posicoes)}")
        
        # Verifica como o NER está identificando
        doc = self.nlp(self.texto_completo)
        entidades_ner = [ent.text for ent in doc.ents if ent.label_ == "PER" and nome_personagem.lower() in ent.text.lower()]
        
        print(f"Entidades NER que contêm '{nome_personagem}': {entidades_ner}")
        print(f"Total de entidades NER: {len(entidades_ner)}")
        
        # Mostra contexto das primeiras ocorrências
        print(f"\nPrimeiras 3 ocorrências no texto:")
        for i, pos in enumerate(posicoes[:3]):
            inicio = max(0, pos - 20)
            fim = min(len(self.texto_completo), pos + len(nome_personagem) + 20)
            contexto = self.texto_completo[inicio:fim]
            print(f"{i+1}. ...{contexto}...")
        
        # Verifica variações do nome
        print(f"\nPossíveis variações do nome '{nome_personagem}':")
        palavras = self.texto_completo.split()
        variacoes = [palavra for palavra in palavras if nome_personagem.lower() in palavra.lower()]
        variacoes_unicas = list(set(variacoes))
        print(f"Variações encontradas: {variacoes_unicas}")
        
        return len(posicoes), len(entidades_ner)

    # ==========================================
    # NOVAS FUNCIONALIDADES AVANÇADAS
    # ==========================================

    def dividir_em_capitulos(self):
        """
        Divide o texto em capítulos baseado em padrões comuns
        """
        print("Dividindo texto em capítulos...")
        
        # Padrões comuns para identificar capítulos
        padroes_capitulo = [
            r'\bCAPÍTULO\s+\d+\b',
            r'\bCAPITULO\s+\d+\b', 
            r'\bCapítulo\s+\d+\b',
            r'\bCapitulo\s+\d+\b',
            r'\bI{1,4}\b',  # Números romanos
            r'\b\d+\.\s*[A-Z]',  # Número seguido de título
        ]
        
        capitulos = []
        posicoes = []
        
        # Encontra todas as posições de início de capítulo
        for padrao in padroes_capitulo:
            matches = re.finditer(padrao, self.texto_completo, re.IGNORECASE)
            for match in matches:
                posicoes.append((match.start(), match.group()))
        
        # Ordena por posição
        posicoes.sort(key=lambda x: x[0])
        
        if not posicoes:
            # Se não encontrar capítulos, divide em seções de 5000 caracteres
            print("Nenhum capítulo encontrado. Dividindo em seções...")
            tamanho_secao = 5000
            for i in range(0, len(self.texto_completo), tamanho_secao):
                fim = min(i + tamanho_secao, len(self.texto_completo))
                capitulos.append({
                    'numero': len(capitulos) + 1,
                    'titulo': f'Seção {len(capitulos) + 1}',
                    'inicio': i,
                    'fim': fim,
                    'texto': self.texto_completo[i:fim]
                })
        else:
            # Cria capítulos baseado nas posições encontradas
            for i, (pos, titulo) in enumerate(posicoes):
                inicio = pos
                fim = posicoes[i + 1][0] if i + 1 < len(posicoes) else len(self.texto_completo)
                
                capitulos.append({
                    'numero': i + 1,
                    'titulo': titulo,
                    'inicio': inicio,
                    'fim': fim,
                    'texto': self.texto_completo[inicio:fim]
                })
        
        self.capitulos = capitulos
        print(f"✓ Texto dividido em {len(capitulos)} capítulos/seções")
        return capitulos

    def analisar_coocorrencias(self, janela_palavras=100):
        """
        Analisa coocorrências entre personagens em janelas de texto
        """
        print(f"Analisando coocorrências (janela: {janela_palavras} palavras)...")
        
        if not self.freq_personagens:
            print("❌ Execute a análise de personagens primeiro")
            return {}
        
        # Pega os personagens mais frequentes
        personagens_principais = [nome for nome, freq in self.freq_personagens.most_common(20)]
        
        # Divide o texto em palavras
        palavras = self.texto_completo.split()
        coocorrencias = {}
        
        # Para cada personagem, encontra suas posições
        posicoes_personagens = {}
        for personagem in personagens_principais:
            posicoes_personagens[personagem] = []
            for i, palavra in enumerate(palavras):
                if personagem.lower() in palavra.lower():
                    posicoes_personagens[personagem].append(i)
        
        # Analisa coocorrências
        for personagem1 in personagens_principais:
            coocorrencias[personagem1] = {}
            
            for personagem2 in personagens_principais:
                if personagem1 != personagem2:
                    contador = 0
                    
                    # Para cada aparição do personagem1
                    for pos1 in posicoes_personagens[personagem1]:
                        # Verifica se personagem2 aparece na janela
                        inicio_janela = max(0, pos1 - janela_palavras // 2)
                        fim_janela = min(len(palavras), pos1 + janela_palavras // 2)
                        
                        for pos2 in posicoes_personagens[personagem2]:
                            if inicio_janela <= pos2 <= fim_janela:
                                contador += 1
                                break
                    
                    coocorrencias[personagem1][personagem2] = contador
        
        self.coocorrencias = coocorrencias
        print(f"✓ Análise de coocorrências concluída")
        return coocorrencias

    def criar_rede_personagens(self):
        """
        Cria uma rede de personagens usando NetworkX
        """
        if not self.coocorrencias:
            print("❌ Execute a análise de coocorrências primeiro")
            return None
        
        print("Criando rede de personagens...")
        
        # Cria grafo
        G = nx.Graph()
        
        # Adiciona nós (personagens)
        for personagem in self.coocorrencias.keys():
            G.add_node(personagem, weight=self.freq_personagens[personagem])
        
        # Adiciona arestas (coocorrências)
        for personagem1 in self.coocorrencias.keys():
            for personagem2, peso in self.coocorrencias[personagem1].items():
                if peso > 0:  # Só adiciona se há coocorrência
                    G.add_edge(personagem1, personagem2, weight=peso)
        
        self.rede_personagens = G
        print(f"✓ Rede criada com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas")
        return G

    def visualizar_rede_personagens(self):
        """
        Cria visualização da rede de personagens
        """
        if not self.rede_personagens:
            print("❌ Rede de personagens não criada")
            return None
        
        print("Criando visualização da rede...")
        
        plt.figure(figsize=(16, 12))
        
        # Layout da rede
        pos = nx.spring_layout(self.rede_personagens, k=3, iterations=50)
        
        # Tamanho dos nós baseado na frequência
        tamanhos = [self.freq_personagens[node] * 100 for node in self.rede_personagens.nodes()]
        
        # Espessura das arestas baseada na coocorrência
        pesos = [self.rede_personagens[u][v]['weight'] * 2 for u, v in self.rede_personagens.edges()]
        
        # Desenha a rede
        nx.draw_networkx_nodes(self.rede_personagens, pos, 
                             node_size=tamanhos, 
                             node_color='lightcoral', 
                             alpha=0.7)
        
        nx.draw_networkx_edges(self.rede_personagens, pos, 
                             width=pesos, 
                             edge_color='gray', 
                             alpha=0.5)
        
        nx.draw_networkx_labels(self.rede_personagens, pos, 
                              font_size=10, 
                              font_weight='bold')
        
        plt.title('Rede de Relações entre Personagens', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        return plt.gcf()

    def analisar_sentimentos_personagens(self):
        """
        Analisa sentimentos dos trechos onde cada personagem aparece
        """
        print("Analisando sentimentos por personagem...")
        
        if not self.freq_personagens:
            print("❌ Execute a análise de personagens primeiro")
            return {}
        
        # Pega os personagens mais frequentes
        personagens_principais = [nome for nome, freq in self.freq_personagens.most_common(10)]
        
        analise_sentimentos = {}
        
        for personagem in personagens_principais:
            # Encontra posições do personagem
            posicoes = []
            texto_lower = self.texto_completo.lower()
            personagem_lower = personagem.lower()
            start = 0
            
            while True:
                pos = texto_lower.find(personagem_lower, start)
                if pos == -1:
                    break
                posicoes.append(pos)
                start = pos + 1
            
            # Analisa contexto de cada aparição
            sentimentos = []
            for pos in posicoes:
                # Pega contexto (100 caracteres antes e depois)
                inicio = max(0, pos - 100)
                fim = min(len(self.texto_completo), pos + len(personagem) + 100)
                contexto = self.texto_completo[inicio:fim]
                
                # Analisa sentimento do contexto
                try:
                    blob = TextBlob(contexto)
                    sentimentos.append(blob.sentiment.polarity)
                except:
                    sentimentos.append(0)  # Neutro se não conseguir analisar
            
            # Calcula estatísticas de sentimento
            if sentimentos:
                analise_sentimentos[personagem] = {
                    'media': np.mean(sentimentos),
                    'mediana': np.median(sentimentos),
                    'desvio': np.std(sentimentos),
                    'positivo': sum(1 for s in sentimentos if s > 0.1),
                    'negativo': sum(1 for s in sentimentos if s < -0.1),
                    'neutro': sum(1 for s in sentimentos if -0.1 <= s <= 0.1),
                    'total_contextos': len(sentimentos)
                }
        
        self.analise_sentimentos = analise_sentimentos
        print(f"✓ Análise de sentimentos concluída para {len(analise_sentimentos)} personagens")
        return analise_sentimentos

    def criar_grafico_sentimentos(self):
        """
        Cria gráfico de sentimentos por personagem
        """
        if not self.analise_sentimentos:
            print("❌ Execute a análise de sentimentos primeiro")
            return None
        
        print("Criando gráfico de sentimentos...")
        
        personagens = list(self.analise_sentimentos.keys())
        sentimentos_medios = [self.analise_sentimentos[p]['media'] for p in personagens]
        
        # Cria gráfico
        plt.figure(figsize=(14, 8))
        
        # Cores baseadas no sentimento
        cores = ['red' if s < -0.1 else 'green' if s > 0.1 else 'gray' for s in sentimentos_medios]
        
        bars = plt.bar(range(len(personagens)), sentimentos_medios, color=cores, alpha=0.7)
        
        # Adiciona valores nas barras
        for bar, sent in zip(bars, sentimentos_medios):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                     f'{sent:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.xlabel('Personagens', fontsize=12)
        plt.ylabel('Sentimento Médio (-1 a 1)', fontsize=12)
        plt.title('Análise de Sentimento por Personagem', fontsize=14, fontweight='bold')
        plt.xticks(range(len(personagens)), personagens, rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()

    def analisar_personagens_por_capitulo(self):
        """
        Analisa quais personagens dominam cada capítulo
        """
        if not self.capitulos:
            self.dividir_em_capitulos()
        
        if not self.freq_personagens:
            print("❌ Execute a análise de personagens primeiro")
            return {}
        
        print("Analisando personagens por capítulo...")
        
        # Pega os personagens mais frequentes
        personagens_principais = [nome for nome, freq in self.freq_personagens.most_common(10)]
        
        analise_capitulos = {}
        
        for i, capitulo in enumerate(self.capitulos):
            texto_capitulo = capitulo['texto']
            freq_capitulo = Counter()
            
            # Conta personagens neste capítulo
            for personagem in personagens_principais:
                freq = texto_capitulo.lower().count(personagem.lower())
                if freq > 0:
                    freq_capitulo[personagem] = freq
            
            # Encontra o personagem dominante
            personagem_dominante = freq_capitulo.most_common(1)[0] if freq_capitulo else (None, 0)
            
            analise_capitulos[i] = {
                'numero': capitulo['numero'],
                'titulo': capitulo['titulo'],
                'personagens': dict(freq_capitulo),
                'personagem_dominante': personagem_dominante[0],
                'freq_dominante': personagem_dominante[1],
                'total_personagens': sum(freq_capitulo.values())
            }
        
        self.analise_temporal = analise_capitulos
        print(f"✓ Análise por capítulos concluída")
        return analise_capitulos

    def criar_grafico_evolucao_temporal(self):
        """
        Cria gráfico mostrando a evolução dos personagens ao longo dos capítulos
        """
        if not self.analise_temporal:
            print("❌ Execute a análise por capítulos primeiro")
            return None
        
        print("Criando gráfico de evolução temporal...")
        
        # Pega os personagens mais frequentes
        personagens_principais = [nome for nome, freq in self.freq_personagens.most_common(5)]
        
        # Prepara dados
        capitulos = list(self.analise_temporal.keys())
        capitulos.sort()
        
        plt.figure(figsize=(16, 8))
        
        for personagem in personagens_principais:
            frequencias = []
            for cap in capitulos:
                freq = self.analise_temporal[cap]['personagens'].get(personagem, 0)
                frequencias.append(freq)
            
            plt.plot(capitulos, frequencias, marker='o', linewidth=2, label=personagem)
        
        plt.xlabel('Capítulos', fontsize=12)
        plt.ylabel('Frequência de Aparição', fontsize=12)
        plt.title('Evolução dos Personagens ao Longo da Obra', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()

    def gerar_relatorio_completo(self):
        """
        Gera um relatório completo com todas as análises
        """
        print("=== GERANDO RELATÓRIO COMPLETO ===")
        
        relatorio = {
            'metadata': {
                'data_analise': datetime.now().isoformat(),
                'total_caracteres': len(self.texto_completo),
                'total_palavras': len(self.texto_completo.split()),
                'total_capitulos': len(self.capitulos) if self.capitulos else 0
            },
            'personagens': {
                'total_identificados': len(self.freq_personagens),
                'top_10': dict(self.freq_personagens.most_common(10)),
                'frequencias_completas': dict(self.freq_personagens)
            },
            'analise_temporal': self.analise_temporal,
            'analise_sentimentos': self.analise_sentimentos,
            'coocorrencias': self.coocorrencias
        }
        
        # Salva relatório em JSON
        Path("resultados").mkdir(exist_ok=True)
        with open("resultados/relatorio_completo.json", "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
        
        print("✓ Relatório completo salvo em resultados/relatorio_completo.json")
        return relatorio

    def analisar_pdf(self, caminho_pdf, salvar_graficos=True, analise_completa=True):
        """
        Executa análise completa de um PDF usando NER e análises avançadas
        """
        print(f"=== ANÁLISE COMPLETA DO PDF: {caminho_pdf} ===")
        
        # Extrai texto
        if not self.extrair_texto_pdf(caminho_pdf):
            return None
        
        # Executa análise NER básica
        resultados = self.analise_completa_ner()
        
        if analise_completa:
            # Executa análises avançadas
            print("\n=== EXECUTANDO ANÁLISES AVANÇADAS ===")
            
            # 1. Análise por capítulos
            self.analisar_personagens_por_capitulo()
            
            # 2. Análise de coocorrências
            self.analisar_coocorrencias()
            
            # 3. Criação da rede
            self.criar_rede_personagens()
            
            # 4. Análise de sentimentos
            self.analisar_sentimentos_personagens()
            
            # 5. Gera relatório completo
            self.gerar_relatorio_completo()
        
        # Mostra resultados
        print(f"\n=== RESULTADOS ===")
        print(f"Total de caracteres no texto: {len(self.texto_completo)}")
        print(f"Personagens identificados: {len(self.personagens_ner)}")
        print(f"Tipos únicos de personagens: {len(set(self.personagens_ner))}")
        
        if self.freq_personagens:
            mais_comum = self.freq_personagens.most_common(1)[0]
            print(f"Personagem mais frequente: {mais_comum[0]} ({mais_comum[1]} aparições)")
        
        # Cria gráficos
        if salvar_graficos:
            # Cria diretório se não existir
            Path("resultados/graficos").mkdir(parents=True, exist_ok=True)
            
            # Gráficos básicos
            fig_freq = self.criar_grafico_frequencia(20)
            if fig_freq:
                fig_freq.savefig('resultados/graficos/personagens_ner_frequencia.png', 
                               dpi=300, bbox_inches='tight')
                print("✓ Gráfico de frequência NER salvo")
            
            fig_disp = self.criar_grafico_dispersao(20)
            if fig_disp:
                fig_disp.savefig('resultados/graficos/personagens_ner_dispersao.png', 
                               dpi=300, bbox_inches='tight')
                print("✓ Gráfico de dispersão NER salvo")
            
            if analise_completa:
                # Gráficos avançados
                fig_rede = self.visualizar_rede_personagens()
                if fig_rede:
                    fig_rede.savefig('resultados/graficos/rede_personagens.png', 
                                   dpi=300, bbox_inches='tight')
                    print("✓ Gráfico da rede de personagens salvo")
                
                fig_sent = self.criar_grafico_sentimentos()
                if fig_sent:
                    fig_sent.savefig('resultados/graficos/analise_sentimentos.png', 
                                   dpi=300, bbox_inches='tight')
                    print("✓ Gráfico de sentimentos salvo")
                
                fig_temp = self.criar_grafico_evolucao_temporal()
                if fig_temp:
                    fig_temp.savefig('resultados/graficos/evolucao_temporal.png', 
                                   dpi=300, bbox_inches='tight')
                    print("✓ Gráfico de evolução temporal salvo")
        
        return self.freq_personagens

# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================
def main():
    """
    Função principal para demonstrar o uso do analisador com NER e análises avançadas
    """
    print("=== ANALISADOR AVANÇADO DE PERSONAGENS EM PDFs ===")
    print("Este script usa spaCy NER + análises avançadas: coocorrência, sentimentos, capítulos")
    print()
    
    # Exemplo de uso
    analisador = AnalisadorPDFNER()
    
    # Verifica se existe um PDF na pasta dados
    pdfs_disponiveis = list(Path("dados").glob("*.pdf"))
    
    if pdfs_disponiveis:
        print("PDFs encontrados na pasta 'dados':")
        for i, pdf in enumerate(pdfs_disponiveis, 1):
            print(f"{i}. {pdf.name}")
        
        # Usa o primeiro PDF encontrado
        pdf_escolhido = pdfs_disponiveis[0]
        print(f"\nAnalisando: {pdf_escolhido.name}")
        
        # Executa análise completa
        resultados = analisador.analisar_pdf(str(pdf_escolhido), analise_completa=True)
        
        if resultados:
            print(f"\n=== TOP 5 PERSONAGENS ===")
            for i, (nome, freq) in enumerate(resultados.most_common(5), 1):
                print(f"{i}. {nome}: {freq} aparições")
            
            if analisador.analise_sentimentos:
                print(f"\n=== ANÁLISE DE SENTIMENTOS (TOP 3) ===")
                for personagem, dados in list(analisador.analise_sentimentos.items())[:3]:
                    sentimento = "Positivo" if dados['media'] > 0.1 else "Negativo" if dados['media'] < -0.1 else "Neutro"
                    print(f"{personagem}: {sentimento} (score: {dados['media']:.2f})")
    
    else:
        print("Nenhum PDF encontrado na pasta 'dados'")
        print("Para usar este script:")
        print("1. Coloque um PDF na pasta 'dados'")
        print("2. Execute o script novamente")
        print("3. Ou use a função analisar_pdf() diretamente")
        
        # Demonstração com texto de exemplo
        print("\n=== DEMONSTRAÇÃO COM TEXTO DE EXEMPLO ===")
        texto_exemplo = """
        José Gabriel era um homem simples que vivia na cidade. Maria Clara, sua esposa, sempre o apoiava.
        Pedro Santos, o vizinho, frequentemente visitava a família. Ana Beatriz, filha de José Gabriel e Maria Clara,
        adorava brincar com Carlos Eduardo, filho de Pedro Santos. Dona Rosa Silva, a professora de Ana Beatriz,
        sempre elogiava seu comportamento. Dr. João Silva, o médico da família, era muito atencioso.
        José Gabriel trabalhava com Sr. Antônio Santos na loja. Maria Clara conversava com Dona Clara Costa na feira.
        Pedro Santos e Carlos Eduardo iam pescar com Tio José Pereira. Ana Beatriz estudava com sua amiga Beatriz Oliveira.
        José Gabriel, Maria Clara, Pedro Santos, Ana Beatriz, Carlos Eduardo, Dona Rosa Silva, Dr. João Silva, 
        Sr. Antônio Santos, Dona Clara Costa, Tio José Pereira e Beatriz Oliveira formavam uma comunidade unida.
        """
        
        # Salva texto de exemplo como arquivo temporário
        with open("dados/texto_exemplo.txt", "w", encoding="utf-8") as f:
            f.write(texto_exemplo)
        
        print("Texto de exemplo criado. Execute novamente para ver a análise.")

if __name__ == "__main__":
    main() 