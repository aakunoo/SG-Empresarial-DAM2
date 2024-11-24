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

