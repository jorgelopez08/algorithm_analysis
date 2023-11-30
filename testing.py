import json

nombre_archivo = 'schedule.json'

#Lee el archivo JSON
def leer_json(nombre_archivo):
    #Abre el archivo JSON y carga su contenido
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

#Llama a la función para leer el archivo JSON
datos_leidos = leer_json(nombre_archivo)

#Verifica si se leyó correctamente y realiza la comprobación
if datos_leidos:
    print("Verificación de horario de clases:")
    for dia, clases in datos_leidos.items(): #El ciclo for pasa por cada día y por cada una de sus clases (iteración sobre esos elementos)
        aulas_horas = {}  #Diccionario para rastrear aulas y horas en el día actual
        print(f"\n{dia.capitalize()}:") #Se imprime el nombre del día
        for clase_info in clases:
            aula_actual = clase_info['aula']
            hora_actual = clase_info['hora']
            #Verificar si hay una coincidencia, si el aula ya está ocupada en la misma hora
            if (aula_actual, hora_actual) in aulas_horas:
                # Muestra una alerta si hay un choque de horario en el mismo aula y hora
                print(f"Alerta: En el aula {aula_actual} hay un choque de horario:")
                print(f"  - {clase_info['materia']} a las {hora_actual}") #Posición actual del diccionario
                print(f"  - {aulas_horas[(aula_actual, hora_actual)]['materia']} también a las {hora_actual}") #posicion actual del contenido del archivo
            else:
                #Registra la clase actual en el diccionario de aulas y horas
                aulas_horas[(aula_actual, hora_actual)] = clase_info
                #Imprime las clases con su aula y hora de forma normal
                print(f"Aula {aula_actual}: {clase_info['materia']} - {hora_actual}")