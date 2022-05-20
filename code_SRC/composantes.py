from code_SRC.api import api


class Game:
    def __init__(self, game_id: str, level_id: str):
        """Class that handle the game, level and the release year of a game."""
        def game_name_cleanup():
            """Removes unwanted elements from the names.
                """
            for unwanted in [" Category Extensions", "The Legend of Zelda: "]:
                self.game = self.game.replace(unwanted, "")


        self.ids = (game_id, level_id)
        self.game, self.release, self.series = api.game(game_id)
        self.level = api.level(level_id) if level_id else ""
        self.release = str(self.release)
        game_name_cleanup()

    def __str__(self):
        string = self.game
        if self.level:
            string += f": {self.level}"
        return string

    def __eq__(self, other):
        return f"{self.game + self.level:<40}" == f"{other.game + other.level:<40}"

    def __le__(self, other):
        return f"{self.game + self.level:<40}" <= f"{other.game + other.level:<40}"

    def __getitem__(self, key):
        return self.__dict__[key]

    def keys(self) -> list:
        """Return all the keys that can be used to retrieve game infos.
            Uses dict.keys() to eases adding functionnalities. 
            Docstring needs to be updated manually.
        
            Returns: ["game", "release", "level"]
            """
        tempo = list(self.__dict__.keys())
        tempo.remove("ids")
        return tempo


class Category:
    def __init__(self, category_id: str, subcat_ids: dict[str:str]):
        """Class that handles the category & the subcategory."""

        def subcategories():
            self.subcategory = []
            ids = []
            for option in subcat_ids.items():
                tempo = api.subcategory(option)
                if tempo:
                    ids.append(option)
                    self.subcategory += [tempo]
            return ids

        self.category = api.category(category_id)
        self.ids = (category_id, subcategories())

    def __str__(self):
        strings = f"{self.category}"
        if self.subcategory:
            strings += f' ({",".join(self.subcategory)})'
        return strings

    def __eq__(self, other):
        return str(self) == str(other)

    def __getitem__(self, key):
        return self.__dict__[key]


class GameCate:
    def __init__(self, game: Game, category: Category):
        """Handles the Game and the Category. 
            Because of the fact that a category can share the same name 
            across different games, this classes handles this part."""
        self.game = game
        self.category = category

    def __str__(self):
        return f"{str(self.game)[:30]:<30}   {str(self.category)[:20]:<20}"

    def ids(self) -> list:
        """Returns all the ids necessary for leaderboard requests.
            Returns: ["game_id", "level_id", "category_id", "subcategory_ids"]
                NOTE: "subcategory_id is a dictionnary {"field":"subcategory selected"}
            """
        return self.game.ids + self.category.ids

    def keys(self):
        """Return all the keys that can be used to retrieve game 
            or/and category infos. Uses dict.keys() to eases 
            adding functionnalities.             
            Returns: ["game", "release", "level", "category]

            Docstring needs to be updated manually.
            """
        return list(self.game.keys()) + ["category"]

    def __getitem__(self, clé):
        if clé == "category":
            return f"{self.game} {self.category}"
        for attribute in [self.game, self.category]:
            if clé in attribute.__dict__:
                return attribute[clé]


class Time:
    def __init__(self, total_seconds: int):
        """Class created mainly to handle the stringing of the times. 
            Stores the total seconds internally as int."""
        self.seconds:[int,float] = total_seconds

    def __float__(self):
        return float(self.seconds)

    def __str__(self):
        return f"{int(self.seconds)//3600:>3}:{int(self.seconds) % 3600 // 60:02}:{int(self.seconds) % 3600 % 60 % 60:02}"

    def __eq__(self, other):
        return self.seconds == other.seconds

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, int):
            return Time(self.seconds + other)
        return Time(self.seconds + other.seconds)

    def __sub__(self, other):
        return Time(self.seconds - other.seconds)

    def __le__(self, other):
        return self.seconds <= other.seconds

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Time(self.seconds / other)
        elif isinstance(other, Time):
            return self.seconds / other.seconds


class System:
    def __init__(self, system_id):
        self.system: str = api.system(system_id)

    def __str__(self):
        if any([x.isupper() for x in self.system]):
            return f'{"".join([x for x in self.system if x.isupper()])[:3]:^3}'
        return f'{self.system[:3]:^3}'

    def keys(self) -> list[str]:
        """Returns retrievable informations about system.
            
            Returns: ["system"]
            """
        return self.__dict__.keys()

    def __getitem__(self, key):
        return self.__dict__[key]


