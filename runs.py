from tools import run_time
from api import get_game, get_category

class PBs:
    def __init__(self, data):
        self.data = []
        for pb in data:
            self.data.append(PB(pb))
        for pb in self.data:
            print(pb)

class Run:
    games = {}
    def __init__(self, data):
        self.time = run_time(data["times"]["primary_t"])
        
        self.game = get_game(data["game"])
        self.category = get_category(data["category"])

class PB(Run):
    def __init__(self, data):
        self.place = data["place"]
        super().__init__(data["run"])

    def __str__(self):
        return f'{self.game}{self.category}{self.time}{self.place}'