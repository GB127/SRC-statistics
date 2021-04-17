import matplotlib.pyplot as plot
from tools import run_time


class plots:

    def __init__(self, data_to_plot):
        self.times = sorted([run.time.time for run in data_to_plot])
        self.min = self.times[0]
        self.max = self.times[-1]
    def __str__(self):
        return str(self.filter())

    def filter(self):
        return [one for one in self.times if one <= self.max and self.min <= one]


    def histo_table(self):
        print(self.filter())
        plot.hist(self.filter())
        print(self.min, self.max)
        print(type(self.min), type(self.max))
        #plot.xticks(plot.xticks()[0],[x for x in plot.xticks()[0]])
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])

        plot.xlim(left=self.min, right=self.max)

        plot.show()
    def __call__(self):
        self.histo_table()
