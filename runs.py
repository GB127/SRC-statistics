from tools import run_time, command_select
from run import Run, PB, Save, System
from generic import table

class Runs(table):
    def __init__(self, data):
        self.data = []
        for run in data:
            if run["times"]["primary_t"] >= 180 and not run["level"]:
                self.data.append(Run(run))

    def __str__(self):
        return f'{len(self)} runs ({self.total_time().days()})'

    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("IDs")
        return types


class PBs(Runs):
    def __init__(self, data):
        self.data = []
        for pb in data:
            if pb["run"]["times"]["primary_t"] > 180 and not pb["run"]["level"]:
                self.data.append(PB(pb))

    def __str__(self):
        return f'{len(self)} PBs ({self.total_time().days()})'

    def total_WR(self):
        return sum([x.WR for x in self.data])
    def mean_percWR(self):
        return round(self.total_time() / self.total_WR() * 100, 2)
    def total_deltaWR(self):
        return sum([x.delta_WR() for x in self.data])
    def mean_deltaWR(self):
        return run_time(self.total_deltaWR() / self.__len__())

    def get_header(self):
        types = super().get_header()
        types.remove("leaderboard")
        types.remove("WR")
        return types


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
        return str(len(self.data))