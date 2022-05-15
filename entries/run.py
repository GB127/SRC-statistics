from code_SRC.composantes import Category, GameCate, Game, System, Time
from tables.leaderboard import LB

class Run:
    def __init__(self, dicto:dict):
        self.gamecat:GameCate = GameCate(Game(dicto["game"], dicto["level"]), Category(dicto["category"], dicto["values"]))
        self.time:Time = Time(dicto["times"]["primary_t"])
        self.system:System = System(dicto["system"]["platform"])

    def __getitem__(self,clé):
        for attribute in [self.gamecat, self.system]:
                if clé in attribute.keys():
                    return attribute[clé]
        return self.__dict__[clé]

    def keys(self):  # TODO : Int only...?
        return list(self.gamecat.keys()) + list(self.system.keys()) + ["time"]

    def __str__(self):
        return f'{self.system}   {self.gamecat}   {self.time}'

class PB(Run):
    def __init__(self, dicto:dict):
        super().__init__(dicto["run"])
        self.leaderboard = LB(dicto["place"], *self.gamecat.ids())

    def __str__(self):
        return super().__str__() + f' {str(self.leaderboard)}'