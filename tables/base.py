from code_SRC.composantes import Time
from statistics import fmean, geometric_mean as geomean
from math import fsum
from collections import Counter
from itertools import chain
from os import system as text_terminal

from tables.leaderboard import LB

clear = lambda: text_terminal("cls")


class Base_table:
    def __call__(self):
        while True:
            clear()
            print(self)
            print("\n")

            for index, fx in enumerate(self.methods()):
                print(index, fx.__name__)
            command = input(
                f"Select option: [0-{len(self.methods()) -1}] | Type end to exit\nInput : "
            )
            if command == "end":
                break
            self.methods()[int(command)]()

    def sort(self, key=None):
        if not key:
            for no, option in enumerate(self.keys()):
                print(no, option)
            key = self.keys()[int(input("Which sorting method? "))]
        self.data.sort(key=lambda x: x[key])

    def group_attr(self) -> dict:
        dicto_sets = {}
        for clé in self.keys():
            if isinstance(self[0][clé], set):
                dicto_sets[clé] = Counter(chain(*[x[clé] for x in self.data]))
            elif isinstance(self[0][clé], (Time, int, float, LB)):
                dicto_sets[clé] = list(x[clé] for x in self.data)
            else:
                dicto_sets[clé] = Counter(x[clé] for x in self.data)
        assert (
            list(dicto_sets.keys()) == self.keys()
        ), f"{dicto_sets.keys()} == {self.keys()}"
        return dicto_sets

    def sum(self) -> dict:
        dicto_groups = self.group_attr()
        dicto_sum = {}
        for clé in self.keys():
            if isinstance(self[0][clé], (int, float, Time)):
                dicto_sum[clé] = fsum(dicto_groups[clé])
            elif isinstance(self[0][clé], LB):
                continue
            else:
                dicto_sum[clé] = len(dicto_groups[clé])
        return dicto_sum

    def mean(self) -> dict:
        dicto_groups = self.group_attr()
        dicto_mean = {}
        for clé in self.keys():
            if isinstance(self[0][clé], (int, float, Time)):
                dicto_mean[clé] = fmean(dicto_groups[clé])
            elif isinstance(self[0][clé], LB):
                continue
            else:
                dicto_mean[clé] = len(dicto_groups[clé]) / len(self)
        return dicto_mean

    def geomean(self) -> dict:
        dicto_groups = self.group_attr()
        dicto_mean = {}
        for clé in self.keys():
            if isinstance(self[0][clé], (int, float, Time)):
                dicto_mean[clé] = geomean(
                    [float(x) for x in dicto_groups[clé] if float(x) > 0]
                )
            elif isinstance(self[0][clé], LB):
                continue
            else:
                dicto_mean[clé] = len(self) / len(dicto_groups[clé])
        return dicto_mean

    def __str__(self):
        line = "-------" + "-" * len(str(self.data[0])) + "\n"
        string = line
        for index, object in enumerate(self.data, start=1):
            string += f"{index:>4}   {str(object)}\n"
        string += line
        string += f"       {self.create_grouped(self.sum())}\n"
        string += f"       {self.create_grouped(self.mean())}\n"
        string += f"       {self.create_grouped(self.geomean())}"
        return string

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return bool(self.data)

    def __getitem__(self, index: int):
        return self.data[index]

    def keys(self):
        """Retrieves keys that can be used for sorting."""
        return self[0].keys()
