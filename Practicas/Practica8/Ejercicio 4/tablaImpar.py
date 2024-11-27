''' By Jeronimo Vicente '''

num = int(input("Introduce un número entero: "))

for i in range(1,11):
    resultado = f"{num} x {i} = {num * i}"
    if i % 2 == 0:
        continue
    print(resultado)

texto = input("\nIntroduce un texto: ")
for j in range(num):
    print(texto)