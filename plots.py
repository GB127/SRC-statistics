import matplotlib.pyplot as plot
from tools import run_time


class plots_generic:
    def __init__(self):
        raise Exception("Cannot create an object of this class")

    def min_max(self):
        self.min_times, self.max_times = 80000000, 0  #TODO: there is surely a way to avoid that number.
        for data in self.times.values():
            self.min_times = min(min(data), self.min_times)
            self.max_times = max(max(data), self.min_times)

    def histo_times(self):
        alpha = {
            "Firsts": 0.7,
            "Runs" : 1,
            "PBs" : 0.50,
            "WRs" : 1
            }
        color = {
            "Firsts" : "darkred",
            "Runs" : "cornflowerblue",
            "PBs" : "darkgreen",
            "WRs" : "gold"
            }

        self.min_max()
        for key, data in self.times.items():
            plot.hist(data, label=key, 
                        bins=10, 
                        range=(self.min_times, self.max_times), 
                        alpha=alpha[key],
                        color=color[key])
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=self.min_times, right=self.max_times)

        plot.legend()
        plot.show()

    def __call__(self):
        self.histo_times()

