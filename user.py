from api import get_userID, get_PBs, get_runs
from tools import run_time, command_select, clear
from PBs import PBs, PBs_levels
from allRuns import Runs, Runs_levels
from Saves import Saves, Saves_levels
from Systems import Systems
from games import Games


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

        PBs_level_data, PBs_full_data = [], []
        for one in get_PBs(ID):
            if one["run"]["level"]:
                PBs_level_data.append(one)
            else:
                PBs_full_data.append(one)

        Runs_level_data, Runs_full_data = [], []
        for one in get_runs(ID):
            if one["level"]:
                Runs_level_data.append(one)
            else:
                Runs_full_data.append(one)

        if PBs_full_data:
            self.Runs = Runs(Runs_full_data)
            self.PBs = PBs(PBs_full_data)
            self.Saves = Saves(self.PBs, self.Runs)
            self.Systems = Systems(self.PBs, self.Runs)
            self.Games = Games(self.PBs, self.Runs)
        if PBs_level_data:
            self.Runs_level = Runs_levels(Runs_level_data)
            self.PBs_level = PBs_levels(PBs_level_data)
            self.Saves_level = Saves_levels(self.PBs_level, self.Runs_level)
            self.Systems_level = Systems(self.PBs_level, self.Runs_level)
            self.Games_level = Games(self.PBs_level, self.Runs_level)



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