from api import get_userID, get_PBs, get_runs
from tools import run_time
from PBs import PBs
from allRuns import Runs
from Saves import Saves
from Systems import Systems
from Games import Games








class user:
    def __init__(self, username):
        """
            Class of a Speedrun.com user. The class contains informations such as username, runs, etc.

            Args:
                username (str) : Username on speedrun.com
        """
        self.username = username.capitalize()
        print(f"Fetching {self.username}'s data...")
        ID = get_userID(self.username)

        self.PBs = PBs(get_PBs(ID))
        self.Runs = Runs(get_runs(ID))
        self.Saves = Saves(self.PBs, self.Runs)
        self.Systems = Systems(self.PBs, self.Runs)
        self.Games = Games(self.PBs, self.Runs)
        
        print("user initialized!")

    def __str__(self):
        tempo = list(self.__dict__.values())
        print(tempo)
        tempo.pop(3)  # Remove saves from the str because we don't want it there.
        return "; ".join([str(x) for x in tempo])

if __name__ == "__main__":
    test = user("niamek")
    test.table_data(test.PBs)