#!/usr/bin/env python3
# ==========================================
# DEMONSTRAÇÃO RÁPIDA DO ANALISADOR AVANÇADO
# ==========================================
# Mostra todas as funcionalidades em ação com dados de exemplo

import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def criar_texto_exemplo():
    """Cria um texto de exemplo com personagens e relacionamentos"""
    
    texto = """
    CAPÍTULO I - O LIVRO
    
    José Gabriel era um homem simples que vivia na cidade de São Paulo. Maria Clara, sua esposa, sempre o apoiava em todas as decisões. Eles formavam um casal muito unido.
    
    Pedro Santos, o vizinho, frequentemente visitava a família. Ele era um comerciante respeitado na região. Ana Beatriz, filha de José Gabriel e Maria Clara, adorava brincar com Carlos Eduardo, filho de Pedro Santos.
    
    Dona Rosa Silva, a professora de Ana Beatriz, sempre elogiava seu comportamento exemplar. Dr. João Silva, o médico da família, era muito atencioso e competente.
    
    CAPÍTULO II - A LOJA
    
    José Gabriel trabalhava com Sr. Antônio Santos na loja do centro. Eles eram sócios há muitos anos. Maria Clara conversava com Dona Clara Costa na feira todas as manhãs.
    
    Pedro Santos e Carlos Eduardo iam pescar com Tio José Pereira nos fins de semana. Ana Beatriz estudava com sua amiga Beatriz Oliveira na escola.
    
    CAPÍTULO III - A FESTA
    
    Na festa de aniversário de Ana Beatriz, todos os personagens se reuniram. José Gabriel e Maria Clara organizaram tudo com muito carinho. Pedro Santos trouxe presentes para a menina.
    
    Dona Rosa Silva fez um discurso emocionante sobre Ana Beatriz. Dr. João Silva contou histórias engraçadas. Sr. Antônio Santos dançou com Dona Clara Costa.
    
    Tio José Pereira tocou violão e todos cantaram. Beatriz Oliveira ajudou Ana Beatriz a abrir os presentes. Carlos Eduardo fez uma apresentação de mágica.
    
    CAPÍTULO IV - O FUTURO
    
    José Gabriel e Maria Clara planejavam uma viagem. Pedro Santos ofereceu-se para cuidar da casa. Ana Beatriz ficou muito feliz com a notícia.
    
    Dona Rosa Silva prometeu enviar lições por correio. Dr. João Silva deu dicas de saúde para a viagem. Sr. Antônio Santos emprestou dinheiro para as passagens.
    
    Dona Clara Costa fez um bolo especial para a despedida. Tio José Pereira contou histórias de suas próprias viagens. Beatriz Oliveira prometeu escrever cartas.
    
    Carlos Eduardo ficou triste, mas entendeu que era importante para a família.
    """
    
    return texto

def demo_analise_basica():
    """Demonstra a análise básica de personagens"""
    print("🔍 DEMONSTRAÇÃO: Análise Básica de Personagens")
    print("-" * 50)
    
    try:
        from analise_pdf_ner import AnalisadorPDFNER
        
        # Inicializa analisador
        analisador = AnalisadorPDFNER()
        
        # Usa texto de exemplo
        texto = criar_texto_exemplo()
        analisador.texto_completo = texto
        
        # Executa análise básica
        resultados = analisador.analise_completa_ner()
        
        print(f"📊 Resultados da análise básica:")
        print(f"   - Total de caracteres: {len(texto):,}")
        print(f"   - Personagens identificados: {len(resultados)}")
        
        if resultados:
            print(f"   - Top 5 personagens:")
            for i, (nome, freq) in enumerate(resultados.most_common(5), 1):
                print(f"     {i}. {nome}: {freq} aparições")
        
        return analisador
        
    except Exception as e:
        print(f"❌ Erro na análise básica: {e}")
        return None

