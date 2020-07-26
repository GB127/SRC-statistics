import datetime
import isodate
import matplotlib.pyplot as plot
import numpy
from api import get_userID, get_PBs, get_runs

class user:
    def __init__(self, username):
        self.username = username
        self.ID = get_userID(self.username)
        self.runs, self.PBs = [], []
        for run in get_runs(self.ID): self.runs.append(Run(run))
        for PB in get_PBs(self.ID): self.PBs.append((PB["place"], Run(PB["run"])))

class Run:
    def __init__(self, data):
        self.system = data["system"]["platform"]
        self.emulated = True if data["system"]["emulated"] else False
        self.ID = data["id"]
        self.gameID = data["game"]
        self.categID = data["category"]
        self.time = isodate.parse_duration(data["times"]["primary"]).total_seconds()

if __name__ == "__main__":
    user = user("niamek")
    print(user.PBs)