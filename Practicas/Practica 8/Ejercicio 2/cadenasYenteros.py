''' By Jeronimo Vicente. '''

numeroHijos = input("Introduce el número de hijos: ")
agnoNacimiento = input("Introduce el año de nacimiento: ")


convertirHijos = input("\n¿Quieres convertir el número de hijos de cadena a entero? (si/no): ").lower().strip()

if convertirHijos == "si":
    numeroHijos = int(numeroHijos)
    print("\nSe ha convertido el número de hijos a entero.")
elif convertirHijos == "no":
    print("\nNo se ha convertido el número de hijos a entero.")
else:
    print("\nRespuesta no válida.")
    exit(1)

convertirAgno = input("\n¿Quieres convertir el año de nacimiento de cadena a entero? (si/no): ").lower().strip()

if convertirAgno == "si":
    agnoNacimiento = int(agnoNacimiento)
    print("\nSe ha convertido el año de nacimiento a entero.")

elif convertirAgno == "no":
    print("\nNo se ha convertido el año de nacimiento a entero.")
else:
    print("\nRespuesta no válida.")
    exit(2)

match convertirHijos, convertirAgno:
    case("no", "no"):
        numeroHijos = int(numeroHijos)
        agnoNacimiento = int(agnoNacimiento)
        print(f"El resultado de la multiplicación entre {numeroHijos} por {agnoNacimiento} es = " + str((numeroHijos * agnoNacimiento)))

    case("si", "no"):
        agnoNacimiento = int(agnoNacimiento)
        print(f"El resultado de la multiplicación entre {numeroHijos} por {agnoNacimiento} es = " + str((numeroHijos * agnoNacimiento)))

    case("no", "si"):
        numeroHijos = int(numeroHijos)
        print(f"El resultado de la multiplicación entre {numeroHijos} por {agnoNacimiento} es = " + str((numeroHijos * agnoNacimiento)))

    case("si", "si"):
        print(f"El resultado de la multiplicación entre {numeroHijos} por {agnoNacimiento} es = " + str((numeroHijos * agnoNacimiento)))

    case _:
        raise ValueError("Respuesta no válida.")
