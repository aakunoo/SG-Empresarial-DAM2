''' By Jerónimo Vicente '''

def calcula_area(figura):
    def calcular(base, altura):
        if figura == "triangulo":
            return base * altura / 2
        elif figura == "rectangulo":
            return base * altura
    return calcular

caTriangulo = calcula_area("triangulo")
print(caTriangulo(12, 7))

fResto = lambda j, l: j % l
print(fResto(414,16))

def mayusculas(func):
    def envoltura(*argumentos, **kwargumentos):
        r = func(*argumentos, **kwargumentos)
        return r.upper()
    return envoltura

def concatena(cadena1, cadena2):
    return cadena1 + cadena2

print(concatena("Feliz ", "Cumpleaños"))

@mayusculas
def concatena(cadena1, cadena2):
    return cadena1 + cadena2

print(concatena("Feliz ", "Cumpleaños"))


def potencia(base, exponente, limite):
    r = base ** exponente

    if r >= limite:
        return exponente - 1
    else:
        return potencia(base, exponente + 1, limite)

print(potencia(2, 1, 100))
print(potencia(5, 1, 1000000))

def por5(unEntero):
    global valor
    valor = unEntero * 5

valor = 18
print(valor)

por5(valor)
print(valor)
