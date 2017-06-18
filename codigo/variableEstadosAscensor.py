import codigo.problema_planificación as probpl


class PosicionAscensor(probpl.VariableDeEstados):
    """
    Variable de estado: proporciona la posición del ascensor

    El rango son las plantas

    Los parametros los ascensores
    """

    def __init__(self, plantas, ascensores):
        super().__init__(nombre='posicion_ascensor({b})', rango=plantas,
                         b=ascensores)


class PosicionPersona(probpl.VariableDeEstados):
    """
    Variable de estado: proporciona la posición de la persona

    El rango son las plantas y los ascensores

    Los parametros las personas
    """

    def __init__(self, ascensores, plantas, personas):
        super().__init__(nombre='posicion_persona({b})',
                         rango=plantas + ascensores,
                         b=personas)


class CapacidadAscensor(probpl.VariableDeEstados):
    """
    Variable de estado: proporciona
     la capacidad del ascensor actualmente

     El rango son las capacidades

     Los parametros los ascensores
     """

    def __init__(self, ascensores, capacidad):
        super().__init__(
            nombre='capacidad_ascensor({b})',
            rango=capacidad,
            b=ascensores)


class VelocidadAscensor(probpl.VariableDeEstados):
    """
    Variable de estado: proporciona la velocidad del ascensor

    El rango es la velocidad

    Los parametros los ascensores
    """

    def __init__(self, ascensores, velocidad):
        super().__init__(
            nombre='velocidad_ascensor({b})',
            rango=velocidad, b=ascensores)
