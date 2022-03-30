from random import randint
import os
from statistics import mean, geometric_mean, stdev

from copy import copy

clear = lambda: os.system('cls')

class Base_Table:
    def __call__(self, *methods):
        while True:
            clear()
            print(self)
            for index, fx in enumerate(methods):
                print(index, fx.__name__)
            command = input(f"Select option: [0-{len(methods) -1}] | Type end to exit\nInput : ")
            if command == "end":
                break
            methods[int(command)]()  # pragma: no cover

    def __len__(self):
        return len(self.data)

    def __getitem__(self, id):
        return self.data[id]

    def __str__(self):
        string = "------" + "-" * len(str(self.data[0])) + "\n"
        for index, object in enumerate(self.data, start=1):
            string += f'{index:>3}   {str(object)}\n'
        string += "------" + "-" * len(str(object)) + "\n"
        string += f'{"∑":>3}   {self.sum()}\n'
        string += "------" + "-" * len(str(object)) + "\n"
        string += f'{"X̅":>4}   {self.mean()}\n'
        string += f'{"gX̅":>4}   {self.geomean()}\n'
        string += "------" + "-" * len(str(object)) + "\n"

        return string

    def sort(self, sorting_key=None):
        if not sorting_key:
            for index, attribute in enumerate(self.data[0].keys()):
                print(index, attribute)
            sorting_key = list(self.data[0].keys())[int(input("Which sorting key? "))]
        self.data.sort(key=lambda x: x[sorting_key])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def sum(self):
        for_sommation = copy(self.data[0])
        for clé in self.data[0].__dict__:
            if isinstance(self.data[0][clé], (int,float)):
                for_sommation[clé] = sum([x[clé] for x in self.data])
            elif isinstance(self.data[0][clé], str):
                for_sommation[clé] = str((len(set([x[clé] for x in self.data]))))  # TODO: Get rid of str here

        return for_sommation

    def mean(self):
        for_mean = copy(self.data[0])
        for clé in self.data[0].__dict__:
            if isinstance(self.data[0][clé], (int,float)):
                for_mean[clé] = mean([x[clé] for x in self.data])
            elif isinstance(self.data[0][clé], str):
                for_mean[clé] = str(round(len(self.data)/len(set([x[clé] for x in self.data])),2))  # TODO: Get rid of str here
            
        return for_mean


    def geomean(self):
        for_mean = copy(self.data[0])
        for clé in self.data[0].__dict__:
            if isinstance(self.data[0][clé], (int,float)):
                for_mean[clé] = geometric_mean([x[clé] for x in self.data if x[clé] > 0])
            elif isinstance(self.data[0][clé], str):
                for_mean[clé] = ""
            
        return for_mean

    def stand_dev(self):
        for_stdev = copy(self.data[0])
        for clé in self.data[0].__dict__:
            if isinstance(self.data[0][clé], (int,float)):
                for_stdev[clé] = stdev([x[clé] for x in self.data])
            elif isinstance(self.data[0][clé], str):
                for_stdev[clé] = ""

        return for_stdev

    def stand_dev_geo(self):
        for_stdev = copy(self.data[0])
        for clé in self.data[0].__dict__:
            if isinstance(self.data[0][clé], (int,float)):
                for_stdev[clé] = stdev([x[clé] for x in self.data if x[clé] > 0], geometric_mean([x[clé] for x in self.data if x[clé] > 0]))
            elif isinstance(self.data[0][clé], str):
                for_stdev[clé] = ""

        return for_stdev

if __name__ == "__main__":  # pragma: no cover
    test = Base_Table()  # pragma: no cover
    test.data = [{f'int2':randint(6, 10), f'int':randint(6, 10), "string":"allo"} for x in range(1,41)]  # pragma: no cover
    test.stats()