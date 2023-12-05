from .university import Course, Room, University
from .timetable import TimeTable

class InputReader:
    def __init__(self, file_path):
        self.reading = {value: False for value in ['COURSES', 'ROOMS', 'CURRICULA', 'UNAVAILABILITY_CONSTRAINTS']}
        self.file_path = file_path

    def refresh(self):
        self.reading = {value: False for value in ['COURSES', 'ROOMS', 'CURRICULA', 'UNAVAILABILITY_CONSTRAINTS']}

    def read_input_file(self):
        courses = {}
        rooms = {}
        curricula = set()
        # Merge 2 dicts, requires python 3.9+ PEP 584 – Add Union Operators To dict
        header = {'Name': ''} | {key: -1 for key in ['Courses', 'Rooms', 'Days', 'Periods_per_day', 'Curricula', 'Constraints']}

        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip() # Remove \n
                lineKey = line.replace(' ', '').split(':') # Transform into ['Key', 'Value']
                if lineKey[0] in header.keys():
                    header.update({lineKey[0]: lineKey[1]})
                    continue
                elif lineKey[0] in self.reading.keys():
                    self.refresh()
                    self.reading.update({lineKey[0]: True})
                    continue
                elif lineKey[0] == 'END.':
                    break

                data = line.split()
                if self.reading['COURSES'] and data != []:
                    course = Course(data[0], data[1], int(data[2]), int(data[3]), int(data[4]))
                    courses[course.name] = course # Add course to courses dict
                elif self.reading['ROOMS'] and data != []:
                    room = Room(data[0], int(data[1]))
                    rooms[room.name] = room # Add room to rooms dict
                elif self.reading['CURRICULA'] and data != []:
                    for pair in zip(data[2:], data[3:]):
                        curricula.add(frozenset(pair)) # Set of imutable sets (frozenset)
                elif self.reading['UNAVAILABILITY_CONSTRAINTS'] and data != []:
                    courses[data[0]].add_unavailability_constraint(int(data[1]), int(data[2]))


        curricula_conflicts = {}
        for i in curricula:
            curricula_conflicts.update({_ : curricula_conflicts.get(_, 0) + 1 for _ in i})
        for i,j in curricula_conflicts.items():
            courses[i].curricula_conflicts = j
    

        university = University(
            header['Name'],
            courses,
            rooms,
            curricula
        )
        timetable = TimeTable(
            university,
            int(header['Rooms']), 
            int(header['Days']),
            int(header['Periods_per_day'])
        )
        return timetable