def demo_analise_avancada(analisador):
    """Demonstra as análises avançadas"""
    print("\n🔬 DEMONSTRAÇÃO: Análises Avançadas")
    print("-" * 50)
    
    if not analisador:
        print("❌ Analisador não disponível")
        return
    
    try:
        # Análise por capítulos
        print("📚 Análise por capítulos...")
        capitulos = analisador.dividir_em_capitulos()
        print(f"   - Capítulos identificados: {len(capitulos)}")
        
        # Análise de coocorrências
        print("🔗 Análise de coocorrências...")
        coocorrencias = analisador.analisar_coocorrencias(janela_palavras=100)
        print(f"   - Personagens analisados: {len(coocorrencias)}")
        
        # Rede de personagens
        print("🌐 Criação da rede de personagens...")
        rede = analisador.criar_rede_personagens()
        if rede:
            print(f"   - Nós na rede: {rede.number_of_nodes()}")
            print(f"   - Arestas na rede: {rede.number_of_edges()}")
        
        # Análise de sentimentos
        print("📈 Análise de sentimentos...")
        sentimentos = analisador.analisar_sentimentos_personagens()
        print(f"   - Personagens analisados: {len(sentimentos)}")
        
        # Análise temporal
        print("⏰ Análise temporal...")
        temporal = analisador.analisar_personagens_por_capitulo()
        print(f"   - Capítulos analisados: {len(temporal)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas análises avançadas: {e}")
        return False

def demo_visualizacoes(analisador):
    """Demonstra a criação de visualizações"""
    print("\n📊 DEMONSTRAÇÃO: Criação de Visualizações")
    print("-" * 50)
    
    if not analisador:
        print("❌ Analisador não disponível")
        return
    
    try:
        # Cria diretório para resultados
        Path("resultados/graficos").mkdir(parents=True, exist_ok=True)
        
        # Gráfico de frequência
        print("📈 Criando gráfico de frequência...")
        fig_freq = analisador.criar_grafico_frequencia(10)
        if fig_freq:
            fig_freq.savefig('resultados/graficos/demo_frequencia.png', dpi=300, bbox_inches='tight')
            print("   ✅ Gráfico de frequência salvo")
        
        # Gráfico de dispersão
        print("📊 Criando gráfico de dispersão...")
        fig_disp = analisador.criar_grafico_dispersao(10)
        if fig_disp:
            fig_disp.savefig('resultados/graficos/demo_dispersao.png', dpi=300, bbox_inches='tight')
            print("   ✅ Gráfico de dispersão salvo")
        
        # Rede de personagens
        if analisador.rede_personagens:
            print("🌐 Criando visualização da rede...")
            fig_rede = analisador.visualizar_rede_personagens()
            if fig_rede:
                fig_rede.savefig('resultados/graficos/demo_rede.png', dpi=300, bbox_inches='tight')
                print("   ✅ Visualização da rede salva")
        
        # Gráfico de sentimentos
        if analisador.analise_sentimentos:
            print("😊 Criando gráfico de sentimentos...")
            fig_sent = analisador.criar_grafico_sentimentos()
            if fig_sent:
                fig_sent.savefig('resultados/graficos/demo_sentimentos.png', dpi=300, bbox_inches='tight')
                print("   ✅ Gráfico de sentimentos salvo")
        
        # Gráfico temporal
        if analisador.analise_temporal:
            print("⏰ Criando gráfico temporal...")
            fig_temp = analisador.criar_grafico_evolucao_temporal()
            if fig_temp:
                fig_temp.savefig('resultados/graficos/demo_temporal.png', dpi=300, bbox_inches='tight')
                print("   ✅ Gráfico temporal salvo")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na criação de visualizações: {e}")
        return False

