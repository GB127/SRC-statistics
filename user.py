from api import get_userID, get_PBs, get_runs
from tools import run_time, command_select, clear
from PBs import PBs
from allRuns import Runs
from Saves import Saves
from Systems import Systems


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
        tempo = list(self.__dict__.values())[1:]
        return f'{self.username} ' + " ; ".join([f'{len(x)} {x.__class__.__name__}' for x in tempo])

    def __call__(self):
        while True:
            liste = list(self.__dict__.keys())
            liste.remove("username")
            clear()
            print(self)
            command = command_select(liste + ["end"], printer=True)
            if command == "end": break
            self.__dict__[command]()

if __name__ == "__main__":
    user("libre")()