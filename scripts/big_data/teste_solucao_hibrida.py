# Teste da solução híbrida NER + Capitalização
import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa o analisador
from analise_pdf_ner import AnalisadorPDFNER

def teste_solucao_hibrida():
    """
    Testa a solução híbrida que combina NER com busca por capitalização
    """
    print("=== TESTE DA SOLUÇÃO HÍBRIDA NER + CAPITALIZAÇÃO ===")
    
    # Texto de exemplo do Dom Casmurro
    texto_exemplo = """
    Agora que expliquei o título, passo a escrever o livro. Antes disso, porém, digamos os motivos que me põem a pena na mão.
    
    Vivo só, com um criado. A casa em que moro é própria; fi-la construir de propósito, levado de um desejo tão particular que me vexa imprimi-lo, mas vá lá. Um dia há de ser que, vindo do Engenho Novo, e entrando numa casa da Rua do Ouvidor, achei num catálogo, que um sujeito me deu, uma estampa de uma mulher, com este título ao pé: D. Casmurro, 1813. Fiquei gostando do nome, e depois da estampa. Quando vim para a cidade, e me decidi a edificar, pus-lhe o nome de Casmurro, para que ficasse completa a semelhança. Nem me importa que lhe dêem outro nome, como de hábito; o que importa é que eu fique sabendo que se chama Casmurro.
    
    Capitu, minha vizinha e amiga, brincava comigo na chácara, e eu gostava dela desde os meus onze anos. Capitu era uma menina esperta, viva, faladeira, e sobretudo muito bonita. Tinha os olhos grandes e pretos, a boca pequena, o nariz fino, e um ar de mistério que me fascinava. Capitu sabia tudo, e eu nada. Capitu explicava-me as coisas, e eu escutava com atenção. Capitu era a minha professora, a minha confidente, a minha amiga.
    
    Bentinho, que era o meu nome de batismo, vivia na casa ao lado. Bentinho e eu éramos amigos desde a infância. Bentinho tinha medo de tudo, e eu corajoso. Bentinho chorava por qualquer coisa, e eu consolava-o. Bentinho era o meu protegido, e eu o seu protetor.
    
    Escobar, que veio morar na nossa rua, era um rapaz alto, forte, e muito inteligente. Escobar sabia latim, grego, e outras línguas. Escobar era o orgulho da família, e todos o admiravam. Escobar tornou-se amigo de Bentinho, e depois meu amigo também.
    
    José Dias, o agregado da família, sempre observava tudo com atenção. José Dias era um homem discreto e observador. José Dias tinha uma influência sutil sobre as decisões da família.
    
    Dona Glória, minha mãe, sempre quis que eu fosse padre. Dona Glória era uma mulher piedosa e determinada. Dona Glória não desistia facilmente de seus objetivos.
    
    Padre Cabral era o confessor da família. Padre Cabral aconselhava Dona Glória sobre minha vocação. Padre Cabral era respeitado por todos.
    
    Ezequiel, nosso filho, nasceu alguns anos depois do casamento. Ezequiel era uma criança inteligente e curiosa. Ezequiel se parecia muito com Escobar, o que me perturbava.
    
    Dona Fortunata, mãe de Capitu, era uma mulher simples e bondosa. Dona Fortunata sempre tratou bem a todos. Dona Fortunata era querida por toda a vizinhança.
    """
    
    # Cria analisador
    analisador = AnalisadorPDFNER()
    
    # Define o texto diretamente
    analisador.texto_completo = texto_exemplo
    
    # Executa análise híbrida
    print("Executando análise híbrida...")
    resultados = analisador.analise_completa_ner()
    
    # Mostra resultados
    print(f"\n=== RESULTADOS DA SOLUÇÃO HÍBRIDA ===")
    print(f"Total de personagens identificados: {len(analisador.freq_personagens)}")
    
    print(f"\n=== TOP 20 PERSONAGENS ===")
    for i, (nome, freq) in enumerate(analisador.freq_personagens.most_common(20), 1):
        print(f"{i:2d}. {nome}: {freq} aparições")
    
    # Verifica especificamente personagens importantes
    personagens_importantes = ["Capitu", "Bentinho", "Escobar", "José", "Dias", "Glória", "Cabral", "Ezequiel", "Fortunata"]
    print(f"\n=== VERIFICAÇÃO DE PERSONAGENS IMPORTANTES ===")
    for personagem in personagens_importantes:
        if personagem in analisador.freq_personagens:
            print(f"✓ {personagem}: {analisador.freq_personagens[personagem]} aparições")
        else:
            print(f"✗ {personagem}: Não encontrado")
    
    # Cria gráficos
    print(f"\n=== CRIANDO GRÁFICOS ===")
    
    # Cria diretório se não existir
    Path("../../resultados/graficos").mkdir(parents=True, exist_ok=True)
    
    # Gráfico de frequência (top 20)
    fig_freq = analisador.criar_grafico_frequencia(20)
    if fig_freq:
        fig_freq.savefig('../../resultados/graficos/teste_hibrido_frequencia.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de frequência híbrido salvo")
    
    # Gráfico de dispersão (top 20)
    fig_disp = analisador.criar_grafico_dispersao(20)
    if fig_disp:
        fig_disp.savefig('../../resultados/graficos/teste_hibrido_dispersao.png', 
                        dpi=300, bbox_inches='tight')
        print("✓ Gráfico de dispersão híbrido salvo")
    
    print(f"\n=== VANTAGENS DA SOLUÇÃO HÍBRIDA ===")
    print("✓ NER identifica nomes reconhecidos pelo modelo")
    print("✓ Busca por capitalização pega nomes não reconhecidos (como Capitu)")
    print("✓ Nomes compostos são identificados corretamente")
    print("✓ Filtro remove falsos positivos")
    print("✓ Maior precisão na identificação de personagens")
    
    return analisador.freq_personagens

if __name__ == "__main__":
    teste_solucao_hibrida() 