from Runs import Runs
from main import get_user_infos
from run import Run


class Speedrunner:
    def __init__(self, user="Niamek"):
        data = get_user_infos()
        Run.update_game_db(data)  # Update game db.

        self.runs = Runs(data["runs"])
        self.runs.sort()

    def __str__(self):
        return str(self.runs)

if __name__ == "__main__":
    test = Speedrunner()
    print(test)