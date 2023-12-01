import json
import random



class ScheduleGenerator:
    def __init__(self, subjects, professors, classrooms, time_slots, days, max_subjects_per_professor=5):
        self.subjects = subjects
        self.professors = professors
        self.classrooms = classrooms
        self.time_slots = time_slots
        self.days = days
        self.max_subjects_per_professor = max_subjects_per_professor
        self.schedule = {}
        self.professor_mapping = self.generate_random_professor_mapping()

    def generate_schedule(self, num = None):
        for subject in self.subjects:
            for _ in range(2):  # For each subject, try scheduling two classes
                professor, classroom, time, day = self.find_available_slot(subject)
                if professor is not None:
                    # self.schedule[subject["Nombre"]] = {'Professor': professor, 'Classroom': classroom, 'Time': time, 'Day': day}
                    if day == 'Monday':
                        self.schedule[subject["Nombre"]] = {'Professor': professor, 'Classroom': classroom,
                                                            'Time': time, 'Day': ['Monday', 'Wednesday']}

                    elif day == 'Tuesday':
                        self.schedule[subject["Nombre"]] = {'Professor': professor, 'Classroom': classroom,
                                                            'Time': time, 'Day': ['Tuesday', 'Thursday']}
                    elif day == 'Wednesday':
                        self.schedule[subject["Nombre"]] = {'Professor': professor, 'Classroom': classroom,
                                                            'Time': time, 'Day': ['Wednesday', 'Friday']}
                else:
                    print(f"No available slot found for {subject}. Schedule incomplete.")
                    break

    def find_available_slot(self, subject):
        random.shuffle(self.days)
        random.shuffle(self.time_slots)
        random.shuffle(self.classrooms)
        for day in self.days:
            for time in self.time_slots:
                for classroom in self.classrooms:
                    professor = self.professor_mapping[subject["Nombre"]]
                    if self.is_slot_available(professor, classroom, time, day, subject["Nombre"]):
                        return professor, classroom, time, day
        return None, None, None, None

    def is_slot_available(self, professor, classroom, time, day, subject):
        for existing_subject, details in self.schedule.items():
            # Allow professors to be scheduled for multiple classes at different times
            if (details['Professor'] == professor
                    and details['Time'] == time
                    and self.days_difference(details['Day'][0], day) >= 1
                    and self.days_difference(details['Day'][1], day) >= 1):
                continue
            # Ensure subjects are not scheduled on the same day and time
            if details['Day'] == day and details['Time'] == time and existing_subject != subject:
                continue
            # Allow multiple classes in different classrooms at the same time
            if details['Time'] == time and details['Day'] == day and details['Classroom'] != classroom:
                continue
            # Block hours on two specified days for each class schedule
            if day in ['Monday', 'Wednesday'] and details['Day'] in ['Monday', 'Wednesday'] and details['Time'] == time:
                return False
            if day in ['Tuesday', 'Thursday'] and details['Day'] in ['Tuesday', 'Thursday'] and details['Time'] == time:
                return False
            if day in ['Wednesday', 'Friday'] and details['Day'] in ['Wednesday', 'Friday'] and details['Time'] == time:
                return False

            # Ensure two classes are not scheduled at the same time in the same classroom
            if details['Time'] == time and day in details['Day'] and classroom == details['Classroom']:
                return False
        return True

    def days_difference(self, day1, day2):
        # Calculate the absolute difference between two days
        return abs(self.days.index(day1) - self.days.index(day2))

    def generate_random_professor_mapping(self):
        professor_mapping = {}
        for subject in self.subjects:
            professor_mapping[subject["Nombre"]] = random.choice(subject["Profesores disponibles"])

        return professor_mapping

    def export_to_file(self):
        days = {}
        for subject, details in self.schedule.items():
            details["Subject"] = subject
            for i in range(0, len(details['Day'])):
                if details["Day"][i] not in days:
                    days[details["Day"][i]] = [details]
                else:
                    days[details["Day"][i]].append(details)

        clean_schedule = {}
        # days_list = ['Monday-Wednesday', 'Tuesday-Thursday', 'Wednesday-Friday']
        days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        schedule_view = ""
        for day in days_list:
            print(day)
            schedule_view = schedule_view + day + "\n"
            clean_schedule[day] = []
            for schedule in days[day]:
                clean_schedule[day].append({
                    "materia": schedule['Subject'],
                    "aula": f"{schedule['Classroom']['Edificio']}-{schedule['Classroom']['Numero']}",
                    "profesor": schedule['Professor'],
                    "hora": schedule['Time']
                })
                print(f"{schedule['Subject']}\t | "
                      f"{schedule['Classroom']['Edificio']}-{schedule['Classroom']['Numero']} "
                      f"| {schedule['Professor']} | {schedule['Time']}")
                schedule_view = schedule_view + (f"{schedule['Subject']}\t | "
                                f"{schedule['Classroom']['Edificio']}-{schedule['Classroom']['Numero']} "
                                f"| {schedule['Professor']} | {schedule['Time']}") + "\n"
            print()
            schedule_view = schedule_view + "\n"


        with open('schedule.json', 'w+') as f:
            f.write(json.dumps(clean_schedule, indent=2))
            f.close()

        return schedule_view


# Example data
# subjects = ['Subject{}'.format(i) for i in range(1, 61)]
# professors = ['Professor{}'.format(i) for i in range(1, 21)]
# classrooms = ['Classroom{}'.format(i) for i in range(1, 26)]
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

    # Generate schedule for the whole week
    schedule_generator.generate_schedule()

    # Print the generated schedule
    schedule_generator.export_to_file()

