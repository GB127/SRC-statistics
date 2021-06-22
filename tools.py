from datetime import timedelta
from os import system
import matplotlib.pyplot as plot


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

    def __format__(self, specs):
        return format(str(self), specs)

    def days(self):
        return str(timedelta(seconds=int(self.time)))


    # Comparateurs
    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __ne__(self, other):
        return self.time != other.time


    # Opérations
    def __add__(self, other):
        if isinstance(other, run_time):
            return run_time(self.time + other.time)
        if isinstance(other, int):
            return run_time(self.time + other)
    __radd__ = __add__

    def __sub__(self, other):
        return run_time(self.time - other.time)


    def __mul__(self, integ):
        return run_time(self.time * integ)
    __rmul__ = __mul__


    def __truediv__(self, integ):
        return self.time / integ

    def __rtruediv__(self,integ):
        return integ / self.time

    def __round__(self, number):
        return run_time(round(self.time, number))


def plot_histo(data, title, typ):
    plot.title(title)
    if typ == "time":
        for one in data:
            assert isinstance(one, run_time), "Must be a run_time"
        data_float = sorted([one.time for one in data])
        plot.hist(data_float, bins=10)
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=data_float[0], right=data_float[-1])
    elif typ == "%":
        for one in data:
            assert isinstance(one, float), "Must be a float"
        data.sort()
        plot.hist(data, bins=10)
        plot.xlim(left=100, right=data[-1])
    else:
        raise BaseException("Must use a typ argument")


    plot.show()



def plot_line(datas, title, ymin=0, ymax=None):
    plot.title(title)
    for data in datas:
        for one in data:
            assert isinstance(one, run_time), "Must be a run_time"
        data_float = [one.time for one in data]
        plot.plot(data_float)

    # Y axis
    plot.ylim(bottom=ymin, top=ymax)
    plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])





    plot.show()







def command_select(iterable, printer=False):
    """Reusable function for command selection.
        Returns the selection.

        Args:
            iterable ([type]): list of options to select
            printer (bool, optional): Print the iterable. Defaults to False.
        """
    if printer:
        for no, one in enumerate(iterable): print(f'{no + 1:>4} - {one}')
    while True:
        try:
            commant = input(f"Which option? [1 - {len(iterable)}] ")
            if int(commant) != 0:
                return list(iterable)[int(commant) - 1]
            raise BaseException
        except:
            if commant == "end":
                return "end"
            pass