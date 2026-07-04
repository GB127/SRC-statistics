from Runs import Runs
from PBs import PBs
from main import get_user_infos
from entry import Run, PB, Entry


class Speedrunner:
    def __init__(self, user="Niamek"):
        data = get_user_infos()
        print(data.keys())
        Entry.update_game_db(data)  # Update game db.
        Entry.update_system_db(data)  # Update systems

        self.runs = Runs(data["runs"])
        self.runs.sort()

        # self.PBs = PBs(data["runs"])


if __name__ == "__main__":
    test = Speedrunner()
    print(test)