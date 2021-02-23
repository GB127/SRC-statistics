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
        def entete():
            tempo = [f'{"#":^3}',
                f'{"System":^7}',
                f'{"Game":40}',
                f'{"Category":20}',
                f'{"Time"}']
            print( " | ".join(tempo))
            print("-" * ((len(" | ".join(tempo)) + 3)))

        def pied():
            tempo = [f'{len(self.Runs):^3}',
                f'{"Total":>73}',
                f'{self.Runs.total_time()}']
            print("-" * ((len(" | ".join(tempo)) + 3)))
            print( " | ".join(tempo))
            tempo = [
                f'{"Mean":>79}',
                f'{self.Runs.mean_time()}']
            print( " | ".join(tempo))

        entete()
        for no, run in enumerate(self.Runs):
            print(f'{no+1:^3} | {run}')
        pied()

    def table_PBs(self):
        for pb in self.PBs:
            print(pb)

if __name__ == "__main__":
    test = user("niamek")
    test.table_Runs()