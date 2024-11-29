from Ejer_Python.funciones1 import mayor, suma
from Ejer_Python.funciones2 import calcula_area as c_area, potencia as pot
from Ejer_Python.objetosYclases2 import *

num = (20, 56, 15, 89)
print(suma(num))

rect = c_area("rectangulo")
print(rect(9,6))

print(pot(7,1,5000))

DeAgua = vAcuatico("kayak", False, "parado", 2.90, 300)
DeAgua.mover()

print(f"El estado es {DeAgua.estado}, y su nombre oculto es: {DeAgua.nombreOculto}")

