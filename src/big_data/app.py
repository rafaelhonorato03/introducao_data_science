# Arquivo: app.py (VERSÃO DE DIAGNÓSTICO TEMPORÁRIA)

import streamlit as st
import os
import sys

st.set_page_config(layout="wide")
st.title("Página de Diagnóstico de Deploy 🕵️")
st.header("Investigando o Ambiente do Servidor do Streamlit")

st.info("Esta página nos ajudará a entender por que o `ImportError` está acontecendo.")

# --- INVESTIGAÇÃO ---

# 1. Mostrar o Diretório de Trabalho Atual (CWD - Current Working Directory)
# É a pasta a partir da qual o seu script está sendo executado.
try:
    cwd = os.getcwd()
    st.subheader("1. Diretório de Trabalho Atual")
    st.code(cwd, language='bash')
except Exception as e:
    st.error(f"Não foi possível obter o diretório de trabalho: {e}")


# 2. Listar todos os arquivos e pastas nesse diretório
# Esta é a verificação mais importante. Ela nos dirá se o seu arquivo está onde deveria estar.
st.subheader(f"2. Arquivos e Pastas encontrados em `{cwd}`")
try:
    files_in_cwd = os.listdir(cwd)
    st.code("\n".join(sorted(files_in_cwd)), language='bash')

    # Verificação CRÍTICA
    st.subheader("3. Verificação do Arquivo `analisador_personagens.py`")
    if 'analisador_personagens.py' in files_in_cwd:
        st.success("✅ SUCESSO! O arquivo 'analisador_personagens.py' FOI ENCONTRADO na pasta do script principal!")
        st.write("Se este teste passou, o erro de importação é provavelmente devido a um problema de 'path' do Python (veja abaixo) ou um erro de sintaxe dentro do próprio arquivo.")
    else:
        st.error("❌ FALHA! O arquivo 'analisador_personagens.py' NÃO FOI ENCONTRADO na pasta do script principal.")
        st.warning("Esta é a causa mais provável do erro. Verifique a estrutura de pastas e a configuração de 'Main file path' no seu deploy.")

except Exception as e:
    st.error(f"Não foi possível listar os arquivos no diretório de trabalho: {e}")


# 3. Mostrar os caminhos que o Python usa para encontrar módulos (sys.path)
# O Python procura os arquivos para importar em cada uma das pastas listadas aqui.
st.subheader("4. Caminhos de Importação do Python (sys.path)")
try:
    st.code("\n".join(sys.path), language='bash')
except Exception as e:
    st.error(f"Não foi possível obter o sys.path: {e}")