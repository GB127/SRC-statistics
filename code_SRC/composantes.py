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
