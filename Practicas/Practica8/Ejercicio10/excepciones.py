# 1- Función para resolver ecuaciones de segundo grado
def resuelveEcuacion(a, b, c):
    try:
        # Comprobación inicial (Aserción)
        assert a <= 10

        # Calculando el discriminante
        discriminante = b ** 2 - 4 * a * c
        if discriminante < 0:
            raise ValueError("El discriminante es negativo, no hay soluciones reales.")

        # Resolviendo las raíces (sin usar la librería math)
        x1 = (-b + discriminante ** 0.5) / (2 * a)
        x2 = (-b - discriminante ** 0.5) / (2 * a)
        resultado = (x1, x2)
    except AssertionError:
        print("No se permiten valores mayores de 10 para ‘a’.")
        return -1
    except TypeError:
        print("Operación no permitida para ese tipo de datos.")
        return -1
    except Exception:
        print("Ocurrió algo y no se pudo realizar la operación.")
        return -1
    else:
        print("El programa ha podido calcular los resultados de la ecuación.")
        return resultado
    finally:
        print("Función resuelveEcuacion finalizada")


# 5- Pruebas con la función resuelveEcuacion
print("\nPrueba con parámetros (1, 4, -5):")
print(resuelveEcuacion(1, 4, -5))

print("\nPrueba con parámetros (1, -8, 16):")
print(resuelveEcuacion(1, -8, 16))

print("\nPrueba con parámetros (12, -4, 0):")
print(resuelveEcuacion(12, -4, 0))

print("\nPrueba con parámetros (5, '7', 9):")
print(resuelveEcuacion(5, "7", 9))


# 6- Clase personalizada noEsCadena
class noEsCadena(Exception):
    def __init__(self, variable):
        super().__init__(f"El dato '{variable}' no es de tipo cadena")


# 7- Función compruebaCadenas
def compruebaCadenas(lista):
    for elemento in lista:
        if not isinstance(elemento, str):  # Si no es una cadena
            raise noEsCadena(elemento)


# 8- Lista con cadenas y un valor no válido
cadenas = ["lunes", "martes", "miércoles", 4, "viernes", "sábado", "domingo"]

# 9- Prueba de la función compruebaCadenas
print("\nComprobación de la lista 'cadenas':")
try:
    compruebaCadenas(cadenas)
except noEsCadena as e:
    print(e)