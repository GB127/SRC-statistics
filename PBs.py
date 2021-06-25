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
    def __init__(self, data):
        super().__init__(data["run"])
        tempo_leaderboard = leaderboard(self.IDs, self.game, self.category, data["place"], level=self.level)

        self.place = data["place"]
        self.WR = tempo_leaderboard.WR
        self.delta_WR = tempo_leaderboard.WR - self.time 
        self.perc_WR = round((self.time) / tempo_leaderboard.WR * 100, 2)

        self.leaderboard = tempo_leaderboard
        self.ranking = f'{data["place"]:>4}/{len(self.leaderboard):<4}'
        self.perc_LB = round((len(tempo_leaderboard) - self.place) / len(tempo_leaderboard) * 100,2)
