from allRuns import Runs, Run
from leaderboard import leaderboard
from tools import run_time, command_select, clear, plot_histo


class PBs(Runs):
    def __init__(self, data):
        super().__init__()
        for pb in data:
            self.data.append(PB(pb))

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


    def __str__(self):
        tostr = super().__str__()
        line = f'{"-" * len(str(self.data[0]))}-----'
        head, body, foot_original = tostr.split(line)
        head_split = head.split(" | ")
        reordered = head_split[:3] + [head_split[4]] + [head_split[3]] + head_split[5:]
        head = " | ".join(reordered)
        return line.join([head, body, foot_original])


class PB(Run):
    def __init__(self, data):
        super().__init__(data["run"])
        tempo_leaderboard = leaderboard(self.IDs, self.game, self.category, data["place"], level=self.level)

        self.place = data["place"]
        self.WR = tempo_leaderboard.WR
        self.delta = self.time - tempo_leaderboard.WR  
        self.perc_WR = round((self.time) / tempo_leaderboard.WR * 100, 2)

        self.leaderboard = tempo_leaderboard
        self.ranking = f'{data["place"]:>4}/{len(self.leaderboard):<4}'
        self.perc_LB = round((len(tempo_leaderboard) - self.place) / len(tempo_leaderboard) * 100,2)

    def __str__(self):
        tostr = super().__str__()
        liste_tostr = tostr.split(" | ")
        reordered = liste_tostr[:3] + [liste_tostr[4]] + [liste_tostr[3]] + liste_tostr[5:]
        
        return " | ".join(reordered)


    def __truediv__(self, other):
        if isinstance(self.leaderboard, leaderboard):
            self.leaderboard = len(self.leaderboard)
        tempo = super().__truediv__(other)
        tempo.leaderboard = int(tempo.leaderboard)
        tempo.place = int(tempo.place)

        tempo.ranking = f'{tempo.place:>4}/{tempo.leaderboard:<4}'
        tempo.perc_LB = round((tempo.leaderboard - tempo.place) / tempo.leaderboard * 100,2)

        tempo.perc_WR = round((tempo.time) / tempo.WR * 100, 2)
        return tempo


    def __add__(self, other):
        if isinstance(self.leaderboard, leaderboard):
            self.leaderboard = len(self.leaderboard)
        if isinstance(other.leaderboard, leaderboard):
            other.leaderboard = len(other.leaderboard)
        tempo = super().__add__(other)
        tempo.leaderboard = int(tempo.leaderboard)
        tempo.place = int(tempo.place)


        tempo.ranking = f'{tempo.place:>4}/{tempo.leaderboard:<4}'
        tempo.perc_LB = round((tempo.leaderboard - self.place) / tempo.leaderboard * 100,2)



        tempo.perc_WR = round((tempo.time) / tempo.WR * 100, 2)
        return tempo
