from tools import run_time, command_select
from run import Run, PB, Save, System, Game
from generic import table
import matplotlib.pyplot as plot

class Runs(table):
    def __init__(self, data):
        self.data = []
        for run in data:
            if run["times"]["primary_t"] >= 180 and not run["level"]:
                self.data.append(Run(run))

    def foot(self):
        string1 = f"{'-' * 80}\n" 
        string2 = f"{'Total |':>60}{self.total_time():>11}\n"
        string3 = f"{'Average |':>60}{self.average_time():>11}\n"
        return string1 + string2 + string3

        average = run_time(self.total_time() / len(self))

    def __str__(self):
        return f'{len(self)} runs ({self.total_time().days()})'

    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("IDs")
        return types

    def total_time(self):
        return sum([x.time for x in self.data])

    def average_time(self):
        return run_time(self.total_time() / len(self))

    def mean_time(self):
        return run_time(self.total_time() / self.__len__())


class PBs(Runs):
    def __init__(self, data):
        self.data = []
        for pb in data:
            if pb["run"]["times"]["primary_t"] > 180 and not pb["run"]["level"]:
                self.data.append(PB(pb))

    def __str__(self):
        return f'{len(self)} PBs ({self.total_time().days()})'

    def plot(self):
        plot.plot([run.time.time for run in self.data], label=f'PBs')
        plot.plot([run.WR.time for run in self.data], label=f'WRs', c="gold")

        plot.ylabel("Time")
        plot.ylim(bottom=0)
        plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])
        plot.legend()
        plot.show()



    def total_WR(self):
        return sum([x.WR for x in self.data])
    def mean_percWR(self):
        return round(self.total_time() / self.total_WR() * 100, 2)
    def total_deltaWR(self):
        return sum([x.delta_WR for x in self.data])
    def mean_deltaWR(self):
        return run_time(self.total_deltaWR() / self.__len__())

    def get_header(self):
        types = super().get_header()
        types.remove("leaderboard")
        types.remove("WR")
        return types


    def foot(self):  # TODO : user super!
        string1 = f"{'-' * 107}\n" 
        string2 = f"{'Total |':>60}{self.total_time():>11}|+ {self.total_deltaWR():9}| {self.mean_percWR()} %\n"
        string3 = f"{'Average |':>60}{self.average_time():>11}|+ {self.mean_deltaWR():9}| {self.mean_percWR()} %"
        return string1 + string2 + string3


class Saves(table):

    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("runs")
        types.remove("save")
        return types

    def __str__(self):
        return f"{len(self.data)} PBs with multiple runs"

    def __init__(self, PBs, Runs):
        self.data = []
        for pb in PBs:
            tempo = Save(pb, Runs)
            if tempo.first != tempo.PB:
                self.data.append(tempo)

    def foot(self):  # TODO : user super!
        return "allo"




class Games(table):
    def __init__(self, PBs, Runs):
        self.data = []
        data_PBs, data_Runs = {},{}
        for pb in PBs:
            data_PBs[pb.game] = data_PBs.get(pb.game, []) + [pb]
        for run in Runs:
            data_Runs[run.game] = data_Runs.get(run.game, []) + [run]

        for game in data_PBs.keys():
            self.data.append(Game(game, data_PBs[game], data_Runs[game]))

    def __str__(self):
        return f'{len(self.data)} Games'





class Systems(table):
    def __init__(self, PBs, Runs):
        self.data = []
        data_PBs, data_Runs = {},{}
        for pb in PBs:
            data_PBs[pb.system] = data_PBs.get(pb.system, []) + [pb]
        for run in Runs:
            data_Runs[run.system] = data_Runs.get(run.system, []) + [run]

        for one_system in data_PBs.keys():
            self.data.append(System(one_system, data_PBs[one_system], data_Runs[one_system]))

    def __str__(self):
        return f'{len(self.data)} systems'