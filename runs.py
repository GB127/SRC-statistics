from tools import run_time
from api import get_game, get_category, get_system

class Runs:
    def __init__(self,data):
        self.data = []
        for run in data:
            self.data.append(Run(run))


class PBs:
    def __init__(self, data):
        self.data = []
        for pb in data:
            self.data.append(PB(pb))

class Run:
    games = {}
    categories = {}
    systems = {
        None : "PC",
        "n5683oev" : "GB",
        "gde3g9k1" : "GBC",
        "3167d6q2" : "GBA",
        "w89rwelk" : "N64",
        "jm95z9ol" : "NES",
        "3167jd6q" : "SGB",
        "83exk6l5" : "SNES",
        "4p9z06rn" : "GC",
        "mr6k0ezw" : "S.GEN",
        "nzelreqp" : "WII VC",
        "3167jd6q" : "SGB",
        "n5e147e2" : "SGB2",
        "wxeod9rn" : "PS",
        "n5e17e27" : "PS2",
        "mx6pwe3g" : "PS3",
        "nzelkr6q" : "PS4",
        }


    def __init__(self, data):
        self.time = run_time(data["times"]["primary_t"])

        try:
            self.game = Run.games[data["game"]]
            self.system = Run.systems[data["system"]["platform"]]
        except KeyError:
            Run.games[data["game"]] = get_game(data["game"])
            self.game = Run.games[data["game"]]
            Run.systems[data["system"]["platform"]] = get_system(data["system"]["platform"])
            self.system = Run.systems[data["system"]["platform"]]

        try:
            self.category = Run.categories[data["category"]]
        except KeyError:
            Run.categories[data["category"]] = get_category(data["category"])
            self.category = Run.categories[data["category"]]



class PB(Run):
    def __init__(self, data):
        self.place = data["place"]
        super().__init__(data["run"])

    def __str__(self):
        return f'{self.game}{self.system}{self.category}{self.time}{self.place}'