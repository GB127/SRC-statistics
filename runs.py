from tools import run_time, command_select
from run import Run, PB, Save

class Runs:
    def __init__(self, data):
        self.data = []
        for run in data:
            if run["times"]["primary_t"] >= 180 and not run["level"]:
                self.data.append(Run(run))

    def __call__(self):
        def table():
            header = " no |"
            for no, size in enumerate(self.data[0].table_size()):
                header += f' {self.get_header()[no]}' + " "*size + "|"
            print(header)
            print("-" * len(header))
            for no, entry in enumerate(self):
                print(f'{no+1:^3} | {entry}')
            print("-" * len(header))

        while True:
            table()
            command = input("What do you want to do? [sort, end]")
            if command == "end": break
            elif command == "sort":
                self.data[0].change_sort()
                self.data.sort()

    def __str__(self):
        return f'{len(self)} runs ({self.total_time().days()})'


    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)


    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("IDs")
        return types



    def total_time(self):
        return sum([x.time for x in self.data])

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


class Saves(Runs):

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

