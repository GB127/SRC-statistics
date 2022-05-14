from code_SRC.api import api

class Game:
    """Game name & Level names are stored here.
    """
    def __init__(self, game_id:str, level_id:str):
        self.ids = (game_id, level_id)
        self.game, self.release, self.series = api.game(game_id)
        self.level = api.level(level_id)

    def __str__(self):
        return f'{": ".join((self.game, self.level)):<40}'

    def __eq__(self, other):
        return f'{self.game + self.level:<40}' == f'{other.game + other.level:<40}'

    def __le__(self, other):
        return f'{self.game + self.level:<40}' <= f'{other.game + other.level:<40}'

class Category:
    """Class that englobes categories and subcategory/variable
    """
    def __init__(self, category_id:str):
        self.category = api.category(category_id)
        self.ids = (category_id)
    def __str__(self):
        strings = [f'{self.category}']
        return "   ".join(strings)

    def __eq__(self, other):
        return str(self) == str(other)

class GameCate:
    def __init__(self,game:Game, category:Category):
        self.game = game
        self.category = category

    def __str__(self):
        return f'{self.game} {self.category}'

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
    def __init__(self, system_id):
        self.name:str = api.system(system_id)
    
    def __str__(self):
        return "".join([x for x in self.name if x.isupper()])