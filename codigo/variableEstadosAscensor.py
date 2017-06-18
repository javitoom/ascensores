import codigo.problema_planificación as probpl


class PosicionAscensor(probpl.VariableDeEstados):
    def __init__(self, plantas, ascensores):
        super().__init__(nombre='posicion_ascensor({b})', rango=plantas,
                         b=ascensores)


class PosicionPersona(probpl.VariableDeEstados):
    def __init__(self, ascensores, plantas, personas):
        super().__init__(nombre='posicion_persona({b})',
                         rango=plantas + ascensores,
                         b=personas)


class CapacidadAscensor(probpl.VariableDeEstados):
    def __init__(self, ascensores, capacidad):
        super().__init__(
            nombre='capacidad_ascensor({b})',
            rango=capacidad,
            b=ascensores)


class PersonasAscensor(probpl.VariableDeEstados):
    def __init__(self, ascensores, personas):
        super().__init__(
            nombre='personas_ascensor({b})',
            rango=personas + ['ninguna'],
            b=ascensores)


class VelocidadAscensor(probpl.VariableDeEstados):
    def __init__(self, ascensores, velocidad):
        super().__init__(
            nombre='velocidad_ascensor({b})',
            rango=velocidad, b=ascensores)
