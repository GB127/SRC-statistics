from tools import run_time
from api import get_game, get_category, get_system, get_variable, get_leaderboard

class Runs:
    def __init__(self,data):
        self.data = []
        for run in data:
            self.data.append(Run(run))
    def __len__(self):
        return len(self.data)
    def total_time(self):
        return sum([x.time for x in self.data])
    def mean_time(self):
        return run_time(self.total_time() / self.__len__())
    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)


class PBs(Runs):
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
        self.WR = None  # Will be updated after PBs during user initialisation.
        self.leaderboard = None

        self.IDs = [data["game"], data["category"], {}]
        self.time = run_time(data["times"]["primary_t"])

        try:
            self.game = Run.games[data["game"]]
        except KeyError:
            Run.games[data["game"]] = get_game(data["game"])
            self.game = Run.games[data["game"]]
        try:
            self.system = Run.systems[data["system"]["platform"]]
        except KeyError:
            Run.systems[data["system"]["platform"]] = get_system(data["system"]["platform"])
            self.system = Run.systems[data["system"]["platform"]]
        try:
            self.category = Run.categories[data["category"]]
        except KeyError:
            Run.categories[data["category"]] = get_category(data["category"])
            self.category = Run.categories[data["category"]]

        self.subcateg = []
        for value, item in data["values"].items():
            tempo = get_variable(value)
            if tempo["is-subcategory"]:
                self.subcateg.append(tempo["values"]["values"][item]["label"])
                self.IDs[2][value] = item


    def full_categ(self):
        if self.subcateg:
            return f'{self.category} ({",".join(self.subcateg)})'
        return f'{self.category}'

    def __str__(self):
        tempo = [
                    f'{self.system[:7]:^7}',
                    f'{self.game[:40]:40}',
                    f'{self.full_categ()[:20]:20}',
                    f'{self.time}']
        return " | ".join(tempo)


class PB(Run):
    def __init__(self, data):
        self.place = data["place"]
        super().__init__(data["run"])
        
        self.leaderboard = get_leaderboard(self.IDs)  # NOTE : In the future I will create a class leaderboards so I can do fancy stuffs with leaderboards.
        self.WR = run_time(self.leaderboard[0][1])

    def __str__(self):
        tempo = [
                    f'{self.system[:7]:^7}',
                    f'{self.game[:40]:40}',
                    f'{self.full_categ()[:20]:20}',
                    f'{self.time}']
        return " | ".join(tempo)