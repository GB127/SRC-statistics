from copy import copy
from random import randint
import os

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
            methods[int(command)]()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, id):
        return self.data[id]

    def __str__(self):
        string = ""
        for index, object in enumerate(self.data, start=1):
            string += f'{index:>3}   {str(object)}\n'
        string += "------" + "-" * len(str(object)) + "\n"
        string += f'{"∑":>3}   {sum(self)}\n'
        string += f'{"X̅":>4}   {self.mean()}'
        return string

    def sort(self, sorting_key=None):
        if not sorting_key:
            for index, attribute in enumerate(self.data[0].keys()):
                print(index, attribute)
            sorting_key = list(self.data[0].keys())[int(input("Which sorting key? "))]
        self.data.sort(key=lambda x: x[sorting_key])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def mean(self):
        return sum(self) / len(self)

    def sum(self):
        return sum(self)

    def median(self, filter):
        self.sort(filter)
        return self[len(self) // 2]


if __name__ == "__main__":
    test = Base_Table()
    test.data = [{f'allo':str(randint(6, 10))} for x in range(1,41)]
    test.sort()