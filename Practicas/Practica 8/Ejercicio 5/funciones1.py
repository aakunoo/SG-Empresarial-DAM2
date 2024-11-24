''' By Jerónimo Vicente '''

def mayor(x, y):
    """
     Compara dos números y muestra el mayor de ellos.

     Parámetros:
     x (int o float): Primer número a comparar.
     y (int o float): Segundo número a comparar.

     Devuelve:
     None
     """
    print(f"El número mayor entre {x} y {y} es: {max(x, y)}.")

mayor(6,90)
mayor(x=45, y=89)

def area(altura, base=8):
    """
    Calcula el área de un rectángulo dado su altura y base.

    Parámetros:
    altura (int o float): Altura del rectángulo.
    base (int o float, opcional): Base del rectángulo, por defecto es 8.

    Devuelve:
    int o float: El área del rectángulo.
        """
    return base * altura

print(area(7, 3))
print(area(altura=5))

def suma(*numeros):
    return sum(*numeros)

valores = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

print(suma(valores))

def peque(**diccionario):
    return min(diccionario, key=diccionario.get)

habitaciones = {"salón": 20, "terraza": 10, "lavadero": 5, "despacho": 7, "cuarto": 15}

print(peque(**habitaciones))

def repetir(texto, /,*, entero):
    for _ in range(entero): # _ es se usa por convención para variables que no se van a usar.
        print(texto)

repetir("repito", entero=6)

def funcion(func1, func2):
    func1()
    print(func2())

asignaturas = {"Acceso a Datos": 5, "Programación": 6, "Sistemas": 8, "Interfaces": 3}
funcion(mayor(14, 23), print(peque(**asignaturas)))


help(mayor)
help(area)