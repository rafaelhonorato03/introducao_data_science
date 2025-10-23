from datetime import date

idade = int(input("Digite sua idade: "))

if idade > 18:
    print("Você é maior de idade")
elif idade == 18:
    print("Você não é nem maior, nem menor de idade!")
else:
    print("Você é menor de idade")

# Outra forma de apresentar condicionais, mais simples e direta
print("Maior de idade") if idade >= 18 else print("Menor de didade")

#switch case
a = "Rafael"
match a:
    case "João":
        print("Não é Rafael")
    case "Rafael":
        print("É Rafael")

# Provinha de teste
ano_nascimento = int(input("Qual o seu ano de nascimento? "))
data_atual = date.today()
data_atual = data_atual.year
idade = data_atual - ano_nascimento

if idade >= 18:
    print(f"Você é maior e tem {idade} anos de idade")
    print("Digite o seu título de eleitor: ")
else:
    print(f"Você é menor, pois tem {idade} anos")
    print("Digite o documento do seu resposável")

# Laços de repetição
a = 1

while a < 10:
    print("Teste")