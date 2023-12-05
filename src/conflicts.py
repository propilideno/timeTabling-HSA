from pprint import pformat # Use this to print objects in a pretty way

class Conflicts:
    def __init__(self):
        self.teacher_constraints = dict() # Dict of frozenset(day, period) representing teacher constraints
        self.room_allocation = dict() # Dict of set of rooms representing room allocation

    def __str__(self):
        return pformat(vars(self), indent=4)

    def add_teacher_constraint(self, teacher,day,period):
        self.teacher_constraints[teacher].add(frozenset((day, period)))

    def remove_teacher_constraint(self, teacher, day, period):
        self.teacher_constraints[teacher].remove(frozenset((day, period)))

    def is_teacher_available(self, teacher, day, period):
        return {day,period} in self.teacher_constraints[teacher]


    ### Soft Constraints ###

    def add_room_allocation(self, course, room):
        self.room_allocation[course].add(room)

    def remove_room_allocation(self, course, room):
        self.room_allocation[course].remove(room)
    
    def room_stability(self,course):
        return len(self.room_allocation[course]) - 1 # 0 if only one room
