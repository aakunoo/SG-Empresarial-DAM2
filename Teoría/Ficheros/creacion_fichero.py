"""
Module for creating a file with car prices.
"""

coches = {
    "Mercedes 360": 45000,
    "BMW 540": 85000,
    "Renault Megane": 25000
}

fichero = open("coches.txt", "w")

for coche, precio in coches.items():
    fichero.write(coche + "," + str(precio) + "\n")

fichero.close()
