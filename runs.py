from tools import run_time
from api import get_game, get_category

class PBs:
    def __init__(self, data):
        self.data = []
        for pb in data:
            self.data.append(PB(pb))
        for pb in self.data:
            print(pb)

class PB:
    def __init__(self, data):
        self.data = data
        self.place = self.data["place"]

        data_1 = self.data["run"]
        self.time = run_time(data_1["times"]["primary_t"])
        
        self.game = get_game(data_1["game"])
        self.category = get_category(data_1["category"])

    def __str__(self):
        return f'{self.game}{self.category}{self.time}{self.place}'