from parameters import max_str_game
from utils import time_str


class Run(dict):
    id_to_game = {}

    def __init__(self, data):
        assert self.id_to_game, "Game db must be updated first."
        unwanted = ["comment", "submittedById", "reason", "dateSubmitted",
                    "hasSplits", "dateVerified", "verifiedById",
                    "enforceMs", "timeWithLoads", "video", "verified", "date",
                    "playerIds", "estimated", "issues", "videoState", "id", "igt", "emulator", "regionId", "orphaned"]
        for one in unwanted:
            del data[one]
        super().__init__(data)

    def __str__(self):
        game_str_size = max([len(x) for x in self.id_to_game.values()])
        final_game_str = min(max_str_game, game_str_size)
        return f'{self.id_to_game[self["gameId"]][:final_game_str]:{final_game_str}}|{time_str(self["time"]):>9}|'

    @staticmethod
    def update_game_db(data):
        test = data["games"]
        for one_game in test:
            id = one_game["id"]
            name = one_game["name"]
            Run.id_to_game[id] = name

    def __gt__(self, other):
        self_game = self.id_to_game[self["gameId"]]
        other_game = other.id_to_game[other["gameId"]]

        if self_game == other_game:
            return self["time"] > other["time"]
        return self_game > other_game

    def __eq__(self, other):
        self_game = self.id_to_game[self["gameId"]]
        other_game = other.id_to_game[other["gameId"]]
        return (self_game == other_game) and (self["time"] == other["time"])

