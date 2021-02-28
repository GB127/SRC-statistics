from api import get_userID, get_PBs, get_runs
from tools import run_time
from runs import PBs, Runs, Saves


class user:
    def __init__(self, username):
        """
            Class of a Speedrun.com user. The class contains informations such as username, runs, etc.

            Args:
                username (str) : Username on speedrun.com
        """
        self.username = username.capitalize()
        print(f"Fectching {self.username}'s data...")
        self.ID = get_userID(self.username)

        self.PBs = PBs(get_PBs(self.ID))
        self.Runs = Runs(get_runs(self.ID))
        self.Saves = Saves(self.PBs, self.Runs)
        
        print("user initialized!")

    def __str__(self):
        tempo = list(self.__dict__.values())
        tempo.pop(1)  # Remove the ID
        tempo.pop(3)
        return "; ".join([str(x) for x in tempo])

if __name__ == "__main__":
    test = user("niamek")
    test.table_data(test.PBs)