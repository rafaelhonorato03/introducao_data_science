# --- verificar_leia.py ---

print("="*50)
print("INICIANDO VERIFICAÇÃO DA BIBLIOTECA DE SENTIMENTO")
print("="*50)

# Verificando a instalação
try:
    import pkg_resources
    versao = pkg_resources.get_distribution('leia-br').version
    print(f"Versão do pacote 'leia-br' encontrada: {versao}\n")
except Exception:
    print("Não foi possível encontrar o pacote 'leia-br'. Você instalou com 'pip install leia-br'?\n")

# --- TENTATIVA 1 ---
print("\n--- Tentativa 1: Importar de 'LeIA' (como na documentação) ---")
try:
    import LeIA
    print("SUCESSO! Conteúdo de 'LeIA':")
    print(dir(LeIA))
except Exception as e:
    print(f"FALHA: {e}")

# --- TENTATIVA 2 ---
print("\n--- Tentativa 2: Importar de 'leia.leia' (como nos erros) ---")
try:
    import leia.leia
    print("SUCESSO! Conteúdo de 'leia.leia':")
    print(dir(leia.leia))
except Exception as e:
    print(f"FALHA: {e}")

# --- TENTATIVA 3 ---
print("\n--- Tentativa 3: Importar a classe direto de 'leia.leia' ---")
try:
    from leia.leia import leia
    print("SUCESSO ao importar 'leia' de 'leia.leia'")
    analisador = leia()
    print("Instância criada com sucesso!")
except Exception as e:
    print(f"FALHA: {e}")
    
# --- TENTATIVA 4 ---
print("\n--- Tentativa 4: Importar a classe direto de 'LeIA' ---")
try:
    from LeIA import SentimentIntensityAnalyzer
    print("SUCESSO ao importar 'SentimentIntensityAnalyzer' de 'LeIA'")
    analisador = SentimentIntensityAnalyzer()
    print("Instância criada com sucesso!")
except Exception as e:
    print(f"FALHA: {e}")


print("\n" + "="*50)
print("VERIFICAÇÃO CONCLUÍDA")
print("="*50)