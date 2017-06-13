class Ascensor:
    def __init__(self, capacidad, plantasDisponibles, plantaActual, velocidad):
        self.capacidad = capacidad
        self.plantasDisponibles = plantasDisponibles
        self.plantaActual = plantaActual
        self.personas = []
        self.velocidad = velocidad