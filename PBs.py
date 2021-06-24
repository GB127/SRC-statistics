from allRuns import Runs, Run
from leaderboard import leaderboard
from tools import run_time, command_select, clear, plot_histo


class PBs(Runs):
    def __init__(self, data):
        self.data = []
        self.backup = []


        for pb in data:
            self.data.append(PB(pb))


    def stats_leaderboard(self):
        clear()
        which = command_select(self.data, printer=True)
        which.leaderboard()

    def methods(self):
        metho = super().methods()
        metho["Leaderboard"] = self.stats_leaderboard
        return metho

    def plot_histo(self):
        command = command_select(["WR%", "delta_WR", "time"], printer=True)
        if command == "WR%":
            plot_histo(sorted([one.perc_WR for one in self.data]), "Histogram of %WR", typ="%", min_data=100)
        if command == "time":
            tempo = sorted([one.time.time for one in self.data])
            plot_histo(tempo, "Histogram of PBs time", typ="time")
        elif command == "delta_WR":
            tempo = sorted([one.delta_WR.time for one in self.data])
            plot_histo(tempo, "Histogram of PBs-WR deltas", typ="time")



class PB(Run):
    table_size = Run.table_size + [2, 3, 5, 1]

    def __init__(self, data):
        super().__init__(data["run"])
        tempo_place = data["place"]
        tempo_leaderboard = leaderboard(self.IDs, self.game, self.category, tempo_place, level=self.level)

        self.WR = tempo_leaderboard.WR
        self.delta_WR = self.time - self.WR
        self.perc_WR = round((self.time) / self.WR * 100, 2)
        self.place = data["place"]
        self.leaderboard = tempo_leaderboard
        self.perc_LB = round((len(self.leaderboard) - self.place) / len(self.leaderboard) * 100,2)


    def sortable(self):
        tempo = super().sortable()
        tempo.remove("leaderboard")
        tempo.remove("place")
        return tempo


