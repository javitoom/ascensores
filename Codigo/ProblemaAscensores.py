from Codigo import Ascensor, Persona

class ProblemaAscensores:
    def __init__(self):
        self.ascensores = []
        self.personas = []

    def create(self):
        seguir = True
        while seguir:
            print("Creacion de ascensor")
            capacidad = input("Capacidad: ")
            plantasDisponibles = input("Plantas disponibles: ")
            plantaActual = input("Planta actual: ")
            listaPlantasDisponibles = set([int(x) for x in plantasDisponibles.strip().split(" ")])
            velocidad = input("Velocidad (rapido/lento): ") == "rapido"
            ascensor = Ascensor.Ascensor(capacidad,listaPlantasDisponibles,plantaActual, velocidad)
            self.ascensores.append(ascensor)
            seguir = input("¿Quieres crear mas ascensores?(y/n)") == "y"
        seguir = True
        while seguir:
            print("Creacion de persona")
            nombre = input("Nombre: ")
            plantaObjetivo = input("Plantas objetivo: ")
            plantaActual = input("Planta actual: ")
            persona = Persona.Persona(nombre,plantaObjetivo,plantaActual)
            self.personas.append(persona)
            seguir = input("¿Quieres crear mas personas?(y/n)") == "y"
