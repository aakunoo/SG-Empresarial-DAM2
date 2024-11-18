''' By Jeronimo Vicente. '''

numeroHijos = input("Introduce el número de hijos: ")
agnoNacimiento = input("Introduce el año de nacimiento: ")

convertirHijos = input("\n¿Quieres convertir el número de hijos de cadena a entero? (si/no): ").lower().strip()

if convertirHijos == "si":
    numeroHijos = int(numeroHijos)
    print("\nSe ha convertido el número de hijos a entero.")
if convertirHijos == "no":
    print("\nNo se ha convertido el número de hijos a entero.")
else:
    print("\nRespuesta no válida.")
    exit(1)

convertirAgno = input("\n¿Quieres convertir el año de nacimiento de cadena a entero? (si/no): ").lower().strip()

if convertirAgno == "si":
    agnoNacimiento = int(agnoNacimiento)
    print("\nSe ha convertido el año de nacimiento a entero.")

if convertirAgno == "no":
    print("\nNo se ha convertido el año de nacimiento a entero.")
else:
    print("\nRespuesta no válida.")
    exit(2)

# Terminar