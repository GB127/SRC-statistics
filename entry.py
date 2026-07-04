from parameters import max_str_game
from utils import time_str

class Entry(dict):
    games = {}
    systems = {}
    categories = {}


    def __init__(self, data):
        assert self.games, "Game db must be updated first."

        # FIXME : Don't do it if absent.
        unwanted = ["comment", "submittedById", "reason", "dateSubmitted",
                    "hasSplits", "dateVerified", "verifiedById",
                    "enforceMs", "timeWithLoads", "video", "verified", "date",
                    "playerIds", "estimated", "issues", "videoState", "id", "igt", "emulator", "regionId", "orphaned"]
        for one in unwanted:
            del data[one]
        super().__init__(data)

    def __str__(self):
        game_str_size = max([len(x) for x in self.games.values()])
        final_game_str = min(max_str_game, game_str_size)

        game =  f'{self.games[self["gameId"]][:final_game_str]:{final_game_str}}'

        system_str_size = max([len(x) for x in self.systems.values()]) +1
        system =  f'{self.systems[self["platformId"]]:^{system_str_size}}'

        cat_str_size = max([len(x) for x in self.categories.values()])
        category =  f'{self.categories[self["categoryId"]]:^{cat_str_size}}'

        return "|" + "|".join([system, game,  category]) + "|"

    def __gt__(self, other):
        # FIXME : add category
        self_game = self.games[self["gameId"]]
        other_game = other.games[other["gameId"]]

        if self_game == other_game:
            return self["time"] > other["time"]
        return self_game > other_game

    def __eq__(self, other):
        # FIXME : add category
        self_game = self.games[self["gameId"]]
        other_game = other.games[other["gameId"]]
        return (self_game == other_game) and (self["time"] == other["time"])

    @staticmethod
    def update_game_db(data):
        test = data["games"]
        for one_game in test:
            id = one_game["id"]
            name = one_game["name"]
            Entry.games[id] = name

    @staticmethod
    def update_system_db(data):
        test = data["platforms"]
        for one in test:
            id = one["id"]
            system = one["url"]  # url is the acronym from what I see.
            Entry.systems[id] = system

    @staticmethod
    def update_cat_db(data):
        test = data["categories"]
        for one in test:
            id = one["id"]
            category = one["name"]
            Entry.categories[id] = category


class Run(Entry):
    def __str__(self):
        return super().__str__() + f'{time_str(self["time"]):>9}|'


class PB(Entry):
    pass


if __name__ == "__main__":
    from Speedrunner import Speedrunner
    test = Speedrunner()

    print(test.runs)