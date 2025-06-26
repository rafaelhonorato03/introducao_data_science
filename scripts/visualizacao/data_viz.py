# Script para aprender diferentes tipos de gráficos em Python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pygal
import os

# ==========================================
# 1. GRÁFICO DE PONTOS (SCATTER PLOT)
# ==========================================
# Mostra a relação entre duas listas de números
print("Criando gráfico de pontos...")
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [1, 2, 3, 4, 2, 6, 7, 8, 9, 10]

plt.scatter(x, y)  # Cria pontos no gráfico
plt.title('Gráfico de Pontos')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.show()

# ==========================================
# 2. GRÁFICO DE LINHA - FUNÇÃO QUADRÁTICA
# ==========================================
# Plota uma função matemática (y = x²)
print("Criando gráfico de função matemática...")
x1 = np.arange(-100, 100, 1)  # Cria números de -100 até 100

plt.plot(x1, x1**2)  # Desenha a linha da função y = x²
plt.title('Função y = x²')
plt.xlabel('x')
plt.ylabel('y = x²')
plt.grid(True)  # Adiciona linhas de grade
plt.show()

# ==========================================
# 3. FUNÇÃO QUADRÁTICA DESLOCADA
# ==========================================
# Plota y = x² - 2000 (função deslocada para baixo)
print("Criando segunda função matemática...")
plt.plot(x1, (x1**2) - 2000)
plt.title('Função y = x² - 2000')
plt.xlabel('x')
plt.ylabel('y = x² - 2000')
plt.grid(True)
plt.show()

# ==========================================
# 4. FUNÇÕES TRIGONOMÉTRICAS (SENO E COSSENO)
# ==========================================
# Plota gráficos ondulados (seno e cosseno)
print("Criando gráficos de seno e cosseno...")
phi = np.linspace(0, 3*np.pi, 150)  # Cria 150 pontos de 0 a 3π
plt.plot(phi, np.sin(phi), label='seno', color='blue')
plt.plot(phi, np.cos(phi), label='cosseno', color='red')
plt.title('Funções Seno e Cosseno')
plt.xlabel('Ângulo (radianos)')
plt.ylabel('Valor')
plt.legend()
plt.grid(True)
plt.show()

# ==========================================
# 5. DADOS FICTÍCIOS DE VACINAÇÃO
# ==========================================
# Cria dados simulados para 30 dias
print("Criando dados de vacinação...")
dias = np.arange(1, 31)  # Dias 1 a 30
vacinados = np.random.randint(0, 1000, 30)  # Números aleatórios de vacinados
contagios = np.random.randint(0, 700, 30)   # Números aleatórios de contágios

# ==========================================
# 6. GRÁFICO COM BARRAS E LINHA JUNTOS
# ==========================================
# Mostra vacinados em barras e contágios em linha
print("Criando gráfico combinado...")
plt.style.use('default')  # Usa estilo padrão
plt.figure(figsize=(12, 6))  # Define tamanho do gráfico

plt.bar(dias, vacinados, alpha=0.7, label='Vacinados', color='skyblue')  # Barras azuis
plt.plot(dias, contagios, 'r', linewidth=2, label='Contágios', marker='o')  # Linha vermelha com pontos

plt.title('Vacinação vs Contágios por Dia')
plt.xlabel('Dias')
plt.ylabel('Número de Pessoas')
plt.legend()  # Mostra legenda
plt.grid(True, alpha=0.3)
plt.tight_layout()  # Ajusta layout automaticamente
plt.show()

# ==========================================
# 7. USANDO PANDAS PARA CRIAR GRÁFICO
# ==========================================
# Pandas facilita a criação de gráficos a partir de tabelas
print("Criando gráfico com Pandas...")
dados = pd.DataFrame(dias, columns=['dias'])
dados['Contagios'] = contagios
dados['Vacinados'] = vacinados

dados.plot(kind='bar', x='dias', y='Vacinados', figsize=(12, 6))  # Gráfico de barras do pandas
plt.title('Vacinados por Dia')
plt.xlabel('Dias')
plt.ylabel('Vacinados')
plt.xticks(rotation=45)  # Rotaciona labels do eixo X
plt.tight_layout()
plt.show()

# ==========================================
# 8. USANDO SEABORN (BIBLIOTECA MAIS BONITA)
# ==========================================
# Seaborn cria gráficos mais bonitos automaticamente
print("Criando gráfico com Seaborn...")
plt.figure(figsize=(12, 6))
sns.barplot(data=dados, x='dias', y='Contagios', alpha=0.7, color='lightcoral')  # Barras do seaborn
sns.lineplot(data=dados, x='dias', y='Vacinados', color='red', linewidth=2, marker='o')  # Linha do seaborn
plt.title('Análise com Seaborn')
plt.xlabel('Dias')
plt.ylabel('Número de Pessoas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================
# 9. GRÁFICO DE PROGRESSO COM IMAGEM
# ==========================================
# Cria um gráfico de progresso cobrindo uma imagem
print("Criando gráfico de progresso...")
progress = 0.34  # 34% de progresso

# Verifica se a imagem existe
image_path = 'money.png'
if os.path.exists(image_path):
    # Carrega a imagem
    img = mpimg.imread(image_path)
    fig, ax = plt.subplots(figsize=(6, 6))

    # Mostra a imagem como fundo
    ax.imshow(img, extent=[0, 1, 0, 1])

    # Cobre parte da imagem com retângulo branco (progresso)
    ax.add_patch(patches.Rectangle((progress, 0), 1 - progress, 1, 
                                  color='white', alpha=0.7))

    ax.axis('off')  # Remove os eixos
    plt.title(f'Progresso: {progress*100:.0f}%', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
else:
    # Se não encontrar a imagem, cria gráfico simples
    print("Imagem não encontrada. Criando gráfico alternativo...")
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.barh(['Progresso'], [progress], color='green', alpha=0.7)
    ax.set_xlim(0, 1)
    ax.set_xlabel('Progresso')
    plt.title(f'Progresso: {progress*100:.0f}%', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

# ==========================================
# 10. GRÁFICO INTERATIVO COM PYGAL
# ==========================================
# Pygal cria gráficos que podem ser salvos como arquivos
print("Criando gráfico com Pygal...")
bar_chart = pygal.Bar()
bar_chart.title = 'Vacinados por dia'
bar_chart.x_labels = ['Dia 1', 'Dia 2', 'Dia 3', 'Dia 4', 'Dia 5']
bar_chart.add('Vacinados', [10, 20, 30, 25, 35])
bar_chart.add('Contágios', [5, 15, 25, 20, 30])

# Salva o gráfico como arquivo
output_file = 'bar_chart.svg'
bar_chart.render_to_file(output_file)
print(f"Gráfico salvo como '{output_file}'")

# ==========================================
# RESUMO FINAL
# ==========================================
print("\n" + "="*50)
print("RESUMO DO QUE VOCÊ APRENDEU:")
print("="*50)
print("1. Gráficos de pontos (scatter plot)")
print("2. Gráficos de linha para funções matemáticas")
print("3. Funções trigonométricas (seno e cosseno)")
print("4. Gráficos de barras")
print("5. Gráficos combinados (barras + linha)")
print("6. Visualização com Pandas")
print("7. Visualização com Seaborn (mais bonita)")
print("8. Gráficos de progresso")
print("9. Gráficos interativos com Pygal")
print("\nDICA: Use Seaborn para análises estatísticas e matplotlib para gráficos customizados!")