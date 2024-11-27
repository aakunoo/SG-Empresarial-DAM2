''' Hecho por Jerónimo Vicente. '''

print("\nEjercicio 1 - Estructuras Alternativas (if)", "\n-------------------------------------------\n")

year = input("Introduce un año: ")

if not year.isdigit():
    print("\nNecesitas introducir un año válido!", "\nSaliendo del programa...")

else:
    year = int(year)
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        print(f"El año {year} es bisiesto.")
    else:
        print(f"El año {year} no es bisiesto.")

    print("\nFin del programa.")
