from Codigo import Ascensor, Persona
import Codigo.problema_planificación as probpl

class ProblemaAscensores:
    def __init__(self, numPlantas):
        self.ascensores = []
        self.personas = []
        self.numPlantas = numPlantas

    def create(self):
        seguir = True
        i = 1
        while seguir:
            print("Creacion de ascensor "+i)
            capacidad = input("Capacidad: ")
            plantasDisponibles = input("Plantas disponibles: ")
            plantaActual = input("Planta actual: ")
            listaPlantasDisponibles = set([int(x) for x in plantasDisponibles.strip().split(" ")])
            velocidad = input("Velocidad (rapido/lento): ") == "rapido"
            ascensor = Ascensor.Ascensor(i, capacidad,listaPlantasDisponibles,plantaActual, velocidad)
            self.ascensores.append(ascensor)
            seguir = input("¿Quieres crear mas ascensores?(y/n)") == "y"
            i=i+1
        seguir = True
        while seguir:
            print("Creacion de persona")
            nombre = input("Nombre: ")
            plantaObjetivo = input("Plantas objetivo: ")
            plantaActual = input("Planta actual: ")
            persona = Persona.Persona(nombre,plantaObjetivo,plantaActual)
            self.personas.append(persona)
            seguir = input("¿Quieres crear mas personas?(y/n)") == "y"

        # Objetos----------------------------------------------------
        Velocidad = ['V{}'.format(i) for i in range(2)]
        Plantas = ['Pl[{}'.format(i) for i in range(self.numPlantas)]
        Capacidad = set([x.capacidad for x in self.ascensores])
        Personas = ['P{}'.format(i) for i in range(len(self.personas))]
        Ascensores = ['A{}'.format(i) for i in range(len(self.ascensores))]
        Booleanos = ['si', 'no']

        print('Velocidad:', Velocidad)
        print('Plantas:', Plantas)
        print('Capacidad:', Capacidad)
        print('Personas:', Personas)
        print('Ascensores:', Ascensores)
        print('Booleanos:', Booleanos)

        #Relaciones rigidas-----------------------------------------------------
        planta_Objetivo = probpl.RelaciónRígida(lambda p ,pl: pl in p.plantaObjetivo)

        plantas_Disponibles = probpl.RelaciónRígida(lambda a, pl: pl in a.plantasDisponibles)

        velocidad_Ascensor = probpl.RelaciónRígida(lambda a: a.velocidad)

        capacidad_Ascensor = probpl.RelaciónRígida(lambda a: a.capacidad)

        #Variables de estado----------------------------------------------------
        posicion_Persona = probpl.VariableDeEstados(nombre='posicion-persona({p})', rango=Plantas + Ascensores,
                                                   p=Personas)
        posicion_Ascensor = probpl.VariableDeEstados(nombre='posicion-ascensor({a})', rango=Plantas, a=Ascensores)

        personas_Contenidas = probpl.VariableDeEstados(nombre='personas-contenidas({a})', rango=Personas, a=Ascensores)

        capacidad_Ascensor = probpl.VariableDeEstados(nombre='capacidad_de({a})', rango= Capacidad, a=Ascensores)

        # Operadores-----------------------------------------------------
        # El ascensor se desplaza de planta
        desplazar = probpl.Operador(nombre='desplazar({a},{pl})', efectos=[posicion_Ascensor({'{a}': '{pl}'})]
                                    , relaciones_rígidas= plantas_Disponibles('{a}', '{pl}'),
                                    a=Ascensores,
                                    pl=Plantas
                                    )
        # La persona se baja del ascensor
        entrar = probpl.Operador(nombre='entrar({p},{a})', precondiciones=[ personas_Contenidas({'{a}':'{-p}'}),
                                                                            posicion_Ascensor({'{a}':'{pl}'}),
                                                                            posicion_Persona({'{p}':'{pl}'}),
                                                                    capacidad_Ascensor({'{a}': Ascensores.capacidad})],
                                    efectos=[posicion_Persona({'{p}': '{a}'}),
                                             capacidad_Ascensor({'{a}' : ascensor.capacidad + 1})],
                                    a=Ascensores,
                                    pl=Plantas,
                                    p= Personas
                                 )
        # La persona sale del ascensor
        salir = probpl.Operador(nombre='salir({p},{a})', precondiciones=[personas_Contenidas({'{a}': '{p}'}),
                                                                         posicion_Ascensor({'{a}': '{pl}'})],
                                 efectos=[posicion_Persona({'{p}': '{pl}'}),
                                          capacidad_Ascensor({'{a}': ascensor.capacidad - 1})],
          #Solo si se baja en la planta objetivo------   relaciones_rígidas= plantaObjetivo('{p)','{pl}'),
                                 a=Ascensores,
                                 pl=Plantas,
                                 p=Personas
                                 )