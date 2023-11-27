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
        self.grafo = self.grafo_bipartito(datos)

    #función para generar grafo bipartito
    def grafo_bipartito(self, datos):
        grafoCyP = nx.Graph()       # grafo bipartito de Cursos y profes
        grafoCyS =nx.Graph()        # grafo bipartito de cursos y secciones

        # Conjunto de Datos "Cursos"    
        cursos = datos["Datos"][2]['Curso']
        #se crea un nodo por cada elemento del conjunto
        for curso in cursos:
            id_curso = curso["ID"]
            grafoCyP.add_node(id_curso, bipartite=0, tipo="Curso")
            grafoCyS.add_node(id_curso, bipartite=0, tipo="Curso")

        # Conjunto de datos 'Profesores'
        profesores = datos["Datos"][0]["Profesor"]
        #se crea un nodo por cada elemento del conjunto
        for profesor in profesores:
            nombre_profesor = profesor['Nombre']
            grafoCyP.add_node(nombre_profesor, bipartite=1, tipo="Profesor")

        # Conjunto de datos "Secciones"
        secciones = datos["Datos"][3]["Seccion"]
        #se crea un nodo por cada elemento del conjunto
        for seccion in secciones:
            id_seccion= seccion["ID"]
            grafoCyS.add_node(id_seccion, bipartite=1, tipo="Seccion")

        # Agregar aristas al grafo 1 dependiendo cuales profesores estan disponibles para cada materia
        for curso in cursos:
            for profesor in profesores:
                nombre_profesor = profesor['Nombre']
                #si el profesor está disponible en ese curso, se crea una arista que los conecta
                if nombre_profesor in curso["Profesores disponibles"]:
                    id_curso = curso["ID"]
                    grafoCyP.add_edge(nombre_profesor, id_curso)

        # Agregar aristas al grafd 2 dependiemdp de cuáles curson hay en cada sección
        for seccion in secciones:
            for curso in cursos:
                nombre_curso = curso["Nombre"]
                #si la sección es compatible con el curso, se crea una arista que las conecta
                if nombre_curso.upper() in seccion["Curso"].upper():
                    id_curso = curso["ID"]
                    id_seccion = seccion["ID"]
                    grafoCyS.add_edge(id_seccion, id_curso)

        return grafoCyP, grafoCyS
    
    def mostrar_nodos(self):
        grafo, grafoS = self.grafo
        
        # esto colorea los nodos de tipo curso de color azul y los demás de rojo
        colores = ['blue' if grafo.nodes[nodo]['tipo'] == 'Curso' else 'red' for nodo in grafo.nodes()]        
        coloresS = ['green' if grafoS.nodes[nodo]['tipo'] == 'Curso' else 'yellow' for nodo in grafoS.nodes()]        
        
        #posiciona en pantalla el grafo de forma circular
        pos = nx.circular_layout(grafo)
        posS = nx.spring_layout(grafoS)
        
        # Crea un nuevo gráfico de subplots
        fig, axs = plt.subplots(1, 2)
        
        # Dibuja el primer grafo en el primer panel
        axs[0].set_title('Grafo de Cursos y profesores')
        nx.draw(grafo, pos, with_labels=True, font_weight='bold', node_color=colores, ax=axs[0])
        
        # Dibuja el segundo grafo en el segundo panel
        axs[1].set_title('Grafo de sección y cursos')
        nx.draw(grafoS, posS, with_labels=True, font_weight='bold', node_color=coloresS, ax=axs[1])
        
        # Muestra los gráficos en pantalla
        plt.show()

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
        grafo, grafoS = self.grafo
        # Obtener la lista de profesores del archivo JSON
        profesores = datos["Datos"][0]["Profesor"]
        nombre = str(input('Qué profesor buscas? -> '))

        for profesor in profesores:
            if nombre.upper() in profesor['Nombre'].upper():
                print(f"Profesor encontrado -> \nID: {profesor['id']}\nNombre: {profesor['Nombre']}\nHorarios disponibles: {profesor['Horarios Disponibles']}")
                print(f"Cursos que imparte -> \n")
                for curso in grafo.neighbors(profesor['Nombre']):
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
        grafo, grafoS = self.grafo
        cursos = datos['Datos'][2]['Curso']
        nombre = str(input('Escribe nombre del curso -> '))
        for curso in cursos:
            if nombre.upper() in curso['Nombre'].upper():
                print(f"Curso encontrado -> \nID: {curso['ID']} \nNombre: {curso['Nombre']}\n")
                print(f"Profesores que imparten la clase -> \n")
                for profesor in grafo.neighbors(curso['ID']):
                    print(f' - {profesor}')
                return
        print(f"No se encontró el curso con nombre '{nombre}'.\n")
        self.buscar_curso()
    
class Horario:
    #crear horarios para cada estudiante y profesor
    def __init__(self,datos):
        grafo = Bipartito(datos)
        self.grafoCyP, self.grafoCyS = grafo.grafo_bipartito(datos)

    def generar_horario(self):
        horarios_por_dia = {dia: [] for dia in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']}
        aulas = datos["Datos"][1]["Aula"]
        secciones = datos["Datos"][3]["Seccion"]

        for seccion in secciones:
            horario = seccion["Horario"]
            curso = self.grafoCyS.neighbors(seccion["ID"])

            for aula in aulas:
                for dia in horario.keys():  # Utilizamos las claves del diccionario de horario
                    horadisponible = aula["Horarios disponibles"].get(dia, [])
                    # Comprobar si alguna de las horas de la sección coincide con alguna de las horas disponibles en el aula
                    if horadisponible is not None:
                        if horario in horadisponible:
                            horarios_por_dia[dia].append({
                                "curso": curso,
                                "seccion": seccion["ID"],
                                "aula": aula["Numero"],
                                "horario": horario
                            })
                            horadisponible[dia].pop(horario)
                            break
        return horarios_por_dia

if __name__ == "__main__":
    # Carga tus datos desde el archivo JSON
    archivo_json = "datos2.json"
    with open(archivo_json, 'r', encoding='utf-8') as file:
        datos = json.load(file)

    grafo1 = Bipartito(datos)
    grafo1.mostrar_nodos()
    horario1 = Horario(datos)
    horarios_por_dia=horario1.generar_horario()

    # Imprimir horarios por día
    for dia, horarios in horarios_por_dia.items():
        print(f"Horarios para el día {dia}:")
        for horario in horarios:
            print(f"  Curso: {horario['curso']}, Sección: {horario['seccion']}, Aula: {horario['aula']}, Horario: {horario['horario']}")
