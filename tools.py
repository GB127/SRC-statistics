from datetime import timedelta
from os import system

clear = lambda: system('cls')

class run_time:
    def __init__(self, seconds):
        self.time = seconds

    def __str__(self):
        self.hours = str(int(self.time//3600))
        self.minutes = int(self.time % 3600 // 60)
        if self.minutes < 10: self.minutes = "0" + str(self.minutes)
        self.seconds = int(self.time % 3600 % 60 % 60)
        if self.seconds < 10: self.seconds = "0" + str(self.seconds)
        return f'{self.hours}:{self.minutes}:{self.seconds}'

    def days(self):
        return str(timedelta(seconds=int(self.time)))

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

def command_select(iterable, printer=False):
    """Reusable function for command selection.
        Returns the selection.

        Args:
            iterable ([type]): list of options to select
            printer (bool, optional): Print the iterable. Defaults to False.
        """
    while True:
        try:
            commant = input(f"Which option? [1 - {len(iterable)}]")
            if int(commant) != 0:
                return iterable[int(commant) - 1]
            raise BaseException
        except:
            if commant != "end":
                pass
            else:
                return "end"

