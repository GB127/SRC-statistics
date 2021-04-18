import matplotlib.pyplot as plot
from tools import run_time


class plots:

    def __init__(self, times):
        # times is a dictionnary.

        self.times = times
        self.min_max()

    def min_max(self):
        self.min, self.max = 80000000, 0  #TODO: there is surely a way to avoid that number.
        for data in self.times.values():
            self.min = min(min(data), self.min)
            self.max = max(max(data), self.min)



    def histo_table(self):
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
        #if "Firsts" in self.times.keys():
        #    alpha["PBs"] = 1


        for key, data in self.times.items():
            plot.hist(data, label=key, 
                        bins=10, 
                        range=(self.min, self.max), 
                        alpha=alpha[key],
                        color=color[key])
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=self.min, right=self.max)
        plot.legend()
        plot.show()
    def __call__(self):
        self.histo_table()