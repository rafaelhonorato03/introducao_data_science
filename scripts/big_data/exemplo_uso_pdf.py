# ==========================================
# EXEMPLO DE USO DO ANALISADOR DE PDFs
# ==========================================
# Este script demonstra como usar o AnalisadorPDF para
# identificar personagens em PDFs e criar gráficos

import sys
import os
from pathlib import Path

# Adiciona o diretório pai ao path para importar o analisador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from big_data.analise_pdf_personagens import AnalisadorPDF

def exemplo_analise_pdf():
    """
    Exemplo completo de como analisar um PDF e identificar personagens
    """
    print("=== EXEMPLO DE ANÁLISE DE PDF ===")
    print("Este exemplo mostra como identificar personagens em PDFs")
    print()
    
    # Cria uma instância do analisador
    analisador = AnalisadorPDF()
    
    # Verifica se há PDFs na pasta dados
    pdfs_disponiveis = list(Path("../../dados").glob("*.pdf"))
    
    if pdfs_disponiveis:
        print("PDFs encontrados:")
        for i, pdf in enumerate(pdfs_disponiveis, 1):
            print(f"{i}. {pdf.name}")
        
        # Usa o primeiro PDF encontrado
        pdf_escolhido = pdfs_disponiveis[0]
        print(f"\nAnalisando: {pdf_escolhido.name}")
        
        # Executa a análise completa
        resultados = analisador.analisar_pdf(str(pdf_escolhido))
        
        if resultados:
            print(f"\n=== TOP 20 PERSONAGENS IDENTIFICADOS ===")
            for i, (nome, freq) in enumerate(resultados.most_common(20), 1):
                print(f"{i:2d}. {nome}: {freq} aparições")
            
            # Mostra estatísticas adicionais
            print(f"\n=== ESTATÍSTICAS ===")
            print(f"Total de personagens únicos: {len(set(analisador.nomes_proprios))}")
            print(f"Total de aparições de personagens: {sum(resultados.values())}")
            
            if resultados:
                mais_frequente = resultados.most_common(1)[0]
                print(f"Personagem mais frequente: {mais_frequente[0]} ({mais_frequente[1]} aparições)")
                
                # Calcula porcentagem do personagem mais frequente
                total_aparicoes = sum(resultados.values())
                porcentagem = (mais_frequente[1] / total_aparicoes) * 100
                print(f"Representa {porcentagem:.1f}% de todas as aparições de personagens")
    
    else:
        print("Nenhum PDF encontrado na pasta 'dados'")
        print("\nPara testar o analisador:")
        print("1. Coloque um PDF na pasta 'dados'")
        print("2. Execute este script novamente")
        print("3. Ou use o exemplo com texto abaixo")

def exemplo_com_texto():
    """
    Exemplo usando texto direto (útil para testar sem PDF)
    """
    print("\n=== EXEMPLO COM TEXTO DIRETO ===")
    
    # Texto de exemplo com personagens
    texto_exemplo = """
    Dom Casmurro é um romance de Machado de Assis. Bentinho, o protagonista, 
    narra sua história desde a infância. Sua mãe, Dona Glória, sempre quis 
    que ele fosse padre. Capitu, sua vizinha e futura esposa, é uma personagem 
    misteriosa. Escobar, amigo de Bentinho, também é importante na trama.
    
    Bentinho e Capitu se casam e têm um filho chamado Ezequiel. José Dias, 
    agregado da família, sempre observa tudo. Dona Fortunata, mãe de Capitu, 
    é uma mulher simples. Padre Cabral é o confessor da família.
    
    Bentinho suspeita que Capitu o traiu com Escobar. Ezequiel se parece 
    muito com Escobar, o que aumenta as suspeitas. Bentinho fica obcecado 
    com essa ideia e acaba se tornando um homem amargo.
    
    No final, Bentinho vive isolado, escrevendo suas memórias. Capitu e 
    Ezequiel morrem, e Bentinho fica sozinho com suas dúvidas.
    """
    
    # Cria analisador
    analisador = AnalisadorPDF()
    
    # Define o texto diretamente
    analisador.texto_completo = texto_exemplo
    
    # Processa o texto
    analisador.tokenizar_texto()
    analisador.identificar_personagens()
    
    # Mostra resultados
    print("Personagens identificados no texto:")
    for nome, freq in analisador.freq_nomes.most_common():
        print(f"- {nome}: {freq} aparições")
    
    # Cria gráficos
    print("\nCriando gráficos...")
    fig_freq = analisador.criar_grafico_frequencia()
    if fig_freq:
        fig_freq.savefig('../../resultados/graficos/exemplo_personagens_frequencia.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de frequência salvo")
    
    fig_disp = analisador.criar_grafico_dispersao()
    if fig_disp:
        fig_disp.savefig('../../resultados/graficos/exemplo_personagens_dispersao.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de dispersão salvo")

def instrucoes_uso():
    """
    Mostra instruções de como usar o analisador
    """
    print("\n=== INSTRUÇÕES DE USO ===")
    print("Para usar o AnalisadorPDF com seus próprios PDFs:")
    print()
    print("1. INSTALAÇÃO:")
    print("   pip install -r dados/requirements_pdf.txt")
    print()
    print("2. COLOCAR PDF:")
    print("   - Coloque seu PDF na pasta 'dados'")
    print("   - O script detectará automaticamente")
    print()
    print("3. EXECUTAR:")
    print("   python scripts/big_data/analise_pdf_personagens.py")
    print()
    print("4. USO PROGRAMÁTICO:")
    print("   from big_data.analise_pdf_personagens import AnalisadorPDF")
    print("   analisador = AnalisadorPDF()")
    print("   resultados = analisador.analisar_pdf('caminho/para/seu.pdf')")
    print()
    print("5. RESULTADOS:")
    print("   - Gráficos salvos em 'resultados/graficos/'")
    print("   - Lista dos 20 personagens mais frequentes")
    print("   - Gráfico de dispersão das aparições")
    print()
    print("CARACTERÍSTICAS DO ANALISADOR:")
    print("✓ Extrai texto de PDFs usando PyMuPDF ou PyPDF2")
    print("✓ Identifica nomes próprios baseado em capitalização")
    print("✓ Filtra palavras comuns e números")
    print("✓ Cria gráficos de frequência e dispersão")
    print("✓ Suporta acentos e caracteres especiais")
    print()
    print("LIMITAÇÕES:")
    print("- Identificação baseada apenas em capitalização")
    print("- Pode incluir falsos positivos (lugares, títulos, etc.)")
    print("- Para análise mais precisa, considere usar NLTK ou spaCy")

if __name__ == "__main__":
    # Executa exemplos
    exemplo_analise_pdf()
    exemplo_com_texto()
    instrucoes_uso() 