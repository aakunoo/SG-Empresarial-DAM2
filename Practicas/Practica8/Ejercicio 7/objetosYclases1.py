''' By Jerónimo Vicente '''

class Vehiculo:
    total = 0

    def __init__(self, nombreOculto, tieneMotor, estado, longitud, precio):
        self.nombreOculto = nombreOculto
        self.tieneMotor = tieneMotor
        self.estado = estado
        self.longitud = longitud
        self.__precio = precio

        Vehiculo.total += precio

    @property
    def nombre(self):
        return self.nombreOculto

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.nombreOculto = nuevo_nombre

    def mover(self):
        self.estado = "moviéndose"

    def parar(self):
        self.estado = "parado"

    @property
    def peso(self):
        return self.longitud * 3

    @classmethod
    def gasto(cls): # cls es la convención para referirse a la clase.
        print(f"El gasto acumulado en vehículos es: {cls.total}")

    @staticmethod
    def informar():
        print("La clase 'vehiculo' sirve para crear todo tipo de vehículos")

    def __gt__(self, vehiculo2):
        return self.longitud > vehiculo2.longitud

v1 = Vehiculo("coche", True, "parado", 3.79, 19000)
v2 = Vehiculo("bicicleta", False, "parado", 1.40, 120)
v3 = Vehiculo("barco", True, "parado", 8.55, 67800)

print("\n------------------------------------------------------------")
print(f"\nNombre del vehiculo 1: {v1.nombre} \nLongitud del vehiculo 2: {v2.longitud} \nPeso del vehiculo 3: {v3.peso}") #,v1.precio no deja porque precio es privado.")

print("\n------------------------------------------------------------")
v1.mover()
v2.mover()
print(f"\nEstado del vehiculo 2: {v2.estado}")

print("\n------------------------------------------------------------")
v1.nombre = "turismo"
print(f"\nNombre del vehiculo 1 actualizado: {v1.nombre}")

print("\n------------------------------------------------------------")
v3.informar()
v2.gasto()


v1.parar()
print("\n------------------------------------------------------------")
print(f"\nEl {v1.nombre} esta: {v1.estado}")
print("\n------------------------------------------------------------")

print(f"\n¿{v1.nombre} es más largo que {v2.nombre}?: {v1 > v2}")
print(f"¿{v2.nombre} es más largo que {v3.nombre}?: {v2 > v3}")
print("\n------------------------------------------------------------")
