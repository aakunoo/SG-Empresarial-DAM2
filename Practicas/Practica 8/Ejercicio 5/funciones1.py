''' By Jerónimo Vicente '''

def mayor(x, y):
    print(f"El número mayor entre {x} y {y} es: {max(x, y)}.")

mayor(6,90)
mayor(x=45, y=89)

def area(altura, base=8):
    return base * altura

print(area(7, 3))
print(area(altura=5))

def suma(*numeros):
    return sum(numeros)
