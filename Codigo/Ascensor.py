class Ascensor:
    def __init__(self, numero, capacidad, plantasDisponibles, plantaActual, velocidad):
        self.numero = numero
        self.capacidad = capacidad
        self.plantasDisponibles = plantasDisponibles
        self.plantaActual = plantaActual
        self.personas = []
        self.velocidad = velocidad