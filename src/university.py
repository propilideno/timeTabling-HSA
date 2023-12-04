from pprint import pformat # Use this to print objects in a pretty way
from .conflicts import Conflicts

class Course:
    def __init__(self, name, professor, lectures, min_days, students):
        self.name = name
        self.professor = professor
        self.lectures = lectures
        self.min_days = min_days
        self.students = students
        self.uconstraints = set() # Set of tuple (day, period) representing unavailability constraints

        # Redundant attributes
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
        self.conflicts: Conflicts = Conflicts()
        #tt[room][day][period] with list comprehension
        self.tt = [[['' for _ in range(periods_per_day)] for _ in range(days)] for _ in range(rooms)]
        self.fitness = 0

    def __str__(self):
        return pformat(vars(self), indent=4)

    def allocate_course(self, course, day, period, room):
        if self.tt[room][day][period] == '':
            self.tt[room][day][period] = course.name

    # H1 - Lectures: Each lecture of a course must be scheduled in
    # a distinct period and a room.
    def h1(self):
        pass

    # H2 - Room occupancy: Any two lectures cannot be assigned
    # in the same period and the same room.
    def h2(self,day,room,period):
        return self.tt[room][day][period] != ''

    # H3 - Conflicts: Lectures of courses in the same curriculum or
    # taught by the same teacher cannot be scheduled in the same
    # period, i.e., no period can have an overlapping of students nor
    # teachers.
    def h3(self,course,day,period):
        # If any of the courses in the curriculum is already allocated in the same period, return True
        return any({self.tt[r][day][period],course} in self.university.curricula for r in range(self.rooms))

    # H4 - Availability: If the teacher of a course is not available at
    # a given period, then no lectures of the course can be assigned
    # to that period.
    def h4(self,course,day,period):
        self.conflicts.is_teacher_available(course.professor,day,period)

    # Soft constraints
    # The problem includes the following soft constraints:
    # – Room Capacity For each lecture, the number of students that attend the
    # course must be less than or equal to the number of seats in all the rooms
    # that host its lectures. Each student above the capacity counts as 1 point of
    # penalty.
    def s1(self):
        weight = 1
        pass
    # – Minimum Working Days The lectures of each course must be spread into
    # the given minimum number of days. Each day below the minimum counts
    # as 5 points of penalty.
    def s2(self):
        weight = 5
        return weight*sum([
            c.number_of_days - c.min_days 
            for c in self.university.courses.values()
            if c.number_of_days < c.min_days
        ])

    # – Curriculum Compactness Lectures belonging to a curriculum should be
    # adjacent to each other (i.e., in consecutive periods). For a given curriculum
    # we account for a violation every time there is one lecture not adjacent to
    # any other lecture within the same day. Each isolated lecture in a curriculum
    # counts as 2 points of penalty.
    def s3(self):
        weight = 2
        pass

    # – Room Stability All lectures of a course should be given in the same room.
    # Each distinct room used for the lectures of a course, beside the first, counts
    # as 1 point of penalty
    def s4(self):
        weight = 1
        pass

    def objective_function(self):
        return self.s2()

    def allocation_order(self):
        keysByScore = sorted(self.university.courses.values(), key=lambda c: c.uconstraints_score())
        return keysByScore # List of courses sorted by unavailability constraints

class University:
    def __init__(self, name, courses, rooms, curricula):
        self.name: str = name
        self.courses: dict = courses
        self.rooms: dict = rooms
        self.curricula: set = curricula # Set of frozenset of pairs (course1, course2) representing curricula

    def __str__(self):
        return pformat(vars(self), indent=4)