def demo_relatorio(analisador):
    """Demonstra a geração de relatório"""
    print("\n📋 DEMONSTRAÇÃO: Geração de Relatório")
    print("-" * 50)
    
    if not analisador:
        print("❌ Analisador não disponível")
        return
    
    try:
        # Gera relatório completo
        print("📄 Gerando relatório completo...")
        relatorio = analisador.gerar_relatorio_completo()
        
        if relatorio:
            print("✅ Relatório gerado com sucesso!")
            print(f"   - Arquivo: resultados/relatorio_completo.json")
            print(f"   - Personagens: {relatorio['personagens']['total_identificados']}")
            print(f"   - Capítulos: {relatorio['metadata']['total_capitulos']}")
            print(f"   - Análise de sentimentos: {'Sim' if relatorio.get('analise_sentimentos') else 'Não'}")
            print(f"   - Coocorrências: {'Sim' if relatorio.get('coocorrencias') else 'Não'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na geração de relatório: {e}")
        return False

def demo_interface_web():
    """Demonstra a interface web"""
    print("\n🌐 DEMONSTRAÇÃO: Interface Web")
    print("-" * 50)
    
    try:
        # Verifica se o arquivo existe
        app_file = Path("app_streamlit.py")
        if app_file.exists():
            print("✅ Arquivo da aplicação Streamlit encontrado")
            print("🚀 Para iniciar a interface web, execute:")
            print("   streamlit run scripts/big_data/app_streamlit.py")
            print("\n📱 Recursos da interface:")
            print("   - Upload de PDFs via web")
            print("   - Configurações interativas")
            print("   - Visualizações dinâmicas")
            print("   - Múltiplas abas de análise")
            print("   - Download de relatórios")
            return True
        else:
            print("❌ Arquivo da aplicação Streamlit não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro na verificação da interface web: {e}")
        return False

def main():
    """Função principal da demonstração"""
    
    print("🎬 DEMONSTRAÇÃO RÁPIDA DO ANALISADOR AVANÇADO")
    print("=" * 60)
    print("Este script demonstra todas as funcionalidades implementadas")
    print()
    
    # Executa demonstrações
    sucessos = 0
    total_demos = 5
    
    # 1. Análise básica
    analisador = demo_analise_basica()
    if analisador:
        sucessos += 1
    
    # 2. Análises avançadas
    if demo_analise_avancada(analisador):
        sucessos += 1
    
    # 3. Visualizações
    if demo_visualizacoes(analisador):
        sucessos += 1
    
    # 4. Relatório
    if demo_relatorio(analisador):
        sucessos += 1
    
    # 5. Interface web
    if demo_interface_web():
        sucessos += 1
    
    # Resumo
    print(f"\n{'='*60}")
    print("📊 RESUMO DA DEMONSTRAÇÃO")
    print("=" * 60)
    print(f"Demonstrações executadas: {sucessos}/{total_demos}")
    
    if sucessos == total_demos:
        print("\n🎉 TODAS AS DEMONSTRAÇÕES FORAM BEM-SUCEDIDAS!")
        print("\n🚀 Próximos passos:")
        print("1. Explore os gráficos gerados em 'resultados/graficos/'")
        print("2. Veja o relatório completo em 'resultados/relatorio_completo.json'")
        print("3. Teste com seus próprios PDFs:")
        print("   - Coloque um PDF na pasta 'dados/'")
        print("   - Execute: python scripts/big_data/analise_pdf_ner.py")
        print("4. Use a interface web:")
        print("   - Execute: streamlit run scripts/big_data/app_streamlit.py")
    else:
        print(f"\n⚠️ {total_demos - sucessos} demonstração(ões) falharam.")
        print("Verifique se todas as dependências estão instaladas:")
        print("python scripts/big_data/install_dependencies.py")
    
    print(f"\n📚 Recursos implementados:")
    print("✅ Identificação de personagens com NER")
    print("✅ Análise de coocorrência entre personagens")
    print("✅ Análise de sentimentos por personagem")
    print("✅ Análise temporal por capítulos")
    print("✅ Rede de relacionamentos")
    print("✅ Visualizações interativas")
    print("✅ Interface web com Streamlit")
    print("✅ Geração de relatórios completos")
    
    return sucessos == total_demos

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 