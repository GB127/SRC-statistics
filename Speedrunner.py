from Runs import Runs
from Runs import PBs


class Speedrunner:
    def __init__(self, runs, pbs):
        self.runs = Runs(runs)
        self.pbs = PBs(pbs)
