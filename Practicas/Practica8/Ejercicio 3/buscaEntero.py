''' By Jerónimo Vicente '''

texto = input("Introduce un texto: ")

numero = 0
while numero < len(texto):
    if texto[numero].isdigit():
        print("Se ha encontrado un número en el texto.")
        break

    else:
        numero += 1

if numero == len(texto):
    print("No se ha encontrado ningún número en el texto.")

print("\nFin del programa.")
