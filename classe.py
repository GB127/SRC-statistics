import datetime
import isodate
import matplotlib.pyplot as plot
import numpy
from api import *
from tools import *

class user:
    def __init__(self, username):
        """
            Object of a Speedrun.com user. It tracks username, ID, runs and PBs

            Args:
                username (str) : Username on speedrun.com

            Attributes created:
                self.username (str) : Username
                self.ID (str) : ID of the user
                self.runs (list) : List of runs
                self.PBs (list) : List of PBs
        """
        print("Fetching data...")


        self.username = username
        self.ID = get_userID(self.username)
        self.runs, self.PBs = [], []


        # PB related
        for pb in get_PBs(self.ID): 
            if pb["run"]["level"] is None and pb["run"]["times"]["primary_t"] > 180:
                self.PBs.append(PB(pb))
            else: pass
        self.total_PB()
        self.total_WR()

        # Runs related:
        for run in get_runs(self.ID):
            if run["level"] is None and run["times"]["primary_t"] > 180:
                self.runs.append(Run(run))
            else: pass




        print("user initialized!")


    def __str__(self):
        return f'{self.username}, {len(self.runs)} runs, {len(self.PBs)} PBs'


    def total_PB(self):
        tempo = []
        for PB in self.PBs:
            tempo.append(PB.time)
        self.total_PB = sum(tempo)


    def total_WR(self):
        tempo = []
        for PB in self.PBs:
            tempo.append(PB.WR)
        self.total_WR = sum(tempo)


    def table_PBs(self):
        """Print a table by printing all PBs
        """
        print("-"*120)
        print(f"| # |{'Sys':^6}| {'Game':^30}| {'Category':^15} | {'Time':^14}|      + \u0394WR     |{'%WR':^10}| {'  Rank      (^%)':20}")
        print("-"*120)
        self.PBs.sort()
        for no, PB in enumerate(self.PBs): print(f'{no+1:3} {PB}')
        print("-"*122)
        print(f'{"Total :":>58}| {str_time(self.total_PB)[:17]:17}| + {str_time(self.total_PB - self.total_WR)[:13]:20}|----------|')
        print(f'{"Average :":>58}| {str_time(self.total_PB/len(self.PBs))[:17]:17}| + {str_time((self.total_PB - self.total_WR)/len(self.PBs))[:13]:20}| {str(round(self.total_PB/self.total_WR * 100,2))[:6]:6} % |')

    def runs_PB(self, PB):
        toreturn = []
        for run in self.runs:
            if run.gameID == PB.gameID and run.categID == PB.categID:
                toreturn.append(run)
        return toreturn


class Run:
    sort = "time"

    def __init__(self, data):
        """
            Args:
                data ([json]): data from requests to speedrun.com

            Attributes:
                self.system : System the run is on
                self.emulated : True if emulated, False if not emulated
                self.ID : ID of the run
                self.gameID : ID of the game ran
                self.categID : ID of the category ran
                self.time : duration of the run
        """
        self.system = get_system(data["system"]["platform"])
        self.emulated = True if data["system"]["emulated"] else False
        self.ID = data["id"]
        self.gameID = data["game"]
        self.categID = data["category"]
        self.vari = data["values"]
        self.time = data["times"]["primary_t"]


    def __str__(self):
        return f'{self.system[:6]:^6}| {get_game(self.gameID)[:30]:30} | {get_category(self.categID)[:15]:15} | {datetime.timedelta(seconds=self.time)}'


    def __lt__(self, other):
        if get_game(self.gameID) != get_game(other.gameID):
            return get_game(self.gameID) < get_game(other.gameID)
        elif get_category(self.categID) != get_category(other.categID):
            return get_category(self.categID) < get_category(other.categID)
        else:
            return self.time < other.time

class PB(Run):
    sort = "%WR"
    def __init__(self, data):
        """
            NOTES:
                Some extra infos not eally related to the PB 
                are stored because of the maths I want to do.

            Attributes:
                self.place : Rank of the PB
                self.lenrank : Length of the leaderboard
                self.WR : WR of the said run
        """
        super().__init__(data["run"])
        self.place = data["place"]
        self.lenrank = get_len_leaderboard(self.gameID, self.categID, self.vari)
        self.perclenrank = round(100 * (self.lenrank - self.place) / self.lenrank, 2)
        self.WR = get_WR(self.gameID, self.categID, self.vari)
        self.delta = self.time - self.WR
        self.percWR = round((self.time * 100/self.WR), 2)


    def __str__(self):
        def str_game(self):
            return f'|{self.system[:6]:^6}| {get_game(self.gameID)[:30]:30}| {get_category(self.categID)[:15]:15}'
        def str_rank(self):
            calculation = f'{self.place}/{self.lenrank}'
            calculation2 = f'({str(self.perclenrank):^5} %)'
            return str(f'{calculation:^9} {calculation2}')
        def str_times(self):
            return f'{str_time(self.time)[:13]:13} | + {str_time(self.delta)[:13]:13}| {self.percWR:^6} %'
        return f'{str_game(self)} | {str_times(self)} | {str_rank(self)}'


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

if __name__ == "__main__":
    pass