from api import get_userID, get_PBs, get_runs
from tools import run_time, percent
from runs import PBs, Runs


class user:
    def __init__(self, username):
        """
            Class of a Speedrun.com user. The class contains informations such as username, runs, etc.

            Args:
                username (str) : Username on speedrun.com
        """
        self.username = username
        self.ID = get_userID(self.username)

        self.PBs = PBs(get_PBs(self.ID))
        self.Runs = Runs(get_runs(self.ID))
        print("user initialized!")
    def debug(self):
        for run in self.PBs:
            print(run)

    def table_Runs(self):
        for run in self.Runs:
            print(run)

    def table_PBs(self):
        for pb in self.PBs:
            print(pb)

if __name__ == "__main__":
    test = user("niamek")
    test.table_Runs()