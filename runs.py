from tools import run_time
from api import *

class Run:
    sort = "time"

    def __init__(self, data):
        """
            Args:
                data ([json]): data from requests to speedrun.com

            Attributes:
                self.categID (string) : ID of the category ran
                self.emulated (bool): True if emulated, False if not emulated
                self.gameID (string): ID of the game ran
                self.ID (string): ID of the run
                self.system (string): System the run is on
                self.time (int): duration of the run, in seconds
                FIXME self.vari : "subcategories" of the category.
        """
        self.ID = data["id"]
        self.time = run_time(data["times"]["primary_t"])

        self.gameID = data["game"]
        self.game = get_game(self.gameID)

        self.categID = data["category"]
        self.categ = get_category(self.categID)
        self.vari = data["values"]

        self.system = get_system(data["system"]["platform"])
        self.emulated = data["system"]["emulated"]
        
    def __str__(self):
        """ Format: System|Game|Category|Time
            """
        return f'{self.system[:6]:^6}| {self.game[:30]:30} | {self.categ[:15]:15} | {self.time}'

    def __lt__(self, other):
        if get_game(self.gameID) != get_game(other.gameID):
            return get_game(self.gameID) <= get_game(other.gameID)
        elif get_category(self.categID) != get_category(other.categID):
            return get_category(self.categID) <= get_category(other.categID)
        else:
            return self.time <= other.time

class PB(Run):
    sort = "game"
    def __init__(self, data):
        """
            NOTES:
                Some extra infos not eally related to the PB 
                are stored because of the maths I want to do.

            New Attributes:
                self.delta (int): Time difference of PB compared to WR, in seconds. 
                self.place (int): Rank of the PB
                self.lenrank (int): Length of the leaderboard
                self.perclenrank (int): Percentage of people you beat in the leaderboard.
                    Note : If you are the only runner on the leaderboard, you will
                    have 0% even if you have the WR! This is because you don't beat anyone.
                    Will never be 100% because it doesn't count you : you ar emerely the threshold
                    for the maths.
                self.percWR (int): % of the WR. 100% means it's the WR. 200% means the time is exactly double
                    the WR
                self.WR (int): WR of the said run, in seconds)
        """
        super().__init__(data["run"])
        self.place = data["place"]
        self.lenrank = get_len_leaderboard(self.gameID, self.categID, self.vari)
        self.perclenrank = round(100 * (self.lenrank - self.place) / self.lenrank, 2)
        self.WR = run_time(get_WR(self.gameID, self.categID, self.vari))
        self.delta = self.time - self.WR
        self.percWR = round((self.time * 100/self.WR), 2)


    def __str__(self):  # FIXME : Documentate this
        def str_game(self):
            return f'|{self.system[:6]:^6}| {self.game[:30]:30}| {self.categ[:15]:15}'
        def str_rank(self):
            calculation = f'{self.place}/{self.lenrank}'
            calculation2 = f'({self.perclenrank:^5} %)'
            return str(f'{calculation:^9} {calculation2}')
        def str_time(self):
            return f'{self.time:8} | + {self.delta:8}| {self.percWR:^6} %'
        return f'{str_game(self)} | {str(str_time(self))} | {str_rank(self)}'


    def __lt__(self, other):
        if PB.sort == "game":
            return get_game(self.gameID) < get_game(other.gameID)
        elif PB.sort == "system":
            return self.system < other.system
        elif PB.sort == "time":
            return self.time < other.time
        elif PB.sort == "delta":
            return self.delta < other.delta
        elif PB.sort == "%WR":
            return self.percWR < other.percWR
        elif PB.sort == "%LB":
            return self.perclenrank > other.perclenrank



class leaderboard:
    def __init__(self):
        pass


    def plot_leaderboard(leaderboards):

        for year in leaderboards.keys():
            if len(leaderboards[year]) == 1:
                plot.plot([time[0] for time in leaderboards[year]], [rank[1] for rank in leaderboards[year]], label=year, marker="*")
            else:
                plot.plot([time[0] for time in leaderboards[year]], [rank[1] for rank in leaderboards[year]], label=year)

        plot.ylabel("Time")
        plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])

        plot.xlabel("Rank")
        ax = plot.gca()
        ax.set_xlim(ax.get_xlim()[::-1])
        


        plot.show()

