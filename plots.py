import matplotlib.pyplot as plot
from tools import run_time


class plots:

    def __init__(self, times):
        # times is a dictionnary.

        self.times = times
        self.min = 0
        self.max = None

    def histo_table(self):
        for key, data in self.times.items():
            plot.hist(data, label=key)
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=self.min, right=self.max)
        plot.legend()
        plot.show()
    def __call__(self):
        self.histo_table()
