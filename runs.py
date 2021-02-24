from tools import run_time
from run import Run, PB

class Runs:

    def __init__(self,data):

        self.data = []
        for run in data:
            if run["times"]["primary_t"] < 180:
                pass  # FIXME : I'm sure there is a way to write something like next or continue
            else:
                self.data.append(Run(run))

        
    def __len__(self):
        return len(self.data)
    def total_time(self):
        return sum([x.time for x in self.data])
    def mean_time(self):
        return run_time(self.total_time() / self.__len__())
    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)
    def total_deltaWR(self):
        return sum([x.delta_WR() for x in self.data])
    def mean_deltaWR(self):
        return run_time(self.total_deltaWR() / self.__len__())


class PBs(Runs):
    def __init__(self, data):
        self.data = []
        for pb in data:
            self.data.append(PB(pb))


