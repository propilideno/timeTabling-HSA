from pprint import pformat # Use this to print objects in a pretty way

class Course:
    def __init__(self, name, professor, lectures, min_days, students):
        self.name: str = name
        self.professor: str = professor
        self.min_days: int = min_days
        self.students: int = students
        self.uconstraints = set() # Set of tuple (day, period) representing unavailability constraints
        self.curricula_conflicts = 0

        # Volatile Redundant attributes
        self.number_of_days = 0

    def __str__(self):
        return pformat(vars(self), indent=4)

    def __eq__(self, other):
        return self.name == other.name and self.professor == other.professor

    def add_unavailability_constraint(self, day, period):
        self.uconstraints.add((day, period))

    def is_available(self, day, period):
        return (day, period) not in self.uconstraints

    def uconstraints_score(self):
        return len(self.uconstraints)

    def remaining_days(self):
        return self.min_days - self.number_of_days
    
class Room:
    def __init__(self, name, capacity):
        self.name: str = name
        self.capacity: str = capacity

        # Redundant attributes
        self.allocations: int = 0

    def __str__(self):
        return pformat(vars(self), indent=4)

    def __eq__(self, other):
        return self.name == other.name

class University:
    def __init__(self, name, courses, rooms, curricula):
        self.name: str = name
        self.courses: dict = courses
        self.rooms: dict = rooms
        self.curricula: set = curricula # Set of frozenset of pairs (course1, course2) representing curricula

    def __str__(self):
        return pformat(vars(self), indent=4)
