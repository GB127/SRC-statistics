import datetime
import isodate
import matplotlib.pyplot as plot
import numpy
from api import *
from tools import *

class user:
    def __init__(self, username):
        self.username = username
        self.ID = get_userID(self.username)
        self.runs, self.PBs = [], []
        for run in get_runs(self.ID): self.runs.append(Run(run))
        for pb in get_PBs(self.ID): self.PBs.append(PB(pb))
    def printruns(self):
        for run in self.runs: print(run)
    def listPBs(self):
        for PB in self.PBs: print(PB)
class Run:
    def __init__(self, data):
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
        self.place = data["place"]
        super().__init__(data["run"])
        self.lenrank = get_len_leaderboard(self.gameID, self.categID)
        self.WR = isodate.parse_duration(get_WR(self.categID)[0]).total_seconds()
    def __str__(self):
        def str_game(self):
            return f'{get_game(self.gameID)[:30]:30}|{get_category(self.categID):20}'
        def str_rank(self):
            calculation = f'{self.place}/{self.lenrank}'
            calculation2 = "(" + str(round(100 * (self.lenrank - self.place) / self.lenrank,2)) + " %)"
            return str(f'{calculation:^9} {calculation2:9}')
        def str_times(self):
            return f'{str_time(self.time):9}(+ {str_time(self.time - self.WR)})'
        return f'{str_game(self)}|{str_rank(self)}|{str_times(self)}'




if __name__ == "__main__":
    user = user("niamek")
    user.listPBs()