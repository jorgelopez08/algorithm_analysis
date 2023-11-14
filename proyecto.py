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
