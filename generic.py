from tools import command_select

class entry:

    def __init__(self):
        raise BaseException("You cannot create an entry class this way")

    def __str__(self):
        pass

    def change_sort(self):
        for no, one in enumerate(list(self.__dict__)):
            print(no + 1, one)
        self.__class__.sorter = command_select(list(self.__dict__))

    def __lt__(self, other):
        if self.__dict__[self.sorter] != other.__dict__[self.sorter]:
            return self.__dict__[self.sorter] < other.__dict__[self.sorter]
        return self.category < other.category
