from .conflicts import Conflicts
from .university import University
from pprint import pformat # Use this to print objects in a pretty way
from random import randint

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

    def __allocate_course(self, course, day, period, room):
        self.tt[room][day][period] = course.name
        self.conflicts.add_room_allocation(course,room)
        self.conflicts.add_teacher_constraint(course.teacher,day,period)
        # Refresh course attributes
        self.university.courses[course.name].number_of_days += 1

    def __dealocate_course(self, day, period, room):
        course_name = self.tt[room][day][period]
        course = self.university.courses[course_name]
        self.tt[room][day][period] = ''
        self.conflicts.remove_room_allocation(course,room)
        self.conflicts.remove_teacher_constraint(course.teacher,day,period)
        # Refresh course attributes
        self.university.courses[course.name].number_of_days -= 1

    def allocate_course(self, course, day, period, room):
        if all([
            self.tt[room][day][period] == '',
            self.valid_allocation(course,room,day,period)
        ]):
            self.__allocate_course(course,day,period,room)

    def deallocate_course(self, day, period, room):
        self.__dealocate_course(day,period,room)


    def geneate_feasible_timetable(self):
        pass

    # H1 - Lectures: Each lecture of a course must be scheduled in
    # a distinct period and a room.
    def h1(self):
        pass

    # H2 - Room occupancy: Any two lectures cannot be assigned
    # in the same period and the same room.
    def h2(self,room,day,period):
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


    def valid_allocation(self,course,room,day,period):
        return all([
            self.h2(room, day, period),
            self.h3(course, day, period),
            self.h4(course, day, period),
        ])
    # Soft constraints
    # The problem includes the following soft constraints:
    # – Room Capacity For each lecture, the number of students that attend the
    # course must be less than or equal to the number of seats in all the rooms
    # that host its lectures. Each student above the capacity counts as 1 point of
    # penalty.
    def s1(self):
        weight = 1
        return weight*sum([
            c.number_of_students - c.room_capacity()
            for c in self.university.courses.values()
            if c.number_of_students > c.room_capacity()
        ])
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
        return weight*sum([
            c.room_stability()
            for c in self.university.courses.values()
        ])

    def objective_function(self):
        return sum([
            self.s1(),
            self.s2(),
            self.s4()
        ])

    def allocation_order(self):
        # List of courses sorted by unavailability constraints
        return sorted(
            self.university.courses.values(),
            key=lambda c: (
                c.curricula_conflicts, # hard constraint
                c.uconstraints_score(), # hard constraint
                c.remaining_days(), #soft constraint
                -self.conflicts.room_stability(c), #soft constraint
            )
        )

    # Move-timeslot: 0< U(0 ,1 ) ≤ 0.10xPAR
    # Swap-timeslot: 0.10xPAR<U(0,1)≤ 0.20xPAR
    # move-location: 0.20xPAR<U(0,1)≤ 0.30xPAR
    # swap-location:0.30xPAR<U(0,1 ) ≤ 0.40xPAR
    # exchange-location:0.40xPAR<U(0,1)≤ 0.50xPAR
    # swap-distinct-timeslots : 0.50xPAR< U(0 ,1 ) ≤ 0.60xPAR
    # move-room : 0.60xPAR< U(0 ,1 ) ≤ 0.70xPAR
    # Swap-room : 0.70xPAR< U(0 ,1 ) ≤ 0.80xPAR

    def __get_random_allocated_timeslot(self,room):
        while True:
            day = randint(0, self.days - 1)
            period = randint(0, self.periods_per_day - 1)
            if self.tt[room][day][period] != '':
                return day,period

    def __swap_timeslot(self,day1,period1,day2,period2,room):
        self.tt[room][day1][period1],self.tt[room][day2][period2] = self.tt[room][day2][period2],self.tt[room][day1][period1]

    # a)The pitch adjustment move-timeslot. An event that
    # meets the probability of 10%×PAR is randomly
    # moved to any feasible timeslot where the room is not
    # changed.
    def move_timeslot(self,room):
        day,period = self.__get_random_allocated_timeslot(room)
        while True:
            # Randomly move to any feasible timeslot where the room is not changed
            course = self.tt[room][day][period]
            new_day = randint(0, self.days - 1)
            new_period = randint(0, self.periods_per_day - 1)
            # Check if the move is valid based on hard constraints
            if self.valid_allocation(course, room, new_day, new_period):
                break

        # Allocate the course in the valid timeslot
        self.__swap_timeslot(day,period,new_day,new_period,room)

    # b) The pitch adjustment Swap-timeslot. An event that
    # meets the probability between 10%×PAR and
    # 20%×PAR is swapped with the timeslot of another
    # event, while the rooms of both events are not
    # changed.
    def swap_timeslot(self,room):
        day1,period1 = self.__get_random_allocated_timeslot(room)
        while True:
            day2,period2 = self.__get_random_allocated_timeslot(room)
            if (day1,period1) != (day2,period2):
                break
        self.tt[room][day1][period1],self.tt[room][day2][period2] = self.tt[room][day2][period2],self.tt[room][day1][period1]
    #
    # c)The pitch adjustment move-location. An event that
    # meets the probability between 20%×PAR and
    # 30%×PAR is randomly moved to any free feasible
    # location in the new harmony solution.
    def move_location(self):
        pass
    #
    # d) The pitch adjustment swap-location. An event that
    # meets the probability between 30%×PAR and
    # 40%×PAR is randomly swapped with another event
    # while the feasibility is maintained.
    def swap_location(self):
        pass
    #
    # e)The pitch adjustment exchange-location. An event
    # that meets the probability between 40%×PAR and
    # 50%×PAR is randomly exchanged with another two
    # events while the feasibility is maintained.
    def exchange_location(self):
        pass
    #
    # f)The pitch adjustment swap-distinct-timeslots. An
    # event that meets the probability between 50%×PAR
    # and 60%×PAR is adjusted as follows: (1) select all
    # the events that have the same timeslot as first event.
    # (2) select a timeslot in random . (3) simply swap all
    # the events in timeslot with all the events in other
    # timeslot without changing the rooms.
    def swap_distinct_timeslots(self):
        pass
    #
    # g) The pitch adjustment move-room. An event that
    # meets the probability between 60%×PAR and
    # 70%×PAR is moved to any free feasible room while
    # the timeslot is not changed.
    def move_room(self):
        pass
    #
    # h) The pitch adjustment Swap-room. An event that
    # meets the probability between 70%×PAR and
    # 80%×PAR swaps its room with a room of another
    # event in the same timeslot while reserving the
    # feasibility.
    def swap_room(self):
        pass
