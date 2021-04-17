import matplotlib.pyplot as plot
from tools import run_time


class plots:
    max = 1000000
    min = 1000
    def __init__(self, data_to_plot):
        self.times = [run.time.time for run in data_to_plot]

    def __str__(self):
        return str(self.filter())

    def filter(self):
        return [one for one in self.times if one < self.max and self.min < one]


    def histo_table(self):
        plot.hist(self.filter())
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.show()
    def __call__(self):
        self.histo_table()
