import datetime
class run_time:

    def __init__(self, seconds):
        self.time = seconds
    def __str__(self):
        return str(datetime.timedelta(seconds=int(self.time)))

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time


    def __format__(self, specs):
        return format(str(self), specs)

    def __mul__(self, integ):
        return run_time(self.time * integ)
    __rmul__ = __mul__

    def __round__(self, number):
        return run_time(round(self.time, number))

    def __truediv__(self, integ):
        return self.time / integ

    def __rtruediv__(self,integ):
        return integ / self.time

    def __sub__(self, other):
        return run_time(self.time - other.time)

    def __add__(self, other):
        if isinstance(other, run_time):
            return run_time(self.time + other.time)
        if isinstance(other, int):
            return run_time(self.time + other)
    __radd__ = __add__

