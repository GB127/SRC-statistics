from warnings import warn
from code_SRC.api import api

class Game:
    """Game name & Level names are stored here.
    """
    def __init__(self, game_id:str, level_id:str):
        self.ids = (game_id, level_id)
        self.game, self.release, self.series = api.game(game_id)
        self.level = api.level(level_id) if level_id else ""

    def __str__(self):
        return f'{": ".join((self.game, self.level)):<40}'

    def __eq__(self, other):
        return f'{self.game + self.level:<40}' == f'{other.game + other.level:<40}'

    def keys(self):
        tempo = list(self.__dict__.keys())
        warn("Maybe this will break everything if I don't use copy")
        tempo.remove("ids")
        return tempo

    def __le__(self, other):
        return f'{self.game + self.level:<40}' <= f'{other.game + other.level:<40}'

    def __getitem__(self, key):
        return self.__dict__[key]

class Category:
    """Class that englobes categories and subcategory/variable
    """

    def keys(self):
        tempo = list(self.__dict__.keys())
        warn("Maybe this will break everything if I don't use copy")
        tempo.remove("ids")
        return tempo

    def __init__(self, category_id:str, subcat_ids:dict[str:str]):
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
        strings = f'{self.category} ({",".join(self.subcategory)})'
        return strings

    def __eq__(self, other):
        return str(self) == str(other)

    def __getitem__(self, key):
        return self.__dict__[key]

class GameCate:
    def keys(self):
        return self.game.keys() + self.category.keys()


    def __getitem__(self, clé):
        for attribute in [self.game, self.category]:
            try:
                return attribute[clé]
            except KeyError:
                continue

    def __init__(self,game:Game, category:Category):
        self.game = game
        self.category = category

    def __str__(self):
        return f'{self.game} {self.category}'

    def ids(self):
        return self.game.ids + self.category.ids

class Time:
    def __init__(self, seconds:int):
        self.seconds = seconds

    def __str__(self):
        return f"{int(self.seconds)//3600:>3}:{int(self.seconds) % 3600 // 60:02}:{int(self.seconds) % 3600 % 60 % 60:02}"

    def __eq__(self, other):
        return self.seconds == other.seconds

    def __add__(self, other):
        return Time(self.seconds + other.seconds)

    def __sub__(self, other):
        return Time(self.seconds - other.seconds)

    def __le__(self, other):
        return self.seconds <= other.seconds

    def __truediv__(self, other):
        if isinstance(other, int):
            return Time(self.seconds / other)
        elif isinstance(other, Time):
            return Time(self.seconds / other.seconds)

class System:
    def keys(self):
        return self.__dict__.keys()

    def __init__(self, system_id):
        self.system:str = api.system(system_id)
    
    def __str__(self):
        return "".join([x for x in self.system if x.isupper()])

    def __getitem__(self, key):
        return self.__dict__[key]
