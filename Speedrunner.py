from Runs import Runs
from PBs import PBs
from main import get_user_infos
from run import Run
from PBs import PB


class Speedrunner:
    def __init__(self, user="Niamek"):
        data = get_user_infos()
        Run.update_game_db(data)  # Update game db.
        PB.update_game_db(data)  # Update game db.

        self.runs = Runs(data["runs"])
        self.runs.sort()

        self.PBs = PBs(data["runs"])


    def __str__(self):
        return str(self.PBs)

if __name__ == "__main__":
    test = Speedrunner()
    print(test)