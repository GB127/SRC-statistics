from entry import PB
from parameters import max_str_game


class PBs(list):
    def __init__(self, data):
        print(data[0].keys())
        super().__init__([PB(x) for x in data if (x["time"] and not x["obsolete"])])

    def __str__(self):
        entete = f'{"Game":{max_str_game}}|{"Time":^9}|'
        line = "-" * len(entete)
        body = "\n".join(str(x) for x in self)

        return body


if __name__ == "__main__":
    from Speedrunner import Speedrunner
    test = Speedrunner().PBs

    print(test)