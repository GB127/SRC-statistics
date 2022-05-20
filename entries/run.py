from code_SRC.composantes import Category, GameCate, Game, System, Time
from tables.leaderboard import LB
from statistics import mean, geometric_mean as geomean
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

    def keys(self):
        return list(self.gamecat.keys()) + list(self.system.keys()) + ["time"]


    def __str__(self):
        return f'{self.system}   {self.gamecat}   {self.time}'

class PB(Run):
    def __init__(self, dicto:dict):
        super().__init__(dicto["run"])
        self.leaderboard = LB(dicto["place"], *self.gamecat.ids())
        self.delta = self.time - self.leaderboard["WR"]  #FIXME : self["WR"] instead
        self.perc = self.time / self.leaderboard["WR"]

    def __call__(self):
        while True:
            print(self.str_lb())
            input("Finish? press enter when yes")
            break
    
    
    
    def str_lb(self):
        def mean_index():
            differences = [abs(x - mean(self.leaderboard.ranking)) for x in self.leaderboard.ranking]
            mean_ind = differences.index(min(differences))
            return mean_ind
        def geomean_index():
            differences = [abs(x - geomean(self.leaderboard.ranking)) for x in self.leaderboard.ranking]
            mean_ind = differences.index(min(differences))
            return mean_ind
        string = ""
        for rank, run_time in enumerate(self.leaderboard.ranking, start=1):
            delta = Time(run_time) - self["WR"]
            string += f'{rank:4}   {Time(run_time)} + {delta} ({Time(run_time) / self["WR"]:.2%}) {delta / (rank-1 if rank != 1 else 1)}'
            if self.leaderboard.place == rank:
                string += "<---Runner"
            if rank - 1 == mean_index():
                string += "<---Mean"
            if rank - 1  == geomean_index():
                string += "<---Geomean"
            string += "\n"
        string += f'Sum     {Time(sum(self.leaderboard.ranking))}\n'
        string += f'Mean   {Time(mean(self.leaderboard.ranking))}\n'
        string += f'Geomean{Time(geomean(self.leaderboard.ranking))}'
        return string



    def keys(self):
        return super().keys() + ["delta", "perc", "perc_lb", "leaderboard"]


    def __getitem__(self, clé):
        if clé == "WR":
            return self.leaderboard[0]
        elif clé == "leaderboard":
            return self.leaderboard
        elif clé == "perc_lb":
            return (len(self.leaderboard) - self.leaderboard.place)/len(self.leaderboard)
        return super().__getitem__(clé)
    def __str__(self):
        return f'{super().__str__()} +{str(self.delta).lstrip()} ({self.perc:.2%})  {str(self.leaderboard)}'