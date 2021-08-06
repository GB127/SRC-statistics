from tools import run_time, command_select
from generic import table, entry
from api import get_system, get_game, get_category, get_variable, get_level
import matplotlib.pyplot as plot



class Runs(table):
    def __init__(self, data=None):
        super().__init__()

        if data:
            for run in data:
                self.data.append(Run(run))

    def histo_times(self):
        plot.title(f"{self.__class__.__name__}")
        data = [one.time.time for one in self.data]
        plot.hist(data, bins=10, range=(min(data), max(data)))
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.xlim(left=min(data), right=max(data))
        plot.show()




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
    subcategories = {}
    sorter = "game"

    def __init__(self, data):
        def clean_gamename(name):
            if "The Legend of Zelda" in name:
                return name[14:]
            if name[-19:] == "Category Extensions":
                return name[:-20]
            else: return name
        def repertoire(lequel, data, requester):
            try:
                return lequel[data]
            except KeyError:
                lequel[data] = requester(data)
                return lequel[data]

        self.IDs = [data["game"], data["category"], data["level"], {}]
        self.system = repertoire(Run.systems, data["system"]["platform"], get_system)

        self.game = clean_gamename(repertoire(Run.games, data["game"], get_game))
        self.category = repertoire(Run.categories, data["category"], get_category)


        subcateg = []
        for value, item in data["values"].items():
            tempo = repertoire(Run.subcategories, value, get_variable)
            if tempo["is-subcategory"]:
                subcateg.append(tempo["values"]["values"][item]["label"])
                self.IDs[3][value] = item
        if subcateg:
            self.category = f'{self.category} ({",".join(subcateg)})'
        
        self.time = run_time(data["times"]["primary_t"])




class Run_level(Run):
    levels = {}

    def __init__(self, data):
        super().__init__(data)
        try:
            self.level = Run_level.levels[self.IDs[2]]
        except KeyError:
            Run_level.levels[self.IDs[2]] = get_level(self.IDs[2])
            self.level = Run_level.levels[self.IDs[2]]

    def __str__(self):
        tempo = super().__str__()
        tempo2 = tempo.split("|")
        tempo2.insert(2, tempo2[-1])
        return "|".join(tempo2[:-1])

class Runs_levels(Runs):
    def __init__(self, data=None):
        self.data = []
        if data:
            for run in data:
                self.data.append(Run_level(run))