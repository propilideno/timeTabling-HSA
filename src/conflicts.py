class Conflicts:
    def __init__(self):
        self.teacher_constraints = dict() # Dict of frozenset(day, period) representing teacher constraints

    def add_teacher_constraint(self, teacher,day,period):
        self.teacher_constraints[teacher].add(frozenset((day, period)))

    def remove_teacher_constraint(self, teacher, day, period):
        self.teacher_constraints[teacher].remove(frozenset((day, period)))

    def is_teacher_available(self, teacher, day, period):
        return {day,period} in self.teacher_constraints[teacher]
