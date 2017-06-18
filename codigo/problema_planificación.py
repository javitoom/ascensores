import copy
import itertools
import re

import codigo.problema_espacio_estados as probee


class VariableDeEstados:
    def __init__(self, nombre, rango, **dominios):
        self.nombre = nombre
        self.rango = rango
        self.parámetros = re.findall('{(.+?)}', nombre)
        if set(self.parámetros) != set(dominios.keys()):
            raise ValueError(
                'Alguno de los parámetros en {} no está definido'.format(
                    self.parámetros))
        else:
            self.dominios = [dominios[parámetro]
                             for parámetro in self.parámetros]

    def __str__(self):
        return (self.nombre + '\n' +
                '\n'.join('{} = {}'.format(parámetro, dominio)
                          for parámetro, dominio in
                          zip(self.parámetros, self.dominios)) +
                '\nRango: ' + str(self.rango))

    def _es_parámetro(self, expresión):
        return re.fullmatch('^\{[^{}]+?\}$', expresión)

    def _es_negativo(self, valor):
        return valor[0] == '-'

    def __call__(self, asignaciones):
        if not isinstance(asignaciones, dict):
            asignaciones = {(): asignaciones}
        asignaciones = {
            valores if isinstance(valores, tuple) else (valores,): valor
            for valores, valor in asignaciones.items()}
        variables_estados = {}
        for valores_paráms, valor in asignaciones.items():
            for valor_parám, dominio in zip(valores_paráms, self.dominios):
                if (not self._es_parámetro(valor_parám) and
                    not valor_parám in dominio):
                    raise ValueError('Asignación {} incorrecta'.format(
                        valores_paráms))
            if not self._es_parámetro(valor):
                valor_sin_signo = (valor[1:] if self._es_negativo(valor)
                                   else valor)
                if valor_sin_signo not in self.rango:
                    raise ValueError('Valor {} fuera de rango'.format(
                        valor_sin_signo))
            nombre = self.nombre.format(
                **dict(zip(self.parámetros, valores_paráms)))
            variables_estados.update({nombre: valor})
        return variables_estados


class Estado:
    def __init__(self, *asignaciones):
        self.asignaciones = {}
        for asignación in asignaciones:
            self.asignaciones.update(asignación)

    def __eq__(self, otro):
        return self.asignaciones == otro.asignaciones

    def __str__(self):
        return '\n'.join(
            '{} = {}'.format(variable_estados, valor)
            for variable_estados, valor in sorted(self.asignaciones.items()))

    def _es_negativo(self, valor):
        return valor[0] == '-'

    def satisface(self, variable_estados, valor):
        valor_estado = self.asignaciones[variable_estados]
        if self._es_negativo(valor):
            return valor_estado != valor[1:]
        else:
            return valor_estado == valor


class AcciónPlanificación(probee.Acción):
    def __init__(self, nombre,
                 precondiciones=None, efectos=None, coste=1):
        self.nombre = nombre
        if precondiciones is None:
            precondiciones = []
        if not isinstance(precondiciones, list):
            precondiciones = [precondiciones]
        self.precondiciones = {}
        for precondición in precondiciones:
            self.precondiciones.update(precondición)
        if efectos is None:
            efectos = []
        if not isinstance(efectos, list):
            efectos = [efectos]
        self.efectos = {}
        for efecto in efectos:
            self.efectos.update(efecto)
        self.coste = coste

    def es_aplicable(self, estado):
        return all(estado.satisface(variable_estados, valor)
                   for variable_estados, valor in self.precondiciones.items())

    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        nuevo_estado.asignaciones.update(self.efectos)
        return nuevo_estado

    def coste_de_aplicar(self, estado):
        return self.coste

    def __str__(self):
        return (self.nombre + '\nPrecondiciones:\n' +
                '\n'.join('{} = {}'.format(variable_estados, valor)
                          for variable_estados, valor
                          in sorted(self.precondiciones.items())) +
                '\nEfectos:\n' +
                '\n'.join('{} <- {}'.format(variable_estados, valor)
                          for variable_estados, valor
                          in sorted(self.efectos.items())) +
                '\nCoste: ' + str(self.coste))


