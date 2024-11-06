fichero = open("coches.txt", "a")

coche = input("Introduce un coche: ")
precio = input("Introduce el precio: ")

while coche != "":
    fichero.write(coche + "," + precio + "\n")
    coche = input("Introduce un coche: ")
    precio = input("Introduce el precio: ")

fichero.close()
