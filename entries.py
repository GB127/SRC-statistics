from api import  get_leaderboard, get_serie, get_game_variables

def time_str(duration:[int, float]):
    no_decimal = int(duration)
    return f"{no_decimal//3600}:{no_decimal% 3600 // 60:02}:{no_decimal % 3600 % 60 % 60:02}"


class Entry:
    games = {}
    systems = {}
    series = {}
    categories = {}
    subcategories = {}
    release = {}
    @staticmethod
    def update_game(infos):
        all_ids = (x["id"] for x in infos)
        all_game_name = (x["names"]["international"] for x in infos)
        ids_games = set(zip(all_ids, all_game_name))

        for id, gamename in ids_games:
            Entry.games[id] = gamename

    @staticmethod
    def update_system(infos):
        all_ids = (x["id"] for x in infos)
        all_names = (x["name"] for x in infos)
        ids_system = set(zip(all_ids, all_names))

        for id, system in ids_system:
            Entry.systems[id] = system
    
    @staticmethod
    def update_category(infos):
        all_ids = list(x["data"]["id"] for x in infos)  # works
        all_names = list(x["data"]["name"] for x in infos)  # works
        ids_category = set(zip(all_ids, all_names))

        for id, category in ids_category:
            Entry.categories[id] = category

    @staticmethod
    def update_release(infos):
        all_ids = [x["id"] for x in infos]
        all_release_years = [x["released"] for x in infos]
        ids_years = set(zip(all_ids, all_release_years))
        for id, year in ids_years:
            Entry.release[id] = year

    def update_subcategory(games):
        for game_id in games:
            all_variables = get_game_variables(game_id)
            for variable in all_variables:
                if Entry.subcategories.get(variable["id"]): 
                    # Just a failsafe check just to be sure.
                    raise BaseException(f"Something is wrong \n{Entry.subcategories} already has {variable['id']}\n Perhaps a game has a exact same variable id?")
                Entry.subcategories[variable["id"]] = {}
                if variable["is-subcategory"]:
                    for label_id, label_data in variable["values"]["values"].items():
                        Entry.subcategories[variable["id"]][label_id] = label_data["label"]


    def update_series(infos):
        for link in infos:
            data = get_serie(link)
            Entry.series[link] = data["names"]["international"]

class Run(Entry):
    sorting_mode = "game"
    def __init__(self, data:dict):
        def build_category():
            def build_subcategory():
                all_subcategory = []
                for subcategory in data["values"].items():
                    try:
                        all_subcategory.append(self.subcategories[subcategory[0]][subcategory[1]])
                    except KeyError:
                        continue
                return all_subcategory
            self.category = f'{self.categories[data["category"]]}' 
            if build_subcategory():
                self.category += f' ({", ".join(build_subcategory())})'
        self.game = self.games[data["game"]]  # Works
        build_category()
        self.time = data["times"]["primary_t"]  # Works
        self.emu = data["system"]["emulated"]  # Works
        self.system = self.systems[data["system"]["platform"]]  # Works
        #TODO : level
        #TODO : Region

    def __str__(self):
        return f'{self.system[:20]:20} {self.game[:30]:30} {self.category[:20]:20} {time_str(self.time)}'

    def __lt__(self, other):
        if self.__dict__[self.sorting_mode] == other.__dict__[self.sorting_mode]:
            if self.__dict__["game"] == other.__dict__["game"]:
                return self.__dict__["category"] < other.__dict__["category"]
            return self.__dict__["game"] < other.__dict__["game"]
        return self.__dict__[self.sorting_mode] < other.__dict__[self.sorting_mode]

class PB(Run):
    def __init__(self, data:dict):
        def build_subcategory():
            all_subcategory = []
            for subcategory in data["run"]["values"].items():
                try:
                    all_subcategory.append((subcategory[0],subcategory[1]))
                except KeyError:
                    continue
            return all_subcategory

        #TODO : leaderboard / WR stuffs
        self.place = data["place"]
        self.LB = get_leaderboard(
            data["run"]["game"],
            data["run"]["level"],
            data["run"]["category"],
            build_subcategory()  # FIXME
        )

        super().__init__(data["run"])
        self.delta = self.time - self.LB[0]
        self.perc = self.time / self.LB[0]

    def __str__(self):
        return super().__str__() + f' +{time_str(self.delta)} ({self.perc:.2%})      {self.place} / {len(self.LB)}'

