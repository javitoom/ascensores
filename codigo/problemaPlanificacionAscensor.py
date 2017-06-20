import codigo.problema_planificación as probpl


class ProblemaPlanificacionAscensor(probpl.ProblemaPlanificación):
    """
    Problema de planificación ascensores
    """

    def __init__(self, posicion_ascensor, posicion_persona, capacidad_ascensor,
                 velocidad_ascensor, desplazar, entrar,
                 salir, numPersonas, numAscensores, personas):

        self.personas = personas

        lista_posicion_ascensor = {}
        lista_capacidad_ascensor = {}
        lista_velocidad_ascensor = {}
        for i in range(numAscensores):
            pla = input(
                "\nPlanta inicial del ascensor A" + str(i) + ": ").split()
            lista_posicion_ascensor['A' + str(i)] = pla[0]
            pla = input(
                "\nCapacidad inicial del ascensor A" + str(i) + ": ").split()
            lista_capacidad_ascensor['A' + str(i)] = pla[0]
            pla = input(
                "\nVelocidad del ascensor A" + str(
                    i) + "(l/r): ").split()
            lista_velocidad_ascensor['A' + str(i)] = pla[0]

        lista_posicion_persona = {}
        lista_posicion_persona_objetivo = {}
        for i in range(numPersonas):
            pla = input(
                "\nPlanta inicial de la persona P" + str(i) + ": ").split()
            lista_posicion_persona['P' + str(i)] = pla[0]
            pla = input(
                "\nPlanta objetivo de la persona P" + str(i) + ": ").split()
            lista_posicion_persona_objetivo['P' + str(i)] = pla[0]

        super().__init__(
            variables_estados=[posicion_ascensor,
                               posicion_persona,
                               capacidad_ascensor],
            operadores=[desplazar,
                        entrar,
                        salir],
            estado_inicial=probpl.Estado(
                posicion_ascensor(lista_posicion_ascensor),
                posicion_persona(lista_posicion_persona),
                capacidad_ascensor(lista_capacidad_ascensor),
                velocidad_ascensor(lista_velocidad_ascensor)),
            objetivos=[posicion_persona(lista_posicion_persona_objetivo)]
        )

    def h(self, nodo):  # h(nodo)
        """
        Funcion para calcular la heuristica de cada nodo

        Dos heuristicas definidas:

        1.Numero de personas sin llegar a su objetivo

        2.Suma de las distancias de todas las personas a su objetivo

        :param nodo:
        :return heuristica:
        """
        heuristica = 0
        for persona in self.personas:
            if "A" in (nodo.estado.asignaciones[
                                   'posicion_persona(' + persona + ')']):
                heuristica = heuristica + abs(int(
                    nodo.estado.asignaciones[
                        'posicion_ascensor(' + nodo.estado.asignaciones[
                            'posicion_persona(' + persona + ')'] + ')']) - int(
                    self.objetivos[
                        'posicion_persona(' + persona + ')']))
            else:

                heuristica = heuristica + abs(int(
                    nodo.estado.asignaciones[
                        'posicion_persona(' + persona + ')']) - int(
                    self.objetivos[
                        'posicion_persona(' + persona + ')']))

        return pow(heuristica, heuristica)

        # heuristica = 0
        # for persona in self.personas:
        #     if "A" in (nodo.estado.asignaciones[
        #                            'posicion_persona(' + persona + ')']):
        #         if (nodo.estado.asignaciones['posicion_ascensor(' +
        #             nodo.estado.asignaciones[
        #                         'posicion_persona(' + persona + ')'] + ')'] ==
        #                 self.objetivos['posicion_persona(' + persona + ')']):
        #             heuristica += 0
        #         else:
        #             heuristica += 1
        #     else:
        #
        #         if (nodo.estado.asignaciones[
        #                         'posicion_persona(' + persona + ')'] ==
        #                 self.objetivos[
        #                             'posicion_persona(' + persona + ')']):
        #             heuristica += 0
        #         else:
        #             heuristica += 1
        #
        # return heuristica