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

class Room:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __str__(self):
        return pformat(vars(self), indent=4)

    def __eq__(self, other):
        return self.name == other.name

class Curriculum:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

    def __str__(self):
        return pformat(vars(self), indent=4)
