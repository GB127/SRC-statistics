from api import get_game, get_category, get_system, get_variable, get_leaderboard
from tools import run_time

class Run:
    data = [f'{"#":^3}',
                f'{"System":^7}',
                f'{"Game":20}',
                f'{"Category":20}',
                f'{"Time":^9}',
                f'{"deltaWR"}']


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
        def clean_gamename(name):
            if "The Legend of Zelda" in name:
                return name[14:]
            if name == "Ocarina of Time Category Extensions":
                return "Zelda: Ocarina of Time"
            if name == "Super Mario 64 Category Extensions":
                return "Super Mario 64"

            else: return name


        self.IDs = [data["game"], data["category"], {}]
        self.time = run_time(data["times"]["primary_t"])

        try:
            self.game = Run.games[data["game"]]
        except KeyError:
            Run.games[data["game"]] = clean_gamename(get_game(data["game"]))
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


    def __str__(self):
        def full_categ():
            if self.subcateg:
                return f'{self.category} ({",".join(self.subcateg)})'
            return f'{self.category}'
        
        tempo = [
                    f'{self.system[:7]:^7}',
                    f'{self.game[:20]:20}',
                    f'{full_categ()[:20]:20}',
                    f'{self.time:>9}']
        return " | ".join(tempo)


    def delta_WR(self):
        return self.time - self.WR
    def perc_WR(self):
        return round((self.time) / self.WR * 100, 2)



class PB(Run):
    def __init__(self, data):
        self.place = data["place"]
        super().__init__(data["run"])
        
        try:  # Don't understand why this doesn't work sometimes, so I have to just keep them out of my datas
            self.leaderboard = get_leaderboard(self.IDs)  # NOTE : In the future I will create a class leaderboards so I can do fancy stuffs with leaderboards.
            self.WR = run_time(self.leaderboard[0][1])
        except BaseException:
            self.leaderboard = False
            


    def __str__(self):
        return super().__str__() + " | " + " | ".join([f'+ {self.delta_WR():<8}',
                                    f'{str(self.perc_WR()) + " %":>9}'])