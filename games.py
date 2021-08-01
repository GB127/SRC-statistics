from generic import table, entry

class Games(table):
    def __init__(self, PBs, Runs):
        PBs_all_games = {}
        Runs_all_games = {}
        for PB in PBs.data:
            PBs_all_games[PB.game] = PBs_all_games.get(PB.game, []) + [PB]

        for run in Runs.data:
            Runs_all_games[run.game] = Runs_all_games.get(run.game, []) + [run]


        self.data = []
        for game_name in PBs_all_games.keys():
            self.data.append(game(game_name, PBs_all_games[game_name], Runs_all_games[game_name]))

class game(entry):
    sorter = "game"
    def __init__(self, game, PBs, Runs):
        self.system = PBs[0].system
        self.game = game

        sum_runs = sum(Runs)
        self.runs_count = len(Runs)
        self.runs_time = sum_runs.time



        sum_PBs = sum(PBs)
        self.PB_count = len(PBs)
        self.WR_time = sum_PBs.WR
        self.PB_time = sum_PBs.time
        self.delta = sum_PBs.delta
        self.perc_WR = sum_PBs.perc_WR