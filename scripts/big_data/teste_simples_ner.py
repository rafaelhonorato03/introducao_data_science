# Teste simples do spaCy NER
import spacy

def teste_spacy_ner():
    """Testa se o spaCy NER está funcionando"""
    print("=== TESTE SIMPLES DO SPAcy NER ===")
    
    try:
        # Carrega o modelo
        print("Carregando modelo spaCy...")
        nlp = spacy.load("pt_core_news_sm")
        print("✓ Modelo carregado com sucesso!")
        
        # Texto de teste
        texto = """
        José Gabriel era um homem simples que vivia na cidade. Maria Clara, sua esposa, sempre o apoiava.
        Pedro Santos, o vizinho, frequentemente visitava a família. Ana Beatriz, filha de José Gabriel e Maria Clara,
        adorava brincar com Carlos Eduardo, filho de Pedro Santos.
        """
        
        print("\nProcessando texto...")
        doc = nlp(texto)
        
        print("\n=== ENTIDADES ENCONTRADAS ===")
        for ent in doc.ents:
            print(f"- {ent.text} ({ent.label_})")
        
        print(f"\n=== PERSONAGENS (PER) ===")
        personagens = [ent.text for ent in doc.ents if ent.label_ == "PER"]
        for i, personagem in enumerate(personagens, 1):
            print(f"{i}. {personagem}")
        
        print(f"\n✓ Teste concluído! Encontrados {len(personagens)} personagens.")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    teste_spacy_ner() 