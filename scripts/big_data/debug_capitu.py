# Debug específico para investigar o problema da Capitu
import spacy
import re
from collections import Counter

def debug_capitu():
    """
    Debug específico para entender por que a Capitu pode estar sendo contada incorretamente
    """
    print("=== DEBUG ESPECÍFICO: CAPITU ===")
    
    # Carrega o modelo spaCy
    try:
        nlp = spacy.load("pt_core_news_sm")
        print("✓ Modelo spaCy carregado")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return
    
    # Texto de exemplo do Dom Casmurro (primeiros parágrafos)
    texto_casmurro = """
    Agora que expliquei o título, passo a escrever o livro. Antes disso, porém, digamos os motivos que me põem a pena na mão.
    
    Vivo só, com um criado. A casa em que moro é própria; fi-la construir de propósito, levado de um desejo tão particular que me vexa imprimi-lo, mas vá lá. Um dia há de ser que, vindo do Engenho Novo, e entrando numa casa da Rua do Ouvidor, achei num catálogo, que um sujeito me deu, uma estampa de uma mulher, com este título ao pé: D. Casmurro, 1813. Fiquei gostando do nome, e depois da estampa. Quando vim para a cidade, e me decidi a edificar, pus-lhe o nome de Casmurro, para que ficasse completa a semelhança. Nem me importa que lhe dêem outro nome, como de hábito; o que importa é que eu fique sabendo que se chama Casmurro.
    
    Agora que expliquei o título, passo a escrever o livro. Antes disso, porém, digamos os motivos que me põem a pena na mão.
    
    Vivo só, com um criado. A casa em que moro é própria; fi-la construir de propósito, levado de um desejo tão particular que me vexa imprimi-lo, mas vá lá. Um dia há de ser que, vindo do Engenho Novo, e entrando numa casa da Rua do Ouvidor, achei num catálogo, que um sujeito me deu, uma estampa de uma mulher, com este título ao pé: D. Casmurro, 1813. Fiquei gostando do nome, e depois da estampa. Quando vim para a cidade, e me decidi a edificar, pus-lhe o nome de Casmurro, para que ficasse completa a semelhança. Nem me importa que lhe dêem outro nome, como de hábito; o que importa é que eu fique sabendo que se chama Casmurro.
    
    Capitu, minha vizinha e amiga, brincava comigo na chácara, e eu gostava dela desde os meus onze anos. Capitu era uma menina esperta, viva, faladeira, e sobretudo muito bonita. Tinha os olhos grandes e pretos, a boca pequena, o nariz fino, e um ar de mistério que me fascinava. Capitu sabia tudo, e eu nada. Capitu explicava-me as coisas, e eu escutava com atenção. Capitu era a minha professora, a minha confidente, a minha amiga.
    
    Bentinho, que era o meu nome de batismo, vivia na casa ao lado. Bentinho e eu éramos amigos desde a infância. Bentinho tinha medo de tudo, e eu corajoso. Bentinho chorava por qualquer coisa, e eu consolava-o. Bentinho era o meu protegido, e eu o seu protetor.
    
    Escobar, que veio morar na nossa rua, era um rapaz alto, forte, e muito inteligente. Escobar sabia latim, grego, e outras línguas. Escobar era o orgulho da família, e todos o admiravam. Escobar tornou-se amigo de Bentinho, e depois meu amigo também.
    """
    
    print(f"Texto de teste com {len(texto_casmurro)} caracteres")
    
    # 1. Busca simples por "Capitu"
    print(f"\n=== 1. BUSCA SIMPLES POR 'CAPITU' ===")
    texto_lower = texto_casmurro.lower()
    ocorrencias_simples = []
    start = 0
    while True:
        pos = texto_lower.find("capitu", start)
        if pos == -1:
            break
        ocorrencias_simples.append(pos)
        start = pos + 1
    
    print(f"Ocorrências encontradas por busca simples: {len(ocorrencias_simples)}")
    for i, pos in enumerate(ocorrencias_simples):
        inicio = max(0, pos - 10)
        fim = min(len(texto_casmurro), pos + 10)
        contexto = texto_casmurro[inicio:fim]
        print(f"  {i+1}. ...{contexto}...")
    
    # 2. Análise com spaCy NER
    print(f"\n=== 2. ANÁLISE COM SPAcy NER ===")
    doc = nlp(texto_casmurro)
    
    # Todas as entidades
    print("Todas as entidades encontradas:")
    for ent in doc.ents:
        print(f"  - {ent.text} ({ent.label_})")
    
    # Apenas entidades PER (pessoas)
    entidades_per = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    print(f"\nEntidades PER (pessoas): {entidades_per}")
    
    # Conta frequência
    freq_per = Counter(entidades_per)
    print(f"\nFrequência das entidades PER:")
    for nome, freq in freq_per.most_common():
        print(f"  - {nome}: {freq}")
    
    # 3. Verifica especificamente "Capitu"
    print(f"\n=== 3. VERIFICAÇÃO ESPECÍFICA: CAPITU ===")
    capitu_ner = [ent.text for ent in doc.ents if ent.label_ == "PER" and "capitu" in ent.text.lower()]
    print(f"Entidades NER que contêm 'Capitu': {capitu_ner}")
    print(f"Total: {len(capitu_ner)}")
    
    # 4. Verifica variações do nome
    print(f"\n=== 4. VARIAÇÕES DO NOME ===")
    palavras = texto_casmurro.split()
    variacoes_capitu = [palavra for palavra in palavras if "capitu" in palavra.lower()]
    variacoes_unicas = list(set(variacoes_capitu))
    print(f"Variações encontradas: {variacoes_unicas}")
    
    # 5. Teste com diferentes contextos
    print(f"\n=== 5. TESTE COM DIFERENTES CONTEXTOS ===")
    frases_teste = [
        "Capitu era minha amiga.",
        "A Capitu brincava comigo.",
        "Capitu, minha vizinha, era bonita.",
        "Eu gostava da Capitu.",
        "Capitu sabia tudo."
    ]
    
    for frase in frases_teste:
        doc_frase = nlp(frase)
        entidades = [ent.text for ent in doc_frase.ents if ent.label_ == "PER"]
        print(f"'{frase}' -> Entidades PER: {entidades}")
    
    # 6. Possíveis problemas identificados
    print(f"\n=== 6. POSSÍVEIS PROBLEMAS ===")
    print("1. O modelo pode não reconhecer 'Capitu' como nome próprio")
    print("2. Pode estar sendo confundido com palavra comum")
    print("3. O contexto pode não ser suficiente para o NER")
    print("4. Pode haver variações de capitalização")
    print("5. O modelo pode precisar de mais contexto")
    
    return len(ocorrencias_simples), len(capitu_ner)

if __name__ == "__main__":
    debug_capitu() 