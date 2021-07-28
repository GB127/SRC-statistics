from api import get_leaderboard, get_user, get_leaderboard_level, get_leaderboards, get_leaderboards_level
from generic import table, entry
from tools import run_time
import matplotlib.pyplot as plot
import numpy as np


class leaderboard(table):
    def __init__(self, IDs, game, category, rank, level=None):
        super().__init__()

        self.IDs = IDs
        self.game = game
        self.category = category
        self.place = rank
        self.level = level
        if not IDs[2]:
            print(f"     Fetching {self.game} - {self.category}")
            infos = get_leaderboard(IDs)["data"]["runs"]
        else:
            print(f"     Fetching {self.game} - {level} - {self.category}")
            infos = get_leaderboard_level(IDs)["data"]["runs"]
        self.WR = run_time(infos[0]["run"]["times"]["primary_t"])
        for no, one in enumerate(infos):
            self.data.append(ranking(one, self.WR))

    def plot_evolution(self):
        if not self.IDs[2]:  # FIXME : Issue if Variables
            toplot = get_leaderboards(self.IDs)
        if self.IDs[2]:
            toplot = get_leaderboards_level(self.IDs)

        for year, times in toplot.items():
            data = [one.time for one in times]
            if len(data) > 1:
                plot.plot(data, label=year)
            else:
                plot.plot(data,"o", label=year)

        plot.show()



    def plot(self):
        if len(self.data) > 1:
            plot.plot([x.time.time for x in self.data[::-1]])
        else:
            plot.plot([x.time.time for x in self.data[::-1]], "o")

        plot.plot(len(self.data) - self.place[0], self.place[1].time, "ro")
        plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])
        plot.title(f"{self.game}\n{self.category}")
        plot.xticks(np.arange(0, len(self.data), 1.0))

        plot.show()

    def __add__(self, other):
        if isinstance(other, leaderboard):
            return len(self) + len(other)
        elif isinstance(other, int):
            return len(self) + other
    __radd__ = __add__

class ranking(entry):
    def __init__(self, data, WR):
        self.WR = WR
        self.place = data["place"]
        self.time = run_time(data["run"]["times"]["primary_t"])
        self.delta_p = self.time - WR
        self.perc = round(self.time / WR * 100, 2)

        if self.place != 1:
            self.moy_rank = run_time((self.time-WR) / (self.place-1))
        else:
            self.moy_rank = run_time(0)

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        tempo = super().__str__()
        datas = tempo.split(" | ")
        datas2 = " | ".join(datas[1:])
        return datas2

    def __add__(self, integ):
        tempo = super().__add__(integ)
        tempo.perc = round((tempo.time/ tempo.WR) * 100,2)
        return tempo



    def __truediv__(self, integ):
        tempo = super().__truediv__(integ)
        tempo.perc = round((tempo.time/ tempo.WR) * 100,2)
        return tempo

if __name__ == "__main__":

    test = ['o6g7xx62', '7dgw5724', None, {}]
    test = leaderboard(test, " Donkey Kong Land III", "Any%", (2, run_time(5420)))
    print(test)