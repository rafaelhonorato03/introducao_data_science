# Teste simples do analisador de PDFs - VERSÃO MELHORADA
import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa o analisador
from analise_pdf_personagens import AnalisadorPDF

def teste_com_texto():
    """Testa o analisador com texto de exemplo"""
    print("=== TESTE DO ANALISADOR DE PDFs - VERSÃO MELHORADA ===")
    print("Testando identificação inteligente de personagens...")
    
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
    
    # Cria analisador
    analisador = AnalisadorPDF()
    
    # Define o texto diretamente
    analisador.texto_completo = texto_exemplo
    
    # Processa o texto
    print("Processando texto...")
    analisador.tokenizar_texto()
    analisador.identificar_personagens_melhorado()
    
    # Mostra resultados
    print(f"\n=== RESULTADOS ===")
    print(f"Total de palavras no texto: {len(analisador.palavras)}")
    print(f"Possíveis personagens encontrados: {len(analisador.nomes_proprios)}")
    print(f"Tipos únicos de personagens: {len(set(analisador.nomes_proprios))}")
    
    print(f"\n=== TOP 5 PERSONAGENS IDENTIFICADOS ===")
    for i, (nome, freq) in enumerate(analisador.freq_nomes.most_common(5), 1):
        print(f"{i}. {nome}: {freq} aparições")
    
    # Mostra todos os personagens encontrados
    print(f"\n=== TODOS OS PERSONAGENS ENCONTRADOS ===")
    for i, (nome, freq) in enumerate(analisador.freq_nomes.most_common(), 1):
        print(f"{i:2d}. {nome}: {freq} aparições")
    
    # Cria gráficos
    print(f"\n=== CRIANDO GRÁFICOS ===")
    
    # Cria diretório se não existir
    Path("../../resultados/graficos").mkdir(parents=True, exist_ok=True)
    
    # Gráfico de frequência (top 5)
    fig_freq = analisador.criar_grafico_frequencia(5)
    if fig_freq:
        fig_freq.savefig('../../resultados/graficos/teste_personagens_frequencia.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de frequência salvo como 'teste_personagens_frequencia.png'")
    
    # Gráfico de dispersão (top 5)
    fig_disp = analisador.criar_grafico_dispersao(5)
    if fig_disp:
        fig_disp.savefig('../../resultados/graficos/teste_personagens_dispersao.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de dispersão salvo como 'teste_personagens_dispersao.png'")
    
    print(f"\n=== MELHORIAS IMPLEMENTADAS ===")
    print("✓ Filtro expandido de falsos positivos (Não, Era, etc.)")
    print("✓ Identificação de nomes compostos (José Gabriel, Maria Clara)")
    print("✓ Filtro de nomes que aparecem apenas uma vez")
    print("✓ Foco nos 5 principais personagens")
    print("✓ Melhor detecção de nomes próprios")
    
    print(f"\n=== RESUMO ===")
    print("✓ Análise concluída com sucesso!")
    print("✓ Personagens identificados e contados")
    print("✓ Gráficos criados e salvos")
    print("\nPara usar com PDFs:")
    print("1. Coloque um PDF na pasta 'dados/'")
    print("2. Use: analisador.analisar_pdf('dados/seu_arquivo.pdf')")

if __name__ == "__main__":
    teste_com_texto() 