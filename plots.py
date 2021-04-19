import matplotlib.pyplot as plot
from tools import run_time, command_select


class plots_generic:
    def __init__(self):
        self.times = None
        self.percents = None

    def min_max(self):
        self.min_times, self.max_times = 80000000, 0  #TODO: there is surely a way to avoid that number.
        for data in self.times.values():
            self.min_times = min(min(data), self.min_times)
            self.max_times = max(max(data), self.min_times)

    def histo_times(self):
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=self.min_times, right=self.max_times)
        plot.legend()
        plot.show()


    def histo_percents(self, min_perc, max_perc):
        plot.xticks(plot.xticks()[0],[f'{x} %' for x in plot.xticks()[0]])
        plot.xlim(left=min_perc, right=max_perc)
        plot.show()

    def __call__(self):
        commands = {"end" : "end"}
        if self.times:
            commands["Histogram of times"] = self.histo_times
        if self.percents:
            commands["Histogram of percent"] = self.histo_percents
        while True:
            command_key = command_select(sorted(commands.keys()), printer=True)
            command = commands[command_key]
            if command != "end":
                command()
            else:
                break
