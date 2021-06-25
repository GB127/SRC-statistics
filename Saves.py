from tools import run_time, command_select
from generic import table, entry
from tools import plot_line, plot_histo
from allRuns import Run

class Saves(table):
    def __init__(self, PBs, Runs):
        super().__init__()

        print("Initializing Saves")
        for pb in PBs:
            tempo = Save(pb, Runs)
            if tempo.first != tempo.time:
                self.data.append(tempo)


    def methods(self):
        metho = super().methods()
        metho["Plot 1 game's saves"] = self.plot_save
        metho["Plot all saves"] = self.plot_all_saves
        metho["Histo"] = self.plot_histo
        return metho

    def plot_save(self):
        print("Select one run to plot")
        select = command_select(self.data)
        select.plot_improvement()


    def plot_all_saves(self):
        all_plots = []
        for category in self.data:
            all_plots.append(list(reversed([run.time for run in category.runs])))
        plot_line(all_plots, "All improvements")


    def plot_histo(self):
        command = command_select(["PB%", "Improvements", "time"], printer=True)
        if command == "PB%":
            plot_histo(sorted([one.perc1st for one in self.data]), "Histogram of %PB", typ="%", max_data=100)
        elif command == "Improvements":
            tempo = sorted([one.save.time for one in self.data])
            plot_histo(tempo, "Histogram of PBs-1st deltas", typ="time")
        elif command == "time":
            tempo = sorted([one.time.time for one in self.data])
            plot_histo(tempo, "Histogram of PBs time", typ="time")
        



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

    def plot_improvement(self):
        data = [one.time for one in self.runs]
        data.reverse()
        plot_line([data], f"{self.game}-{self.category} Improvement", ymin=None)

