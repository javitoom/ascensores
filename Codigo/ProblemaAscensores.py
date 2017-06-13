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
        plantaObjetivo = probpl.RelaciónRígida(lambda p: p.plantaObjetivo)

        plantasDisponibles = probpl.RelaciónRígida(lambda a: a.plantasDisponibles)

        velocidadAscensor = probpl.RelaciónRígida(lambda a: a.velocidad)

        capacidadAscensor = probpl.RelaciónRígida(lambda a: a.capacidad)

        #Variables de estado----------------------------------------------------
        posicionPersona=probpl.VariableDeEstados(nombre='posicion-persona({p})', rango=Plantas + Ascensores, p=Personas)
        posicionAscensor = probpl.VariableDeEstados(nombre='posicion-ascensor({a})', rango=Plantas, a=Ascensor)
        personasContenidas = probpl.VariableDeEstados(nombre='personas-contenidas({a})', rango=Personas, a=Ascensor)

        # Operadores-----------------------------------------------------

    