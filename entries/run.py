from code_SRC.composantes import Category, GameCate, Game, System, Time
from tables.leaderboard import LB

class Run:
    def __init__(self, dicto:dict):
        self.gamecat:GameCate = GameCate(Game(dicto["game"], dicto["level"]), Category(dicto["category"], dicto["values"]))
        self.time:Time = Time(dicto["times"]["primary_t"])
        self.system:System = System(dicto["system"]["platform"])


    def __str__(self):
        return f'{self.system}   {self.gamecat}   {self.time}'

class PB(Run):
    def __init__(self, dicto:dict):
        super().__init__(dicto["run"])
        self.leaderboard = LB(dicto["place"], *self.gamecat.ids())

    def __str__(self):
        return super().__str__() + f' {str(self.leaderboard)}'