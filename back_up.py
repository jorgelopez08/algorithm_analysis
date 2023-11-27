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

    def generate_schedule(self):
        for subject in self.subjects:
            for _ in range(2):  # For each subject, try scheduling two classes
                professor, classroom, time, day = self.find_available_slot(subject)
                if professor is not None:
                    self.schedule[subject] = {'Professor': professor, 'Classroom': classroom, 'Time': time, 'Day': day}
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
                    professor = self.professor_mapping[subject]
                    if self.is_slot_available(professor, classroom, time, day, subject):
                        return professor, classroom, time, day
        return None, None, None, None

    def is_slot_available(self, professor, classroom, time, day, subject):
        for existing_subject, details in self.schedule.items():
            # Allow professors to be scheduled for multiple classes at different times
            if details['Professor'] == professor and details['Time'] == time and self.days_difference(details['Day'],
                                                                                                      day) >= 1:
                continue
            # Ensure subjects are not scheduled on the same day and time
            if details['Day'] == day and details['Time'] == time and existing_subject != subject:
                continue
            # Allow multiple classes in different classrooms at the same time
            if details['Time'] == time and details['Day'] == day and details['Classroom'] != classroom:
                continue
        return True

    def days_difference(self, day1, day2):
        # Calculate the absolute difference between two days
        return abs(self.days.index(day1) - self.days.index(day2))

    def generate_random_professor_mapping(self):
        professor_mapping = {}

        for subject in self.subjects:
            professor_mapping[subject] = random.choice(self.professors)
        print(professor_mapping)
        return professor_mapping


# Example data
subjects = [f'Materia-{i}' for i in range(1, 61)]
professors = [f'Profe-{i}' for i in range(1, 21)]
classrooms = [f'Salon-{i}' for i in range(1, 26)]
time_slots = ['9:00-11:00', '11:00-1:00', '1:00-3:00', '3:00-5:00']
days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Create ScheduleGenerator instance
schedule_generator = ScheduleGenerator(subjects, professors, classrooms, time_slots, days_list)

# Generate schedule for the whole week
schedule_generator.generate_schedule()

# Print the generated schedule
days = {}
for subject, details in schedule_generator.schedule.items():
    if details["Day"] not in days:
        days[details["Day"]] = [details]
    else:
        days[details["Day"]].append(details)

    # print(f"{subject}: Professor {details['Professor']}, Classroom {details['Classroom']}, Time {details['Time']}, Day {details['Day']}")

days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
for day in days_list:
    print(day)
    for schedule in days[day]:
        print(f"{schedule['Classroom']} | {schedule['Professor']}\t | {schedule['Time']}")
    print()
