from tools import run_time, command_select
from generic import table, entry
from allRuns import Run
import matplotlib.pyplot as plot


class Saves(table):
    def __init__(self, PBs, Runs):
        super().__init__()

        print("Initializing Saves")
        for pb in PBs:
            tempo = Save(pb, Runs)
            if tempo.first != tempo.time:
                self.data.append(tempo)

    def plot_save(self):
        print("Select one run to plot")
        select = command_select(self.data)
        select.plot_improvement()

    def __str__(self):
        return super().__str__().replace("+", "-")

    def plot_all_saves(self):
        all_plots = []
        for category in self.data:
            all_plots.append(list(reversed([run.time.time for run in category.runs])))
        for saves in all_plots:
            plot.plot(saves)
        plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])
        plot.show()


    def histo_times(self):
        plot.title(f"{self.__class__.__name__}")
        data_PBs = [one.time.time for one in self.data]
        data_WRs = [one.first.time for one in self.data]



        plot.hist([data_PBs],color="darkgreen", bins=10,
            range=(
                    min(min(data_PBs), min(data_WRs)), 
                    max(max(data_PBs), max(data_WRs))
                    ))
        plot.hist([data_WRs],color="darkred", bins=10, alpha=0.7,
            range=(
                    min(min(data_PBs), min(data_WRs)), 
                    max(max(data_PBs), max(data_WRs))
                    ))

        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=min(min(data_PBs), min(data_WRs)),right=max(max(data_PBs), max(data_WRs)))
        plot.show()


class Save(entry):
    sorter = "time"

    def __init__(self, PB, Runs):
        self.system = PB.system
        self.game = PB.game
        self.category = PB.category
        self.runs = []
        for run in Runs:
            if run.game == self.game and run.category == self.category:
                self.runs.append(run)
        self.count = len(self.runs)

        Run.sorter = "time"
        self.runs.sort()
        self.first = self.runs[-1].time
        self.time = PB.time
        self.delta = self.first - self.time
        self.perc1st = round(self.delta/self.first * 100, 2)

        self.WR = PB.WR

    def plot_improvement(self):
        data = [one.time.time for one in self.runs]
        data.reverse()
        plot.plot(data)
        plot.axhline(self.WR.time, color="gold")
        plot.title(f"{self.game}\n{self.category}")
        plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])

        plot.show()
    def __add__(self, other):
        tempo = super().__add__(other)
        tempo.perc1st = round(tempo.delta/tempo.first * 100, 2)
        return tempo

    def __truediv__(self, other):
        tempo = super().__truediv__(other)
        tempo.perc1st = round(tempo.delta/tempo.first * 100, 2)
        return tempo

    def __str__(self):
        return super().__str__().replace("+", "-")