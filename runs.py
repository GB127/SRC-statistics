from tools import run_time, command_select
from run import Run, PB

class Runs:

    def __init__(self, data):

        self.data = []
        for run in data:
            if run["times"]["primary_t"] >= 180:
                self.data.append(Run(run))


    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f'{len(self)} runs ({self.total_time().days()})'

    def __call__(self):
        while True:
            self.table()
            command = input("What do you want to do? [sort, end]")
            if command == "end": break
            elif command == "sort":
                self.data[0].change_sort()
                self.data.sort()

    def table(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("IDs")
        header = " | ".join(types)
        print(header)
        for no, entry in enumerate(self):
            print(f'{no+1:^3} | {entry}')


    def total_time(self):
        return sum([x.time for x in self.data])


    def mean_time(self):
        return run_time(self.total_time() / self.__len__())




class PBs(Runs):
    def __init__(self, data):
        self.data = []
        for pb in data:
            tempo = PB(pb)
            if tempo.leaderboard:  # NOTE : Tempo fix. Some runs can't get a proper leaderboard for some reason.
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

