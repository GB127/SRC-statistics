from tools import run_time, command_select
from generic import table, entry



class Game(entry):
    table_size = [3, 17, 21]
    sorter = "game"

    def __init__(self, game, pbs, runs):
        self.game = game

        self.Runs = runs
        self.Run_count = len(self.Runs)
        self.Run_Total = sum([run.time for run in self.Runs])


        self.Pbs = pbs
        self.PB_count = len(pbs)
        self.PB_Total = sum([pb.time for pb in self.Pbs])

        self.PB_Total_delta = sum([pb.delta_WR for pb in self.Pbs])
        self.WR_Total = sum([pb.WR for pb in self.Pbs])
        self.PB_perc = round(self.PB_Total / self.WR_Total * 100,2)

    def __str__(self):
        tempo = [
                    f'{self.game[:30]:30}',
                    f'{self.Run_count:2}',
                    f'{self.Run_Total:>9}',
                    f'{self.PB_count:2}',
                    f'{self.PB_Total:>9} (+{self.PB_Total_delta})',
                    f'{self.PB_perc:>6} %'
                ]
        return " | ".join(tempo)

    def sortable(self):
        tempo = list(self.__dict__)
        tempo.remove("Pbs")
        tempo.remove("Runs")
        return tempo




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

    def foot(self):
        runs_count = sum([game.Run_count for game in self.data])
        total_runs = sum([game.Run_Total for game in self.data])
        total_PBs = sum([game.PB_Total for game in self.data])
        PBs_count = sum([game.PB_count for game in self.data])
        total_WRs = sum([game.WR_Total for game in self.data])
        total_deltas = sum([game.PB_Total_delta for game in self.data])
        perc_average = round(total_PBs / total_WRs * 100, 2)


        string1 = "-" * 93 + "\n"
        string2 = f"{len(self.data):<3} games{'':28}|{runs_count:3} | {total_runs:9} |{PBs_count:3} | {total_PBs:>9} (+{total_deltas:7})| {perc_average} %\n"
        string3 = f"{len(self.data):<3} games{'':28}|{int(runs_count/len(self.data)):3} | {run_time(total_runs/len(self.data)):9} |{int(PBs_count/len(self.data)):3} | {run_time(total_PBs/len(self.data)):>9} (+{run_time(total_deltas/len(self.data)):7}) | {perc_average} %"

        return string1 + string2 + string3

