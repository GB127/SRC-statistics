from entry import PB
from parameters import max_str_game
from tqdm import tqdm

class PBs(list):
    def __init__(self, data):
        tempo  = []
        for run in tqdm(data, desc="Preparing PB data"):
            if (run["time"] and not run["obsolete"]):
                tempo.append(PB(run))
        super().__init__(tempo)
        self.sort()

    def __str__(self):
        entete = f'{"Game":{max_str_game}}|{"Time":^9}|'
        line = "-" * len(entete)
        body = "\n".join(str(x) for x in self)

        return body


if __name__ == "__main__":
    from Speedrunner import Speedrunner
    test = Speedrunner().PBs

    print(test)