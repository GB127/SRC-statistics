from api import get_game, get_category, get_system, get_variable, get_leaderboard
from tools import run_time, command_select

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

    sorter = "game"

    def change_sort(self):
        options = list(self.__dict__)
        options.pop(0)
        for no, one in enumerate(options):
            print(no + 1, one)
        self.__class__.sorter = command_select(options)

    def __lt__(self, other):
        if self.__dict__[self.sorter] != other.__dict__[self.sorter]:
            return self.__dict__[self.sorter] < other.__dict__[self.sorter]
        return self.category < other.category

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
        return " | ".join([str(x) for x in tempo])


class PB(Run):
    def __init__(self, data):
        super().__init__(data["run"])
        try:  # Don't understand why this doesn't work sometimes, so I have to just keep them out of my datas
            self.leaderboard = get_leaderboard(self.IDs)  # NOTE : In the future I will create a class leaderboards so I can do fancy stuffs with leaderboards.
            self.WR = run_time(self.leaderboard[0][1])
        except BaseException:
            self.leaderboard = False
        self.delta_WR = self.time - self.WR
        self.perc_WR = round((self.time) / self.WR * 100, 2)
        self.place = data["place"]


    def __str__(self):
        return super().__str__() + " | " + " | ".join([
                                    f'+ {self.delta_WR:<8}',
                                    f'{str(self.perc_WR) + " %":>9}',
                                    f"{self.place}/{len(self.leaderboard)}"])