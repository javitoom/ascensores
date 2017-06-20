import time

import codigo.búsqueda_espacio_estados as búsqee
import codigo.costeOperadorAscensor as coste
import codigo.operadorAscensor as operador_ascensor
import codigo.problemaPlanificacionAscensor as probpl_ascensor
import codigo.relacionRigidaAscensor as relacion_rigida
import codigo.variableEstadosAscensor as variables


class ProblemaAscensores:
    """
    Creación del problema: Objetos, Variables de estado, Relaciones rígidos,
    Operadores
    """

    def __init__(self):

        num_ascensores = int(input('Número de ascensores: '))
        num_plantas = int(input('\nNúmero de plantas: '))
        num_personas = int(input('\nNúmero de personas: '))
        capacidad_max = int(input('\nCapacidad mayor: '))

        # ------ OBJETOS -----
        ascensores = ['A{}'.format(i) for i in range(num_ascensores)]
        personas = ['P{}'.format(i) for i in range(num_personas)]
        plantas = ['{}'.format(i) for i in range(num_plantas)]
        velocidad = ['l', 'r']
        capacidad = [str(i) for i in range(capacidad_max + 1)]

        # ------CREACION VARIABLES DE ESTADO-----
        posicion_ascensor = variables.PosicionAscensor(plantas, ascensores)
        posicion_persona = variables.PosicionPersona(ascensores, plantas,
                                                     personas)
        capacidad_ascensor = variables.CapacidadAscensor(ascensores, capacidad)
        velocidad_ascensor = variables.VelocidadAscensor(ascensores, velocidad)

        # -----COSTE OPERADOR--------
        coste_desplazar = coste.CosteOperadorAscensor()

        # -----CREACION DE RELACIONES RIGIDAS--------
        plantas_disponibles = relacion_rigida.PlantasDisponibles(
            num_ascensores)
        plantas_diferentes = relacion_rigida.PlantasDiferentes()
        capacidad_anterior = relacion_rigida.CapacidadAnterior()

        # --------CREACION DE OPERADORES----------
        # Desplazar ascensor:
        desplazar = operador_ascensor.Desplazar(posicion_ascensor,
                                                velocidad_ascensor,
                                                plantas_disponibles,
                                                plantas_diferentes,
                                                coste_desplazar, ascensores,
                                                plantas, velocidad)
        # Entrar en el ascensor:
        entrar = operador_ascensor.Entrar(posicion_persona, posicion_ascensor,
                                          capacidad_ascensor,
                                          capacidad_anterior, ascensores,
                                          plantas, personas, capacidad)
        # Salir del ascensor:
        salir = operador_ascensor.Salir(posicion_persona, posicion_ascensor,
                                        capacidad_ascensor,
                                        capacidad_anterior, ascensores,
                                        plantas, personas, capacidad)

        # INSTANCIACION DEL PROBLEMA
        problema_ascensores = probpl_ascensor.ProblemaPlanificacionAscensor(
            posicion_ascensor, posicion_persona, capacidad_ascensor,
            velocidad_ascensor, desplazar, entrar, salir,
            num_personas, num_ascensores, personas)

        while True:
            # ALGORITMOS DE BUSQUEDA
            opcion = int(input(
                '\nSeleccione algoritmo de búsqueda\n' +
                '{0: Búsqueda A*,\n'
                '1: BúsquedaEnAnchura,\n'
                '2: BúsquedaEnProfundidad,\n'
                '3: BúsquedaEnProfundidadAcotada,\n'
                '4: BúsquedaEnProfundidadIterativa,\n'
                '5: BúsquedaPrimeroElMejor,\n'
                '6: búsqee.BúsquedaÓptima}\n'
                'Cualquier otro parametro para salir: '))

            if opcion == 0:
                busqueda = búsqee.BúsquedaAEstrella(problema_ascensores.h,
                                                    detallado=True)
            elif opcion == 1:
                busqueda = búsqee.BúsquedaEnAnchura()
            elif opcion == 2:
                busqueda = búsqee.BúsquedaEnProfundidad()
            elif opcion == 3:
                busqueda = búsqee.BúsquedaEnProfundidadAcotada(cota=10)
            elif opcion == 4:
                busqueda = búsqee.BúsquedaEnProfundidadIterativa(cota_final=10)
            elif opcion == 5:
                busqueda = búsqee.BúsquedaPrimeroElMejor(problema_ascensores.h,
                                                         detallado=True)
            elif opcion == 6:
                busqueda = búsqee.BúsquedaÓptima()
            else:
                break

            tiempoActual = time.time()
            print(busqueda.buscar(
                problema_ascensores))  # Búsqueda de la solución
            print()
            duracion = time.time() - tiempoActual
            if (int(duracion) > 0):
                print(int(duracion), 'segundos')
            else:
                print(duracion, 'segundos')
