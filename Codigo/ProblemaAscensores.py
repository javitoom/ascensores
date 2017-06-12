from jupyter_client.kernelspecapp import raw_input

from interfaces import Ascensor, Persona


class ProblemaAscensores:
    def __init__(self, numAscensores, numPersonas):
        self.numAscensores = numAscensores
        self.numPersonas = numPersonas
        self.costeTotal = 0
        self.ascensores = []
        self.personas = []
        for i in range(0,numAscensores):
            x = Ascensor.Ascensor(raw_input('Capacidad:'),raw_input('Plantas disponibles:'),raw_input('Planta actual:'))
            self.ascensores.append(x)
        for i in range(0,numPersonas):
            x = Persona.Persona(raw_input('Nombre:'),raw_input('Planta objetivo:'),raw_input('Planta actual:'))
            self.personas.append(x)
        