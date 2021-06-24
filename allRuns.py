from tools import run_time, command_select, plot_histo
from generic import table, entry
from api import get_system, get_game, get_category, get_variable, get_level

class Runs(table):
    def __init__(self, data):
        super().__init__()
        print("collecting Runs data")


        for run in data:
            self.data.append(Run(run))

    # STRING RELATED
    def __str__(self):
        return f'{len(self)} runs ({sum([x.time for x in self.data]).days()})'


    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("IDs")
        types.remove("level")
        return types

    def foot(self):
        total_time = sum([x.time for x in self.data])

        string1 = f"{'-' * 72}\n" 
        string2 = f"{'Total |':>60}{total_time:>10}\n"
        string3 = f"{'Average |':>60}{run_time(total_time/ len(self)):>10}\n"
        return string1 + string2 + string3


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

    table_size = [1, 17, 13, 6]
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
        self.IDs = [data["game"], data["category"], data["level"], {}]

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
                self.IDs[3][value] = item
        if subcateg:
            self.category = f'{self.category} ({",".join(subcateg)})'
        
        if self.IDs[2]:
            self.level = get_level(self.IDs[2])
        else:
            self.level = None

        self.time = run_time(data["times"]["primary_t"])

    def __str__(self):
        tempo = [
                    f'{self.system[:6]:^6}',
                    f'{self.game[:20]:20}',
                    f'{self.category[:20]:20}',
                    f'{self.time:>9}']
        return " | ".join([str(x) for x in tempo]) + " |"

    def sortable(self):
        tempo = list(self.__dict__)
        tempo.remove("IDs")
        return tempo

