from run import Run
from parameters import max_str_game
from utils import time_str
from statistics import mean, median

class Runs(list):
    def __init__(self, data):
        super().__init__([Run(x) for x in data if x["time"]])

    def __str__(self):
        entete = f'{"Game":{max_str_game}}|{"Time":^9}|'
        line = "-" * len(entete)
        body = "\n".join(str(x) for x in self)

        foot = f'{f"Total: {len(self)} runs":{max_str_game}}|{time_str(self.sum()):>9}|'
        foot += f'\n{"Mean:":{max_str_game}}|{time_str(self.mean()):>9}|'
        foot += f'\n{"Median:":{max_str_game}}|{time_str(self.median()):>9}|'

        return f"\n{line}\n".join([entete, body, foot])

    def sum(self):
        return sum([x["time"] for x in self])

    def mean(self):
        return mean([x["time"] for x in self])

    def median(self):
        return median([x["time"] for x in self])


if __name__ == "__main__":
    from Speedrunner import Speedrunner
    test = Speedrunner().runs

    print(test)