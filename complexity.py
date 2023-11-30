import json
import big_o
from schedule_generator import ScheduleGenerator

if __name__ == "__main__":
    # Carga tus datos desde el archivo JSON
    archivo_json = "Datos.json"
    with open(archivo_json, 'r', encoding='utf-8') as file:
        datos = json.load(file)

    subjects = [curso for curso in (datos["Datos"][2]["Curso"])]
    professors = [profesor for profesor in (datos["Datos"][0]["Profesor"])]
    classrooms = [aula for aula in (datos["Datos"][1]["Aula"])]
    time_slots = ['9:00-11:00', '11:00-1:00', '1:00-3:00', '3:00-5:00']
    days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # Create ScheduleGenerator instance
    schedule_generator = ScheduleGenerator(subjects, professors, classrooms, time_slots, days_list)

    best, others = big_o.big_o(schedule_generator.generate_schedule, lambda n: big_o.datagen.integers(n, 0, 10000), n_repeats=100)
    print(best)
    print()
    for i in others:
        print(i)
