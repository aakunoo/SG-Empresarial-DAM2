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
    def nombre(self, valor):
        self.nombreOculto = valor

    def mover(self):
        self.estado = "moviéndose"

    def parar(self):
        self.estado = "parado"

    @property
    def peso(self):
        return self.longitud * 3

    @classmethod
    def gasto(cls):
        pass#print(f"El gasto acumulado en vehículos es: {cls.total}")

    @staticmethod
    def informar():
        pass#print("La clase ‘vehiculo’ sirve para crear todo tipo de vehículos")

    def __gt__(self, vehiculo2):
        return self.longitud > vehiculo2.longitud


class vTerrestre(Vehiculo):
    def mover(self):
        self.estado = "rodando"

    def enganchar(self, incremento):
        self.longitud += incremento


class vAereo(Vehiculo):
    def __init__(self, nombreOculto, tieneMotor, estado, longitud, precio, altura):
        super().__init__(nombreOculto, tieneMotor, estado, longitud, precio)
        self.altura = altura

    def mover(self):
        self.estado = "volando"
        self.altura = 1000


class vAcuatico(Vehiculo):
    def mover(self):
        self.estado = "navegando"


terrestre1 = vTerrestre("camion", True, "parado", 10.50, 75000)

aereo1 = vAereo("Boing 747", True, "parado", 65.70, 100000000, 0)

acuatico1 = vAcuatico("barca", False, "parado", 3.90, 400)

#print("\n------------------------------------------------------------")
aereo1.mover()
#print(f"\nEl estado de 'aereo1' es: {aereo1.estado} y su altura es: {aereo1.altura} m")

acuatico1.mover()
#print(f"El estado de 'acuatico1' es: {acuatico1.estado}")

terrestre1.enganchar(9.15)
#print(f"La longitud de 'terrestre1' es: {terrestre1.longitud} m")
#print("\n------------------------------------------------------------")


class vHibrido1(vTerrestre, vAcuatico):
    pass

hibrido1 = vHibrido1("anfibio", True, "parado", 8.15, 125000)


class vHibrido2(vAereo, vAcuatico):
    def __init__(self, nombreOculto, tieneMotor, estado, longitud, precio, altura):
        super().__init__(nombreOculto, tieneMotor, estado, longitud, precio, altura)


hibrido2 = vHibrido2("hidroavion", True, "parado", 15.60, 500000, 0)

hibrido1.mover()
hibrido2.mover()

#print(f"\nEl estado de 'hibrido1' es: {hibrido1.estado}")
#print(f"El estado de 'hibrido2' es: {hibrido2.estado} y su altura es: {hibrido2.altura} m")

class Reproductor:
    def __init__(self, nombre):
        self.nombre = nombre

    def cantar(self):
        pass        #print("Mi carro, me lo robaron…")


class Turismo(vTerrestre):
    def __init__(self, nombreOculto, tieneMotor, estado, longitud, precio, radio):
        super().__init__(nombreOculto, tieneMotor, estado, longitud, precio)
        self.radio = radio


reproduce = Reproductor("MxOnda")

turismo1 = Turismo("Seat Ateca", True, "parado", 4.40, 23000, reproduce)

#print("\n------------------------------------------------------------")
turismo1.radio.cantar()
#print("------------------------------------------------------------")