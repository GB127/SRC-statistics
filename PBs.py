from allRuns import Runs, Run
from leaderboard import leaderboard
from tools import run_time, command_select, clear
import matplotlib.pyplot as plot


class PBs(Runs):
    def __init__(self, data):
        super().__init__()
        for pb in data:
            self.data.append(PB(pb))


    def __str__(self):
        tostr = super().__str__()
        line = f'{"-" * len(str(self.data[0]))}-----'
        head, body, foot_original = tostr.split(line)
        head_split = head.split(" | ")
        reordered = head_split[:3] + [head_split[4]] + [head_split[3]] + head_split[5:]
        head = " | ".join(reordered)
        return line.join([head, body, foot_original])

    def histo_times(self):
        plot.title(f"{self.__class__.__name__}")
        data_PBs = [one.time.time for one in self.data]
        data_WRs = [one.WR.time for one in self.data]



        plot.hist([data_WRs],color="gold", bins=10, label="WRs",
            range=(
                    min(min(data_PBs), min(data_WRs)), 
                    max(max(data_PBs), max(data_WRs))
                    ))
        plot.hist([data_PBs], bins=10,color="darkgreen", alpha=0.65,label="PBs",
            range=(
                    min(min(data_PBs), min(data_WRs)), 
                    max(max(data_PBs), max(data_WRs))
                    ))

        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=min(min(data_PBs), min(data_WRs)),right=max(max(data_PBs), max(data_WRs)))
        plot.legend()
        plot.show()



    def open_a_leaderboard(self):
        command_select(self.data).leaderboard()

class PB(Run):
    def __init__(self, data):
        super().__init__(data["run"])

        self.place = data["place"]

        tempo_leaderboard = leaderboard(self.IDs, self.game, self.category, (self.place, self.time), level=self.level)
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
        tempo = super().__add__(other)
        tempo.place = int(tempo.place)
        tempo.ranking = f'{tempo.place:>4}/{tempo.leaderboard:<4}'
        tempo.perc_LB = round((tempo.leaderboard - self.place) / tempo.leaderboard * 100,2)



        tempo.perc_WR = round((tempo.time) / tempo.WR * 100, 2)
        return tempo
