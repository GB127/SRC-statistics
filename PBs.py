from allRuns import Runs, Run
from api import get_leaderboard
from tools import run_time
from plots import histo_generic
import matplotlib.pyplot as plot


class PBs(Runs):
    def __init__(self, data):
        print("Initializing PBs data")
        self.data = []
        for pb in data:
            if pb["run"]["times"]["primary_t"] > 180 and not pb["run"]["level"]:
                self.data.append(PB(pb))

    def __str__(self):
        return f'{len(self)} PBs ({sum([x.time for x in self.data]).days()})'

    def histo(self):
        histo_PBs(self)()
        

    def get_header(self):
        types = super().get_header()
        types.remove("leaderboard")
        types.remove("WR")
        return types


    def foot(self):  #TODO: Redo this
        string1, string2, string3, string4 = super().foot().split("\n")
        
        total_time = sum([pb.time for pb in self.data])
        total_wr = sum([pb.WR for pb in self.data])

        percentage = round(100* total_time / total_wr, 2)

        total_deltaWR = sum([pb.delta_WR for pb in self.data])

        string1 += "-" * 46
        string2 += f' |+ {total_deltaWR} |  {percentage} % |'
        string3 += f' |+ {run_time(total_deltaWR / len(self))}  |  {percentage} % |'





        return "\n".join([string1, string2, string3])


class PB(Run):
    table_size = Run.table_size + [2, 3, 5, 1]

    def sortable(self):
        tempo = super().sortable()
        tempo.remove("leaderboard")
        return tempo

    def __init__(self, data):
        super().__init__(data["run"])
        self.leaderboard = get_leaderboard(self.IDs)  # NOTE : In the future I will create a class leaderboards so I can do fancy stuffs with leaderboards.
        self.WR = run_time(self.leaderboard[0][1])
        self.delta_WR = self.time - self.WR
        self.perc_WR = round((self.time) / self.WR * 100, 2)
        self.place = data["place"]
        self.perc_LB = round((len(self.leaderboard) - self.place) / len(self.leaderboard) * 100,2)

    def __str__(self):
        return super().__str__() + " | ".join([
                                    f'+ {self.delta_WR:<8}',
                                    f'{str(self.perc_WR) + " %":>9}',
                                    f"{f'{self.place}/{len(self.leaderboard)}':9}",
                                    f"{self.perc_LB:6} %"]) + "|"


class histo_PBs(histo_generic):
    def __init__(self, PBs):
        super().__init__()
        self.times = {"WRs" : [run.WR.time for run in PBs.data],
                        "PBs" : [run.time.time for run in PBs.data]
                        }
        self.percents = [run.perc_WR for run in PBs.data]
        self.deltas = {"PBs" : [run.delta_WR.time for run in PBs.data]}
    def histo_percents(self):
        plot.hist(self.percents, 
                        bins=10,
                        range=(100, max(self.percents))
                )
        super().histo_percents(100, max(self.percents))

    def histo_times(self):
        alpha = {
            "PBs" : 0.50,
            "WRs" : 1
            }
        color = {
            "PBs" : "darkgreen",
            "WRs" : "gold"
            }

        self.min_max()
        for key, data in self.times.items():
            plot.hist(data, label=key, 
                        bins=10, 
                        range=(self.min_times, self.max_times), 
                        alpha=alpha[key],
                        color=color[key])
        super().histo_times()



    def histo_deltatimes(self):
        alpha = {
            "PBs" : 0.50,
            "WRs" : 1
            }
        color = {
            "PBs" : "darkgreen",
            "WRs" : "gold"
            }
        for key, data in self.deltas.items():
            plot.hist(data, label=key, 
                        bins=10, 
                        alpha=alpha[key],
                        color=color[key])
        super().histo_deltatimes()
