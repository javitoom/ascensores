import time

import codigo.búsqueda_espacio_estados as búsqee
import codigo.costeOperadorAscensor as coste
import codigo.operadorAscensor as operador_ascensor
import codigo.problemaPlanificacionAscensor as probpl_ascensor
import codigo.relacionRigidaAscensor as relacion_rigida
import codigo.variableEstadosAscensor as variables


class ProblemaAscensores:
    def __init__(self):

        num_ascensores = int(input('Numero de ascensores: '))
        num_plantas = int(input('\nNumero de plantas: '))
        num_personas = int(input('\nNumero de personas: '))
        capacidad_max = int(input('\nCapacidad maxima: '))

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
        capacidad_siguiente = relacion_rigida.CapacidadSiguente()

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
                                        capacidad_siguiente, ascensores,
                                        plantas, personas, capacidad)

        # INSTANCIACION DEL PROBLEMA
        problema_ascensores = probpl_ascensor.ProblemaPlanificacionAscensor(
            posicion_ascensor, posicion_persona, capacidad_ascensor,
            velocidad_ascensor, desplazar, entrar, salir,
            num_personas, num_ascensores, personas)

        # ALGORITMO DE BUSQUEDA
        options = {0: búsqee.BúsquedaAEstrella(problema_ascensores.h),
                   1: búsqee.BúsquedaEnAnchura(),
                   2: búsqee.BúsquedaEnProfundidad(),
                   3: búsqee.BúsquedaEnProfundidadAcotada(cota=10),
                   4: búsqee.BúsquedaEnProfundidadIterativa(cota_final=10),
                   5: búsqee.BúsquedaPrimeroElMejor(problema_ascensores.h,
                                                    detallado=True),
                   6: búsqee.BúsquedaÓptima()}

        busqueda = options[int(input(
            '\nSeleccione algoritmo de busqueda\n' +
            '{0: Búsqueda A*,\n'
            '1: BúsquedaEnAnchura,\n'
            '2: BúsquedaEnProfundidad,\n'
            '3: BúsquedaEnProfundidadAcotada,\n'
            '4: BúsquedaEnProfundidadIterativa,\n'
            '5: BúsquedaPrimeroElMejor,\n'
            '6: búsqee.BúsquedaÓptima}:\n'))]

        tiempoActual = time.time()
        print(busqueda.buscar(problema_ascensores))  # Búsqueda de la solución
        print()
        duracion = time.time() - tiempoActual
        if (int(duracion) > 0):
            print(int(duracion), 'segundos')
        else:
            print(duracion, 'segundos')
