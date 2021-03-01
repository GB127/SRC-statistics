from generic import entry
from api import get_game, get_category, get_system, get_variable, get_leaderboard
from tools import run_time, command_select

class Run(entry):
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

    sorter = "game"

    def __init__(self, data):
        def clean_gamename(name):
            if "The Legend of Zelda" in name:
                return name[14:]
            if name == "Ocarina of Time Category Extensions":
                return "Zelda: Ocarina of Time"
            if name == "Super Mario 64 Category Extensions":
                return "Super Mario 64"

            else: return name
        self.IDs = [data["game"], data["category"], {}]

        try:
            self.system = Run.systems[data["system"]["platform"]]
        except KeyError:
            Run.systems[data["system"]["platform"]] = get_system(data["system"]["platform"])
            self.system = Run.systems[data["system"]["platform"]]

        try:
            self.game = Run.games[data["game"]]
        except KeyError:
            Run.games[data["game"]] = clean_gamename(get_game(data["game"]))
            self.game = Run.games[data["game"]]
        try:
            self.category = Run.categories[data["category"]]
        except KeyError:
            Run.categories[data["category"]] = get_category(data["category"])
            self.category = Run.categories[data["category"]]

        subcateg = []
        for value, item in data["values"].items():
            tempo = get_variable(value)
            if tempo["is-subcategory"]:
                subcateg.append(tempo["values"]["values"][item]["label"])
                self.IDs[2][value] = item
        if subcateg:
            self.category = f'{self.category} ({",".join(subcateg)})'
        
        self.time = run_time(data["times"]["primary_t"])

    def __str__(self):
        tempo = [
                    f'{self.system[:6]:^6}',
                    f'{self.game[:20]:20}',
                    f'{self.category[:20]:20}',
                    f'{self.time:>9}']
        return " | ".join([str(x) for x in tempo]) + " |"

    def table_size(self):  # Idea : Global variable so it's not a method.
        return [1, 17, 13, 6]

class Save(entry):
    def __init__(self, PB, Runs):
        self.system = PB.system
        self.game = PB.game
        self.category = PB.category
        self.runs = []
        for run in Runs:
            if run.game == self.game and run.category == self.category:
                self.runs.append(run)
        self.X = len(self.runs)

        Run.sorter = "time"
        self.runs.sort()
        self.first = self.runs[-1].time
        self.PB = PB.time
        self.save = self.first - self.PB
        self.perc1st = round(self.save/self.first * 100, 2)

    def __str__(self):
        return " | ".join([
                            f'{self.system[:6]:^6}',
                            f'{self.game[:20]:20}',
                            f'{self.category[:20]:20}',
                            f'{self.X:^3}',
                            f'{self.first:>9}',
                            f'{self.PB:>9}' + f' (-{self.save})',
                            f'(-{self.perc1st:6}%)'
                        ]) + "|"

    def table_size(self):  # Idea : Global variable so it's not a method.
        return [1, 17, 13, 3, 5, 19, 3]


class PB(Run):
    def __init__(self, data):
        super().__init__(data["run"])
        self.leaderboard = get_leaderboard(self.IDs)  # NOTE : In the future I will create a class leaderboards so I can do fancy stuffs with leaderboards.
        self.WR = run_time(self.leaderboard[0][1])
        self.delta_WR = self.time - self.WR
        self.perc_WR = round((self.time) / self.WR * 100, 2)
        self.place = data["place"]

    def __str__(self):
        return super().__str__() + " | ".join([
                                    f'+ {self.delta_WR:<8}',
                                    f'{str(self.perc_WR) + " %":>9}',
                                    f"{f'{self.place}/{len(self.leaderboard)}':9}"]) + "|"

    def table_size(self):
        return super().table_size() + [2, 3, 4]
