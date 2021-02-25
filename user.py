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
        self.username = username.capitalize()
        print(f"Fectching {self.username}'s data...")
        self.ID = get_userID(self.username)

        self.PBs = PBs(get_PBs(self.ID))
        self.Runs = Runs(get_runs(self.ID))

        print("user initialized!")

    def __str__(self):  # Not sure I'll keep this. We'll see.
        return f'{self.username} : {self.Runs.total_time().days()} ({len(self.Runs)} runs) ; {self.PBs.total_time().days()} ({len(self.PBs)} PBs)'

if __name__ == "__main__":
    test = user("niamek")
    test.table_data(test.PBs)