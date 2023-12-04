from pprint import pformat # Use this to print objects in a pretty way

class Course:
    def __init__(self, name, professor, lectures, min_days, students):
        self.name = name
        self.professor = professor
        self.lectures = lectures
        self.min_days = min_days
        self.students = students
        self.uconstraints = set() # Set of tuple (day, period) representing unavailability constraints

    def __str__(self):
        return pformat(vars(self), indent=4)

    def __eq__(self, other):
        return self.name == other.name and self.professor == other.professor

    def add_unavailability_constraint(self, day, period):
        self.uconstraints.add((day, period))

    def is_available(self, day, period):
        return (day, period) not in self.uconstraints

    def conflict_score(self):
        pass

class Room:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __str__(self):
        return pformat(vars(self), indent=4)

    def __eq__(self, other):
        return self.name == other.name

class TimeTable:
    def __init__(self,university,rooms,days,periods_per_day):
        self.rooms: int = rooms
        self.days: int = days
        self.periods_per_day: int = periods_per_day
        self.university: University = university
        #tt[room][day][period] with list comprehension
        self.tt = [[['' for _ in range(periods_per_day)] for _ in range(days)] for _ in range(rooms)]

    def __str__(self):
        return pformat(vars(self), indent=4)

    def allocate_course(self, course, day, period, room):
        if self.tt[room][day][period] == '':
            self.tt[room][day][period] = course.name

    # – H1-Aulas: Todas as aulas de uma disciplina devem ser alocadas, e em períodos
    # diferentes. Uma violação ocorre se uma aula não é alocada, ou se duas aulas da
    # mesma disciplina são alocadas no mesmo período
    def h1(self,course,day,room,period):
        pass
   
    # H2-Ocupação de Sala: Duas aulas não podem ser alocadas em uma mesma sala
    # e no mesmo período. Cada aula extra em uma mesma sala e no mesmo período
    # conta como uma violação.
    def h2(self,course,room,period):
        return any ({self.tt[room][d][period],course} in self.university.curricula for d in range(self.days))

    # H3-Conflitos: Aulas de disciplinas de um mesmo currículo, ou ministradas
    # pelo mesmo professor devem ser alocadas em períodos diferentes. Duas aulas
    # conflitantes no mesmo período representa uma violação
    def h3(self,course,day,period):
        # If any of the courses in the curriculum is already allocated in the same period, return True
        return any({self.tt[r][day][period],course} in self.university.curricula for r in range(self.rooms))

    # – H4-Indisponibilidade: Se o professor de uma disciplina não está disponível para
    # lecioná-la em determinado período, nenhuma aula dessa disciplina pode ser
    # alocada nesse período. Cada aula alocada em um período não disponível para a
    # disciplina conta como uma violação.
    def h4(self):
        # Implement logic to calculate h4
        pass

    def conflicts(self, course, day, period, room):
        return\
            self.tt[room][day][period] != '' and\
            self.h2(course,room,period) and\
            self.h3(course,day,period)

    # Soft constraints
    # The problem includes the following soft constraints:
    # – Room Capacity For each lecture, the number of students that attend the
    # course must be less than or equal to the number of seats in all the rooms
    # that host its lectures. Each student above the capacity counts as 1 point of
    # penalty.
    # – Minimum Working Days The lectures of each course must be spread into
    # the given minimum number of days. Each day below the minimum counts
    # as 5 points of penalty.
    # – Curriculum Compactness Lectures belonging to a curriculum should be
    # adjacent to each other (i.e., in consecutive periods). For a given curriculum
    # we account for a violation every time there is one lecture not adjacent to
    # any other lecture within the same day. Each isolated lecture in a curriculum
    # counts as 2 points of penalty.
    # – Room Stability All lectures of a course should be given in the same room.
    # Each distinct room used for the lectures of a course, beside the first, counts
    # as 1 point of penalty
    def objective_function(self):
        # Implement logic to calculate the objective function value
        pass

class University:
    def __init__(self, name, courses, rooms, curricula):
        self.name: str = name
        self.courses: dict = courses
        self.rooms: dict = rooms
        self.curricula: set = curricula # Set of frozenset of pairs (course1, course2) representing curricula

    def __str__(self):
        return pformat(vars(self), indent=4)

    def allocate_lectures(self):
        # Implement logic to allocate lectures to timetable
        pass
