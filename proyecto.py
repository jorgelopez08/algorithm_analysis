import networkx as nx
import json
import matplotlib.pyplot as plt

#profesores
class Profesor:
    def __init__(self, id_profesor, nombre, horarios_disp):
        self.id = id_profesor
        self.nombre = nombre
        self.horarios_disp = horarios_disp

#cursos
class Curso:
    def __init__(self, id_curso, nombre, horas, lab, profe_disp, max_alumnos):
        self.id = id_curso
        self.nombre = nombre
        self.horas = horas
        self.lab = lab
        self.profe_disp = profe_disp
        self.max_alumnos = max_alumnos

#aulas 
class Aula:
    def __init__(self, numero, edificio, lab, max_alumnos, horarios_disp):
        self.numero = numero
        self.edificio = edificio
        self.lab = lab
        self.max_alumnos = max_alumnos
        self.horarios_disp = horarios_disp

#sección de materia
class Seccion:
    def __init__(self, id_seccion, profesor_asignado, horario, dias, curso):
        self.id = id_seccion
        self.profesor_asignado = profesor_asignado
        self.horario = horario
        self.dias = dias
        self.curso = curso

# Cargar datos JSON
with open('Datos.json', 'r', encoding='utf-8') as file:
    datos = json.load(file)

#muestra todos los profesores disponibles
def mostrarprofesor():
        if 'Profesor' in datos['Datos'][0]:
            profesores = datos["Datos"][0]["Profesor"]
            if profesores:
                print('PROFESORES ->')
                for profesor in profesores:
                    print(f" ID: {profesor['id']},\n Nombre: {profesor['Nombre']}, \n Horarios disponibles: ")
                    for horario in profesor['Horarios Disponibles']:
                        print(f'    - {horario}')

                    
            else: return print("No hay profesores en los datos.")
        else: print("No hay información sobre profesores en el archivo.")
mostrarprofesor()

#función para generar grafo bipartito
def generar_grafo_bipartito(datos):
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

def nodos(grafo_bipartito):
    # esto colorea los nodos de tipo curso de color azul y los demás de rojo
    colores = ['blue' if grafo_bipartito.nodes[nodo]['tipo'] == 'Curso' else 'red' for nodo in grafo_bipartito.nodes()]

    # Dibujar el grafo coloreado
    pos = nx.spring_layout(grafo_bipartito)
    nx.draw(grafo_bipartito, pos, with_labels=True, font_weight='bold', node_color=colores, cmap=plt.cm.rainbow)
    plt.show()

# Generar el grafo bipartito
grafo_bipartito = generar_grafo_bipartito(datos)

#dibuja el grafo
nodos(grafo_bipartito)

"""
grafo={
    'A' : ['B','C'],
    'B' : ['D','E','F'], 
    'C' : ['G'],
    'D' : [],
    'E' : [],
    'F' : ['H'],
    'G' : ['I'],
    'H' : [],
    'I' : [],
}

def bfs(grafo,node):
    visited = []
    queueFIFO = []

    visited.append(node)
    queueFIFO.append(node)

    while queueFIFO:
        s= queueFIFO.pop(0)
        print(s, end=' ')

        for n in grafo[s]:
            if n not in visited:
                visited.append(n)
                queueFIFO.append(n)

bfs(grafo,'A')
"""
