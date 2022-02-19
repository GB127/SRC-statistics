from copy import copy

class Base_Table:

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
        self.data.sort(key= lambda x: x[sorting_key])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def mean(self):
        return sum(self) / len(self)

    def sum(self):
        return sum(self)

    def median(self, filter):
        self.sort(filter)
        return self[len(self) // 2]

    def join(self, key):
        new = copy(self)
        sommes = {}
        for object in self.data:
            sommes[object[key]] = sommes.get(object[key], 0) + object
        new.data = list(sommes.values())

        return new