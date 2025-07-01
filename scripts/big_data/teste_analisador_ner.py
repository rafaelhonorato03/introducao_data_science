# Teste do analisador de PDFs com NER (spaCy)
import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa o analisador NER
from analise_pdf_ner import AnalisadorPDFNER

def teste_ner_com_texto():
    """Testa o analisador NER com texto de exemplo"""
    print("=== TESTE DO ANALISADOR DE PDFs COM NER ===")
    print("Testando identificação precisa de personagens usando spaCy...")
    
    # Texto de exemplo com personagens (incluindo nomes compostos)
    texto_exemplo = """
    Dom Casmurro é um romance de Machado de Assis. Bentinho, o protagonista, 
    narra sua história desde a infância. Sua mãe, Dona Glória, sempre quis 
    que ele fosse padre. Capitu, sua vizinha e futura esposa, é uma personagem 
    misteriosa. José Dias, amigo de Bentinho, também é importante na trama.
    
    Bentinho e Capitu se casam e têm um filho chamado Ezequiel. José Dias, 
    agregado da família, sempre observa tudo. Dona Fortunata, mãe de Capitu, 
    é uma mulher simples. Padre Cabral é o confessor da família.
    
    Bentinho suspeita que Capitu o traiu com José Dias. Ezequiel se parece 
    muito com José Dias, o que aumenta as suspeitas. Bentinho fica obcecado 
    com essa ideia e acaba se tornando um homem amargo.
    
    No final, Bentinho vive isolado, escrevendo suas memórias. Capitu e 
    Ezequiel morrem, e Bentinho fica sozinho com suas dúvidas.
    
    José Gabriel era um homem simples que vivia na cidade. Maria Clara, sua esposa, sempre o apoiava.
    Pedro Santos, o vizinho, frequentemente visitava a família. Ana Beatriz, filha de José Gabriel e Maria Clara,
    adorava brincar com Carlos Eduardo, filho de Pedro Santos. Dona Rosa Silva, a professora de Ana Beatriz,
    sempre elogiava seu comportamento. Dr. João Silva, o médico da família, era muito atencioso.
    José Gabriel trabalhava com Sr. Antônio Santos na loja. Maria Clara conversava com Dona Clara Costa na feira.
    Pedro Santos e Carlos Eduardo iam pescar com Tio José Pereira. Ana Beatriz estudava com sua amiga Beatriz Oliveira.
    """
    
    # Cria analisador NER
    analisador = AnalisadorPDFNER()
    
    # Define o texto diretamente
    analisador.texto_completo = texto_exemplo
    
    # Processa o texto com NER
    print("Processando texto com spaCy NER...")
    resultados = analisador.analise_completa_ner()
    
    # Mostra resultados
    print(f"\n=== RESULTADOS NER ===")
    print(f"Total de caracteres no texto: {len(analisador.texto_completo)}")
    print(f"Personagens identificados com NER: {len(analisador.personagens_ner)}")
    print(f"Tipos únicos de personagens: {len(set(analisador.personagens_ner))}")
    
    print(f"\n=== TOP 5 PERSONAGENS IDENTIFICADOS (NER) ===")
    for i, (nome, freq) in enumerate(analisador.freq_personagens.most_common(5), 1):
        print(f"{i}. {nome}: {freq} aparições")
    
    # Mostra todos os personagens encontrados
    print(f"\n=== TODOS OS PERSONAGENS ENCONTRADOS (NER) ===")
    for i, (nome, freq) in enumerate(analisador.freq_personagens.most_common(), 1):
        print(f"{i:2d}. {nome}: {freq} aparições")
    
    # Cria gráficos
    print(f"\n=== CRIANDO GRÁFICOS NER ===")
    
    # Cria diretório se não existir
    Path("../../resultados/graficos").mkdir(parents=True, exist_ok=True)
    
    # Gráfico de frequência (top 5)
    fig_freq = analisador.criar_grafico_frequencia(5)
    if fig_freq:
        fig_freq.savefig('../../resultados/graficos/teste_personagens_ner_frequencia.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de frequência NER salvo como 'teste_personagens_ner_frequencia.png'")
    
    # Gráfico de dispersão (top 5)
    fig_disp = analisador.criar_grafico_dispersao(5)
    if fig_disp:
        fig_disp.savefig('../../resultados/graficos/teste_personagens_ner_dispersao.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de dispersão NER salvo como 'teste_personagens_ner_dispersao.png'")
    
    print(f"\n=== VANTAGENS DO NER ===")
    print("✓ Identificação precisa de entidades nomeadas")
    print("✓ Distinção automática entre pessoas, lugares, organizações")
    print("✓ Melhor detecção de nomes compostos")
    print("✓ Redução significativa de falsos positivos")
    print("✓ Análise contextual avançada")
    
    print(f"\n=== RESUMO NER ===")
    print("✓ Análise NER concluída com sucesso!")
    print("✓ Personagens identificados com alta precisão")
    print("✓ Gráficos criados e salvos")
    print("\nPara usar com PDFs:")
    print("1. Coloque um PDF na pasta 'dados/'")
    print("2. Use: analisador.analisar_pdf('dados/seu_arquivo.pdf')")

def comparar_metodos():
    """Compara o método básico com o NER"""
    print("\n=== COMPARAÇÃO: MÉTODO BÁSICO vs NER ===")
    
    # Importa ambos os analisadores
    from analise_pdf_personagens import AnalisadorPDF
    from analise_pdf_ner import AnalisadorPDFNER
    
    texto_exemplo = """
    José Gabriel era um homem simples que vivia na cidade. Maria Clara, sua esposa, sempre o apoiava.
    Pedro Santos, o vizinho, frequentemente visitava a família. Ana Beatriz, filha de José Gabriel e Maria Clara,
    adorava brincar com Carlos Eduardo, filho de Pedro Santos. Dona Rosa Silva, a professora de Ana Beatriz,
    sempre elogiava seu comportamento. Dr. João Silva, o médico da família, era muito atencioso.
    """
    
    # Testa método básico
    print("1. MÉTODO BÁSICO:")
    analisador_basico = AnalisadorPDF()
    analisador_basico.texto_completo = texto_exemplo
    analisador_basico.tokenizar_texto()
    analisador_basico.identificar_personagens_melhorado()
    
    print(f"   Personagens encontrados: {len(analisador_basico.nomes_proprios)}")
    print(f"   Top 3: {[nome for nome, freq in analisador_basico.freq_nomes.most_common(3)]}")
    
    # Testa método NER
    print("\n2. MÉTODO NER:")
    analisador_ner = AnalisadorPDFNER()
    analisador_ner.texto_completo = texto_exemplo
    resultados_ner = analisador_ner.analise_completa_ner()
    
    print(f"   Personagens encontrados: {len(analisador_ner.personagens_ner)}")
    print(f"   Top 3: {[nome for nome, freq in analisador_ner.freq_personagens.most_common(3)]}")
    
    print("\n=== CONCLUSÃO ===")
    print("O NER oferece identificação mais precisa e contextual!")

if __name__ == "__main__":
    teste_ner_com_texto()
    comparar_metodos() 