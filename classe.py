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
        self.username = username
        print("initializing data...")
        self.ID = get_userID(self.username)
        self.runs, self.PBs = [], []
        for run in get_runs(self.ID): self.runs.append(Run(run))
        for pb in get_PBs(self.ID): 
            if pb["run"]["level"] is None:
                self.PBs.append(PB(pb))
            else: pass
        print("user initialized!")

    def listPBs(self):  # TODO : Change name
        """Print a table by printing all PBs
        """
        print(f"|{'Sys':^6}| {'Game':^30}| {'Category':^15} | {'  Rank      (^%)':20}| {'Time':^13}| + \u0394WR")
        print("-"*120)
        for PB in self.PBs: print(PB)
class Run:
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
        self.system = data["system"]["platform"]
        self.emulated = True if data["system"]["emulated"] else False
        self.ID = data["id"]
        self.gameID = data["game"]
        self.categID = data["category"]
        self.time = isodate.parse_duration(data["times"]["primary"]).total_seconds()
    def __str__(self):
        return f'{get_game(self.gameID)} - {get_category(self.categID)} - {datetime.timedelta(seconds=self.time)}'

class PB(Run):
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
        self.lenrank = get_len_leaderboard(self.gameID, self.categID)
        self.WR = isodate.parse_duration(get_WR(self.categID)[0]).total_seconds()
    def __str__(self):
        def str_game(self):
            return f'|{get_system(self.system)[:6]:^6}| {get_game(self.gameID)[:30]:30}| {get_category(self.categID)[:15]:15}'
        def str_rank(self):
            calculation = f'{self.place}/{self.lenrank}'
            calculation2 = f'({str(round(100 * (self.lenrank - self.place) / self.lenrank,2)):^5} %)'
            return str(f'{calculation:^9} {calculation2}')
        def str_times(self):
            return f'{str_time(self.time)[:11]:12} | + {str_time(self.time - self.WR)[:11]:11}'
        return f'{str_game(self)} | {str_rank(self)} | {str_times(self)}'


if __name__ == "__main__":
    user = user("Pac")
    user.listPBs()