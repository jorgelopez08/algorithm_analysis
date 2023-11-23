import networkx as nx
import json
import matplotlib.pyplot as plt

#profesores
class Profesor:
    def __init__(self, id_profesor, nombre, horarios_disp):
        self.id = id_profesor
        self.nombre = nombre
        self.horarios_disp = horarios_disp

#Aulas
class Aula:
    def __init__(self, numero, edificio, lab, capacidad, horarios_disp):
        self.numero = numero
        self.edificio = edificio
        self.lab = lab
        self.capacidad = capacidad
        self.horarios_disp = horarios_disp

#cursos
class Curso:
    def __init__(self, id_curso, nombre, horas, lab, profe_disp, capacidad):
        self.id = id_curso
        self.nombre = nombre
        self.horas = horas
        self.lab = lab
        self.profe_disp = profe_disp
        self.capacidad = capacidad
    
#secciones
class Seccion:
    def __init__(self, id_seccion, profesor_asignado, horario, dias, curso):
        self.id = id_seccion
        self.profesor_asignado = profesor_asignado
        self.horario = horario
        self.dias = dias
        self.curso = curso

#Grafo bipartito
class Bipartito:
    def __init__(self,grafo):
        self.grafo = self.generar_grafo_bipartito(datos)

    #muestra todos los profesores disponibles
    def mostrarprofesores(self):
        if 'Profesor' in datos['Datos'][0]:
            profesores = datos["Datos"][0]["Profesor"]
            print('PROFESORES ->')
            for profesor in profesores:
                print(f" ID: {profesor['id']}\n Nombre: {profesor['Nombre']}\n Horarios disponibles: ")
                for horario in profesor['Horarios Disponibles']:
                    print(f'    - {horario}')
                print('')
        else: print("No hay información de profesores")
    
    #busca los profesores desde un diccionario
    def buscarProfe(self):
        # Obtener la lista de profesores del archivo JSON
        profesores = datos["Datos"][0]["Profesor"]
        nombre = str(input('Qué profesor buscas? -> '))

        for profesor in profesores:
            if nombre.upper() in profesor['Nombre'].upper():
                print(f"Profesor encontrado -> \nID: {profesor['id']}\nNombre: {profesor['Nombre']}\nHorarios disponibles: {profesor['Horarios Disponibles']}")
                print(f"Cursos que imparte -> \n")
                for curso in self.grafo.neighbors(profesor['Nombre']):
                    print(f' - {curso}')
                return
        print(f"No se encontró ningún profesor con el nombre '{nombre}'.")
        self.buscarProfe()

    #muestra los cursos disponibles
    def mostrarCursos(self):
        if 'Curso' in datos['Datos'][2]:
            cursos = datos['Datos'][2]['Curso']
            print('Cursos ->')
            for curso in cursos:
                print(f" ID: {curso['ID']}\n Nombre: {curso['Nombre']}\n Horas por semana -> {curso['Cantidad de horas']}\n Laboratorio: {curso['Uso de laboratorio']}")
                for profesor in curso['Profesores disponibles']:
                    print(f'    - {profesor}')
                print(f" Capacidad máxima de alumnos: {curso['Cantidad máxima de alumnos']}\n")
        else: print("No hay información de los cursos")

    #busca los cursos disponibles
    def buscar_curso(self):
        cursos = datos['Datos'][2]['Curso']
        nombre = str(input('Escribe nombre del curso -> '))
        for curso in cursos:
            if nombre.upper() in curso['Nombre'].upper():
                print(f"Curso encontrado -> \nID: {curso['ID']} \nNombre: {curso['Nombre']}\n")
                print(f"Profesores que imparten la clase -> \n")
                for profesor in self.grafo.neighbors(curso['ID']):
                    print(f' - {profesor}')
                return
        print(f"No se encontró el curso con nombre '{nombre}'.\n")
        self.buscar_curso()
    
    #función para generar grafo bipartito
    def generar_grafo_bipartito(self, datos):
        grafo = nx.Graph()
        
        #conjunto de datos 'Cursos'
        cursos = datos["Datos"][2]["Curso"]
        #se crea un nodo por cada elemento del conjunto
        for curso in cursos:
            id_curso = curso["ID"]
            grafo.add_node(id_curso, bipartite=0, tipo="Curso")

        # Conjunto de datos 'Profesores'
        profesores = datos["Datos"][0]["Profesor"]
        #se crea un nodo por cada elemento del conjunto
        for profesor in profesores:
            nombre_profesor = profesor['Nombre']
            grafo.add_node(nombre_profesor, bipartite=1, tipo="Profesor")

        # Agregar aristas al grafo dependiendo cuales profesores estan disponibles para cada materia
        for curso in cursos:
            for profesor in profesores:
                nombre_profesor = profesor['Nombre']
                #si el profesor está disponible en ese curso, se crea una arista que los conecta
                if nombre_profesor in curso["Profesores disponibles"]:
                    id_curso = curso["ID"]
                    grafo.add_edge(nombre_profesor, id_curso)
        return grafo

    #esta función imprime el grafo
    def mostrar_nodos(self):
        # esto colorea los nodos de tipo curso de color azul y los demás de rojo
        colores = ['blue' if self.grafo.nodes[nodo]['tipo'] == 'Curso' else 'red' for nodo in self.grafo.nodes()]        
        
        #posiciona en pantalla el grafo de forma circular
        pos = nx.circular_layout(self.grafo)
        nx.draw(self.grafo, pos, with_labels=True, font_weight='bold', node_color=colores)
        plt.show()

    def generar_horario(self):
        print("Horario ->")
        for nodo in self.grafo.nodes:
            if self.grafo.nodes[nodo]['tipo'] == 'Profesor':
                cursos_asignados = list(self.grafo.neighbors(nodo))
                if cursos_asignados:
                    print(f"\nProfesor: {nodo}")
                    for curso in cursos_asignados:
                        print(f"  Curso: {curso}")
        print("\nFin del horario")

if __name__ == "__main__":
    # Aquí deberías cargar tus datos desde el archivo JSON
    archivo_json = "Datos.json"
    with open(archivo_json, 'r', encoding='utf-8') as file:
        datos = json.load(file)

    grafo1 = Bipartito(datos)
    grafo1.generar_horario()
    grafo1.mostrar_nodos()
