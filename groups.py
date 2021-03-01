from tools import run_time
from run import Save

class Systems:
    def __init__(self, PBs, Runs):
        self.data = []
        self.PBs = {}
        for pb in PBs:
            self.PBs[pb.system] = self.PBs.get(pb.system, []) + [pb]
        for system, runs in self.PBs.items():
            self.data.append(Save(system, runs))
        self.Runs = {}
        for run in Runs:
            self.Runs[pb.system] = self.Runs.get(pb.system, []) + [pb]

