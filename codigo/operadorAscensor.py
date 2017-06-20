import codigo.problema_planificación as probpl


# --------CREACION DE OPERADORES----------
# Desplazar ascensor:
class Desplazar(probpl.Operador):
    """
    Operador: desplaza los ascensores de una planta a otra
    """

    def __init__(self, posicion_ascensor, velocidad_ascensor,
                 plantas_disponibles, plantas_diferentes, coste_desplazar,
                 ascensores, plantas, velocidad):
        super().__init__(nombre='desplazar({a}, {v}, {pl1}, {pl2})',
                         precondiciones=[
                             posicion_ascensor({'{a}': '{pl1}'}),
                             velocidad_ascensor({'{a}': '{v}'})],
                         efectos=[
                             posicion_ascensor({'{a}': '{pl2}'})],
                         relaciones_rígidas=[
                             plantas_disponibles('{a}', '{pl1}'),
                             plantas_disponibles('{a}', '{pl2}'),
                             plantas_diferentes('{pl1}', '{pl2}')],
                         coste=coste_desplazar('{v}', '{pl1}',
                                               '{pl2}'),
                         a=ascensores,
                         pl1=plantas,
                         pl2=plantas,
                         v=velocidad
                         )


# Entrar en el ascensor:
class Entrar(probpl.Operador):
    """
        Operador: entrar un persona en un ascensor
    """

    def __init__(self, posicion_persona, posicion_ascensor, capacidad_ascensor,
                 capacidad_anterior, ascensores, plantas, personas, capacidad):
        super().__init__(nombre='entrar({p}, {a}, {pl}, {c1}, {c2})',
                         precondiciones=[
                             posicion_persona({'{p}': '{pl}'}),
                             posicion_ascensor({'{a}': '{pl}'}),
                             capacidad_ascensor({'{a}': '{c2}'})
                         ],

                         efectos=[posicion_persona({'{p}': '{a}'}),
                                  capacidad_ascensor({'{a}': '{c1}'})
                                  ],

                         relaciones_rígidas=capacidad_anterior('{c1}',
                                                               '{c2}'),
                         a=ascensores,
                         pl=plantas,
                         p=personas,
                         c1=capacidad,
                         c2=capacidad
                         )


# Salir del ascensor:
class Salir(probpl.Operador):
    """
        Operador: sacar a una persona de un ascensor
    """

    def __init__(self, posicion_persona, posicion_ascensor, capacidad_ascensor,
                 capacidad_anterior, ascensores, plantas, personas,
                 capacidad):
        super().__init__(nombre='salir({p}, {a}, {pl}, {c1}, {c2})',
                         precondiciones=[
                             posicion_persona({'{p}': '{a}'}),
                             posicion_ascensor({'{a}': '{pl}'}),
                             capacidad_ascensor({'{a}': '{c1}'})
                         ],
                         efectos=[posicion_persona({'{p}': '{pl}'}),
                                  capacidad_ascensor({'{a}': '{c2}'})
                                  ],
                         relaciones_rígidas=capacidad_anterior('{c1}',
                                                               '{c2}'),
                         a=ascensores,
                         pl=plantas,
                         p=personas,
                         c1=capacidad,
                         c2=capacidad
                         )
