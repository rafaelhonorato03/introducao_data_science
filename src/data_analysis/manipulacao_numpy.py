import numpy as np

# Gerando dados aleatórios

dados = np.random.rand(2,3)
print(dados)

# tipo de array
print(dados.dtype)
print(dados.shape)
print(dados.ndim)

lista = [1, 2, 3, 4, 5]
dados2 = np.array(lista)
print(dados2)

lista2 = [[1, 2, 3], [4, 5, 6]]
dados3 = np.array(lista2)
print(dados3)

dadoszero = np.zeros(10)
print(dadoszero)

dadoszero1 = np.zeros((2, 3), dtype=int)
print(dadoszero1)

dadosum = np.ones((2, 3), dtype=int)
print(dadosum)

dadosseq = np.arange(10)
print(dadosseq)

dadosseq1 = np.arange(0, 20, 2)
print(dadosseq1)

dadosseqf = dadosseq.astype(np.float64)
print(dadosseqf)

dados4 = np.array([[1, 2], [3, 4]])
print(dados4)

print(dados4*dados4)
print(dados4-dados4)
print(dados4+dados4)
print(1/dados4)
print(dados4>dados4)
print(dadosseq[5])
print(dadosseq[1:5])
dadosseq[2:5] = 0
print(dadosseq)
dadosseq[1] = 1000
print(dadosseq)

fatia = dadosseq[1:5].copy()
print(fatia)
fatia[0] = 100
print(fatia)
print(dadosseq)

# Mascara

mascara = dadosseq > 5
print(mascara)

multi = np.dot(dados4, dados4)
print(multi)