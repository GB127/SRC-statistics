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

        for pb in self.PBs:
            for run in self.Runs:
                if pb.IDs == run.IDs:
                    run.WR = pb.WR
                    run.leaderboard = pb.leaderboard
        print("user initialized!")

    def table_Runs(self):
        def entete():
            tempo = [f'{"#":^3}',
                f'{"System":^7}',
                f'{"Game":20}',
                f'{"Category":20}',
                f'{"Time":^9}',
                f'{"deltaWR"}']  # NOTE : Put back the delta symbol
            print( " | ".join(tempo))
            print("-" * ((len(" | ".join(tempo)) + 3)))
        def pied():
            tempo = [f'{len(self.Runs):^3}',
                f'{"Total":>53}',
                f'{self.Runs.total_time():>9}',
                f'+ {self.Runs.total_deltaWR():<9}']
            print("-" * ((len(" | ".join(tempo)) + 3)))
            print( " | ".join(tempo))
            tempo = [
                f'{"Mean":>59}',
                f'{self.Runs.mean_time():>9}',
                f'+ {self.Runs.mean_deltaWR():<9}']
            print( " | ".join(tempo))
        entete()
        for no, run in enumerate(self.Runs):
            print(f'{no+1:^3} | {run}')
        pied()


    def table_PBs(self):
        def entete():
            tempo = [f'{"#":^3}',
                f'{"System":^7}',
                f'{"Game":20}',
                f'{"Category":20}',
                f'{"Time":^9}',
                f'{"deltaWR"}']  # NOTE : Put back the delta symbol
            print( " | ".join(tempo))
            print("-" * ((len(" | ".join(tempo)) + 3)))
        def pied():
            tempo = [f'{len(self.PBs):^3}',
                f'{"Total":>53}',
                f'{self.PBs.total_time():>9}',
                f'+ {self.PBs.total_deltaWR():<9}']
            print("-" * ((len(" | ".join(tempo)) + 3)))
            print( " | ".join(tempo))
            tempo = [
                f'{"Mean":>50}',
                f'{self.PBs.mean_time():>9}',
                f'+ {self.PBs.mean_deltaWR():<9}']
            print( " | ".join(tempo))
        entete()
        for no, run in enumerate(self.PBs):
            print(f'{no+1:^3} | {run}')
        pied()


if __name__ == "__main__":
    test = user("niamek")
    test.table_Runs()