class RelaciónRígida:
    def __init__(self, predicado=lambda *argumentos: True):
        self.predicado = predicado

    def verifica(self, asignación):
        return self.predicado(*(argumento.format(**asignación)
                                for argumento in self.argumentos))

    def __call__(self, *argumentos):
        relación_rígida = copy.deepcopy(self)
        relación_rígida.argumentos = argumentos
        return relación_rígida


class CosteOperador:
    def __init__(self, coste=None):
        if coste is None:
            coste = 1
        if isinstance(coste, int):
            def función_coste(*argumentos):
                return coste
            self.función_coste = función_coste
        else:
            self.función_coste = coste

    def coste(self, asignación):
        return self.función_coste(*(argumento.format(**asignación)
                                    for argumento in self.argumentos))

    def __call__(self, *argumentos):
        coste_operador = copy.deepcopy(self)
        coste_operador.argumentos = argumentos
        return coste_operador


class Operador:
    def __init__(self, nombre, precondiciones=None, efectos=None,
                 relaciones_rígidas=None, coste=None, **variables):
        self.nombre = nombre
        if precondiciones is None:
            precondiciones = []
        if not isinstance(precondiciones, list):
            precondiciones = [precondiciones]
        self.precondiciones = precondiciones
        if efectos is None:
            efectos = []
        if not isinstance(efectos, list):
            efectos = [efectos]
        self.efectos = efectos
        if relaciones_rígidas is None:
            relaciones_rígidas = []
        if not isinstance(relaciones_rígidas, list):
            relaciones_rígidas = [relaciones_rígidas]
        self.relaciones_rígidas = relaciones_rígidas
        if coste is None or isinstance(coste, int):
            coste = CosteOperador(coste)()
        self.coste_operador = coste
        self.variables = variables

    def _procesar(self, componente, asignación):
        return {variable_estados.format(**asignación):
                valor.format(**asignación)
                for variable_estados, valor in componente.items()}

    def obtener_acción(self, asignación):
        nombre = self.nombre.format(**asignación)
        precondiciones = [self._procesar(precondición, asignación)
                          for precondición in self.precondiciones]
        efectos = [self._procesar(efecto, asignación)
                   for efecto in self.efectos]
        coste = self.coste_operador.coste(asignación)
        return AcciónPlanificación(nombre, precondiciones, efectos, coste)

    def verifica_relaciones_rígidas(self, asignación):
        return all(relación_rígida.verifica(asignación)
                   for relación_rígida in self.relaciones_rígidas)

    def obtener_acciones(self):
        nombres_variables = self.variables.keys()
        valores_variables = self.variables.values()
        producto_valores = itertools.product(*valores_variables)
        asignaciones = (dict(zip(nombres_variables, valores))
                        for valores in producto_valores)
        return [self.obtener_acción(asignación) for asignación in asignaciones
                if self.verifica_relaciones_rígidas(asignación)]

    def __str__(self):
        acciones = self.obtener_acciones()
        return ('Operador: ' + self.nombre +
                '\nACCIONES GENERADAS:\n' +
                '\n\n'.join(str(acción) for acción in acciones))


class ProblemaPlanificación(probee.ProblemaEspacioEstados):
    def __init__(self, variables_estados, operadores,
                 estado_inicial, objetivos):
        if not isinstance(variables_estados, list):
            variables_estados = [variables_estados]
        nombres_estado_inicial = set(estado_inicial.asignaciones.keys())
        for variable_estados in variables_estados:
            nombres = set(
                variable_estados.nombre.format(
                    **dict(zip(variable_estados.parámetros, valores)))
                for valores in itertools.product(*variable_estados.dominios))
            if not nombres.issubset(nombres_estado_inicial):
                raise ValueError('El estado inicial no está completo')
        if not isinstance(operadores, list):
            operadores = [operadores]
        if not isinstance(objetivos, list):
            objetivos = [objetivos]
        self.objetivos = {}
        for objetivo in objetivos:
            self.objetivos.update(objetivo)
        acciones = sum(([operador] if isinstance(operador, AcciónPlanificación)
                       else operador.obtener_acciones()
                       for operador in operadores), [])
        super().__init__(acciones, estado_inicial)

    def es_estado_final(self, estado):
        return all(estado.satisface(variable_estados, valor)
                   for variable_estados, valor in self.objetivos.items())
