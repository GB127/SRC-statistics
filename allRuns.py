from tools import run_time, command_select, plot_histo
from generic import table, entry
from api import get_system, get_game, get_category, get_variable, get_level

class Runs(table):
    def __init__(self, data):
        super().__init__()
        print("collecting Runs data")


        for run in data:
            self.data.append(Run(run))

    # PLOTS
    def plot_histo(self):
        plot_histo(sorted([one.time.time for one in self.data]), 
            "Runs", typ="time")

    #OTHERS
    def methods(self):
        metho = super().methods()
        metho["Histo"] = self.plot_histo
        return metho    


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

    levels = {}
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
        def repertoire(lequel, data, requester):
            try:
                return lequel[data]
            except KeyError:
                lequel[data] = requester(data)
                return lequel[data]

        self.IDs = [data["game"], data["category"], data["level"], {}]
        self.system = repertoire(Run.systems, data["system"]["platform"], get_system)

        self.game = clean_gamename(
            repertoire(Run.games, data["game"], get_game))

        self.category = repertoire(Run.categories, data["category"], get_category)


        subcateg = []
        for value, item in data["values"].items():
            tempo = get_variable(value)
            if tempo["is-subcategory"]:
                subcateg.append(tempo["values"]["values"][item]["label"])
                self.IDs[3][value] = item
        if subcateg:
            self.category = f'{self.category} ({",".join(subcateg)})'
        
        self.level = None
        if self.IDs[2]:
            self.level = repertoire(Run.levels, self.IDs[2], get_level)

        self.time = run_time(data["times"]["primary_t"])
