import codigo.problema_planificación as probpl


class PlantasDisponibles(probpl.RelaciónRígida):
    """
    Relación rígida: Plantas a las que puede acceder cada ascensor
    """

    def __init__(self, numAscensores):
        lista_plantas_disponibles = []
        for i in range(numAscensores):
            print("\nPlantas a las que puede acceder el ascensor A" + str(
                i) + ' Ej (0 1 2)')
            plas = set(input("Plantas: ").strip().split(" "))
            for pla in plas:
                relacion = ('A' + str(i), pla)
                lista_plantas_disponibles.append(relacion)
        super().__init__(
            lambda a, pl: (a, pl) in lista_plantas_disponibles)


class PlantasDiferentes(probpl.RelaciónRígida):
    """
    Relación rígida: Comprobar que dos plantas son diferentes
    """

    def __init__(self):
        super().__init__(lambda pl1, pl2: pl1 != pl2)


class CapacidadAnterior(probpl.RelaciónRígida):
    """
    Relación rígida: Comprobar que un capacidad es anterior a otra
    """

    def __init__(self):
        super().__init__(lambda n1, n2: int(n1) == int(n2) - 1)