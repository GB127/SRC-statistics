from tools import run_time, command_select
from generic import table, entry

class Games(table):
    def __init__(self, PBs, Runs):
        super().__init__()

        data_PBs, data_Runs = {},{}
        for pb in PBs:
            data_PBs[pb.game] = data_PBs.get(pb.game, []) + [pb]
        for run in Runs:
            data_Runs[run.game] = data_Runs.get(run.game, []) + [run]

        for game in data_PBs.keys():
            self.data.append(Game(game, data_PBs[game], data_Runs[game]))


class Game(entry):
    table_size = [27, 2, 1,2,13,5]
    sorter = "game"

    def __init__(self, game, pbs, runs):
        self.game = game

        self.runs = runs
        self.Run_count = len(self.runs)
        self.Run_Total = sum([run.time for run in self.runs])


        self.pbs = pbs
        self.PB_count = len(pbs)
        self.WR_Total = sum([pb.WR for pb in self.pbs])
        self.PB_Total = sum([pb.time for pb in self.pbs])

        self.PB_Total_delta = sum([pb.delta_WR for pb in self.pbs])
        self.PB_perc = round(self.PB_Total / self.WR_Total * 100,2)
