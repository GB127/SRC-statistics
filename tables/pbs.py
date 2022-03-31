from entries.personal_best import PB
from tables.base import Base_Table
from plots.handler import window_handler
from plots.histo import Histo_app
from plots.pie import Pie_app
from statistics import mean, geometric_mean, stdev


class Table_pb(Base_Table):
    def __init__(self, list_runs:list, include_lvl:bool):
        self.data = []
        for data in list_runs:
            if include_lvl == bool(data["run"]["level"]):
                self.data.append(PB(data))

    def __call__(self):
        super().__call__(self.histo, self.pie, self.plots, self.sort)  # pragma: no cover


    def histo(self): # pragma: no cover
        window_handler(self.data, Histo_app)

    def pie(self):# pragma: no cover
        window_handler(self.data, Pie_app)# pragma: no cover

    def sum(self):
        tempo = super().sum()
        tempo.leaderboard = sum([len(x.leaderboard) for x in self.data])
        tempo.update_data()
        return tempo

    def mean(self):
        tempo = super().mean()
        tempo.leaderboard = mean([len(x.leaderboard) for x in self.data])
        tempo.update_data()
        return tempo

    def stand_dev(self):
        tempo = super().stand_dev()
        tempo.leaderboard = stdev([len(x.leaderboard) for x in self.data])
        return tempo

    def geomean(self):
        tempo = super().geomean()
        tempo.leaderboard = geometric_mean([len(x.leaderboard) for x in self.data])
        tempo.update_data()
        return tempo

    def stand_dev_geo(self):
        tempo = super().stand_dev_geo()
        tempo.leaderboard = stdev([len(x.leaderboard) for x in self.data], geometric_mean([len(x.leaderboard) for x in self.data]))
        return tempo