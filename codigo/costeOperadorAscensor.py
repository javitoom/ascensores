import codigo.problema_planificación as probpl


class CosteOperadorAscensor(probpl.CosteOperador):
    """
        Coste: calcula el coste en función de la rapidez del
        ascensor y el numero de plantas que se desplaza
    """
    def __init__(self):
        super().__init__(
            lambda v, pl1, pl2: (6 + abs(int(pl2) - int(pl1))) if (
                v == 'l') else (2 + (3 * abs(int(pl2) - int(pl1)))))
