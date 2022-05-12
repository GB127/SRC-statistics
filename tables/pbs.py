from entries.personal_best import PB
from tables.base import Base_Table
from plots.handler import window_handler
from plots.histo import Histo_app
from plots.pie import Pie_app
from statistics import mean, geometric_mean, stdev


class Table_pb(Base_Table):
    def __init__(self, list_runs:list, include_lvl:bool):
        self.data = []
        for no, data in enumerate(list_runs, start=1):
            if include_lvl == bool(data["run"]["level"]):
                self.data.append(PB(data))
            print(f'{no} / {len(list_runs)} PBs processed')


    def __call__(self):
        super().__call__(self.histo, self.pie, self.sort)  # pragma: no cover


    def histo(self):
        window_handler(self.data, Histo_app)  # pragma: no cover

    def pie(self):
        window_handler(self.data, Pie_app)  # pragma: no cover

    def sum(self):
        tempo = super().sum()
        tempo.leaderboard = sum([x.leaderboard for x in self.data])
        tempo["LB %"] = (tempo.leaderboard - tempo.place)/tempo.leaderboard
        tempo["WR %"] = tempo.time / tempo["WR time"]
        return tempo

    def mean(self):
        tempo = super().mean()
        tempo.leaderboard = mean([x.leaderboard for x in self.data])
        tempo["LB %"] = (tempo.leaderboard - tempo.place)/tempo.leaderboard
        tempo["WR %"] = tempo.time / tempo["WR time"]

        return tempo

    def geomean(self):
        tempo = super().geomean()
        tempo.leaderboard = geometric_mean([x.leaderboard for x in self.data])
        tempo["LB %"] = (tempo.leaderboard - tempo.place)/tempo.leaderboard
        tempo["WR %"] = tempo.time / tempo["WR time"]

        return tempo
