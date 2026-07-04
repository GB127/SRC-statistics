from run import Run
from parameters import max_str_game
from utils import time_str
from statistics import mean, median

class PBs(list):
    def __init__(self, data):
        print(data[0].keys())
        super().__init__([PB(x) for x in data if (x["time"] and not x["obsolete"])])

    def __str__(self):
        entete = f'{"Game":{max_str_game}}|{"Time":^9}|'
        line = "-" * len(entete)
        body = "\n".join(str(x) for x in self)

        return body


class PB(dict):
    id_to_game = {}

    def __init__(self, data):
        assert self.id_to_game, "Game db must be updated first."
        super().__init__(data)

    @staticmethod
    def update_game_db(data):
        test = data["games"]
        for one_game in test:
            id = one_game["id"]
            name = one_game["name"]
            PB.id_to_game[id] = name

    def __str__(self):
        game_str_size = max([len(x) for x in self.id_to_game.values()])
        final_game_str = min(max_str_game, game_str_size)
        return f'{self.id_to_game[self["gameId"]][:final_game_str]:{final_game_str}}|{time_str(self["time"]):>9}|'


if __name__ == "__main__":
    from Speedrunner import Speedrunner
    test = Speedrunner().PBs

    print(test)