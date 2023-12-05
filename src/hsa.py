from .university import Course
from .timetable import TimeTable
from random import randint,uniform
from copy import deepcopy

class HSA:
    def __init__(self, timetable: TimeTable):
        self.HMS = 50
        self.HMCR = 0.9
        self.PAR = 1.0
        self.HM = []  # List of feasible timetables ordered by fitness
        self.MI = int(10e5) # Max iterations
        self.timetable: TimeTable = timetable

    def pitch_adjustment(self, timetable, course, room):
        pitch_value = uniform(0, 1)

        if pitch_value <= 0.10 * self.PAR:
            timetable.move_timeslot(room)
        elif 0.10 * self.PAR < pitch_value <= 0.20 * self.PAR:
            timetable.swap_timeslot(room)
        elif 0.20 * self.PAR < pitch_value <= 0.30 * self.PAR:
            timetable.move_location()
        elif 0.30 * self.PAR < pitch_value <= 0.40 * self.PAR:
            timetable.swap_location()
        elif 0.40 * self.PAR < pitch_value <= 0.50 * self.PAR:
            timetable.exchange_location()
        elif 0.50 * self.PAR < pitch_value <= 0.60 * self.PAR:
            timetable.swap_distinct_timeslots()
        elif 0.60 * self.PAR < pitch_value <= 0.70 * self.PAR:
            timetable.move_room()
        elif 0.70 * self.PAR < pitch_value <= 0.80 * self.PAR:
            timetable.swap_room()

    def generate_initial_harmony_memory(self):
        for _ in range(self.HMS):
            self.timetable.geneate_feasible_timetable()
            self.HM.append(deepcopy(self.timetable))

    def improvise_new_harmony(self):
        new_timetable: TimeTable = deepcopy(self.timetable)

        for course in new_timetable.university.courses.values():
            for _ in range(course.lectures):
                if uniform(0, 1) <= self.HMCR:
                    # Memory consideration
                    room = randint(0, new_timetable.rooms - 1)
                    self.pitch_adjustment(new_timetable, course, room)
                else:
                    # Random consideration
                    new_timetable.allocate_course(course, randint(0, new_timetable.days - 1),
                                                  randint(0, new_timetable.periods_per_day - 1),
                                                  randint(0, new_timetable.rooms - 1))

        return new_timetable

    def update_harmony_memory(self, new_timetable):
        # Check if the new timetable is better than the worst in the harmony memory
        worst_index = max(range(len(self.HM)), key=lambda i: self.HM[i].fitness)
        if new_timetable.fitness < self.HM[worst_index].fitness:
            self.HM[worst_index] = new_timetable

    def solve(self):
        self.generate_initial_harmony_memory()

        for _ in range(self.MI):
            new_timetable = self.improvise_new_harmony()
            self.update_harmony_memory(new_timetable)

        # Return the best timetable found in the harmony memory
        best_timetable = min(self.HM, key=lambda t: t.fitness)
        return best_timetable
