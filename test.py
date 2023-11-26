class ScheduleGenerator:
    def __init__(self, subjects, professors, classrooms, time_slots):
        self.subjects = subjects
        self.professors = professors
        self.classrooms = classrooms
        self.time_slots = time_slots
        self.schedule = {}

    def generate_schedule(self):
        for subject in self.subjects:
            slot = self.find_available_slot(subject)
            if slot is not None:
                professor, classroom, time = slot
                self.schedule[subject] = {'Professor': professor, 'Classroom': classroom, 'Time': time}
            else:
                print(f"No available slot found for {subject}. Schedule incomplete.")

    def find_available_slot(self, subject):
        for professor in self.professors:
            for time in self.time_slots:
                # Use all classrooms simultaneously
                for classroom in self.classrooms:
                    if self.is_slot_available(professor, classroom, time):
                        return professor, classroom, time
        return None

    def is_slot_available(self, professor, classroom, time):
        for existing_subject, details in self.schedule.items():
            # Allow professors to be scheduled for multiple classes at different times
            if details['Professor'] == professor and details['Time'] == time:
                return False
            # Allow multiple classes in different classrooms at the same time
            if details['Classroom'] == classroom and details['Time'] == time:
                return False
        return True


# Example data
subjects = ['Subject{}'.format(i) for i in range(1, 41)]
professors = ['Professor{}'.format(i) for i in range(1, 21)]
classrooms = ['Classroom{}'.format(i) for i in range(1, 26)]
time_slots = ['7:00-9:00', '9:00-11:00', '11:00-1:00', '1:00-3:00', '3:00-5:00', '5:00-7:00']

# Create ScheduleGenerator instance
schedule_generator = ScheduleGenerator(subjects, professors, classrooms, time_slots)

# Generate schedule for the whole day
schedule_generator.generate_schedule()

# Print the generated schedule
for subject, details in schedule_generator.schedule.items():
    print(f"{subject}: Professor {details['Professor']}, Classroom {details['Classroom']}, Time {details['Time']}")
