from utils import time_str

class Entry:
    games = {}
    systems = {}
    categories = {}

    def __init__(self, game, time, category):
        self.game = game
        self.category = category
        self.time = time


    def __str__(self):
        game_str = 30
        cat_str = 20
        return (f'{self["game"][:game_str]:{game_str}}|{self["category"][:cat_str]:{cat_str}}|{self["time"]:>10}|')

    def __getitem__(self, key):
        if key == "game":
            return self.games[self.game]
        elif key == "time":
            return time_str(self.time)
        elif key == "category":
            return self.categories[self.category]
        raise NotImplementedError("FIXME LATER")

    @staticmethod
    def update_games(infos):
        Entry.games = infos

    @staticmethod
    def update_categories(infos):
        Entry.categories = infos


class Run(Entry):
    pass

class PB(Entry):
    pass