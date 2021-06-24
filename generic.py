from tools import command_select, run_time
class table:
    def __init__(self):
        self.backup = []
        self.data = []


    # TABLE RELATED STUFFS : Calling the class will create the table and the command promp
    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        return types
    def head(self):
        header = " no  |"
        for no, size in enumerate(self.data[0].table_size):
            header += f' {self.get_header()[no]}' + " "*size + "|"
        return header
    def foot(self):
        pass
    def __call__(self):
        def table():
            header = self.head()
            header += "\n" + ("-" * len(header))
            print(header)
            for no, entry in enumerate(self):
                print(f'{no+1:^4} | {entry}')
            print(self.foot())
        while True:
            self.data.sort()
            table()
            command_key = command_select(sorted(self.methods().keys()), printer=True)
            command = self.methods()[command_key]
            if command != "end":
                command()
            else:
                self.reset_filter()
                break

    # COMMAND PROMPT related
    def methods(self):
        return {"Change the sorting": self.change_sort,
                "Filter the table" : self.filter_select,
                "end": "end"}

    def filter_select(self):
        while True:
            print("To remove a single run, enter a single number\nTo remove a range, enter 2 numbers serparated by a -\nTo reset the filtering, enter reset\nTo cancel, type end")
            command = input()
            if command == "reset":
                self.reset_filter()
                break
            elif command == "end":
                break
            else:
                try:
                    number1, number2 = command.split("-")
                    self.filter(int(number1) -1, int(number2))
                    break
                except ValueError:
                    self.filter(int(command)-1)
                    break
                except:
                    pass

    def filter(self, start, end=None):
        if end:
            self.backup += self.data[:start]
            self.backup += self.data[end:]
            self.data = self.data[start: end]
        else:  # This works
            self.back = self.data[start]
            self.data.pop(start)

    def reset_filter(self):
        self.data = self.backup + self.data
        self.backup = []

    def change_sort(self):
        self.data[0].change_sort()

    # Basic stuffs for making the stuff an iterable and all.
    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)

class entry:
    def sortable(self):
        return list(self.__dict__)

    def change_sort(self):
        for no, one in enumerate(self.sortable()):
            print(no + 1, one)
        self.__class__.sorter = command_select(self.sortable())

    def __lt__(self, other):  # FIXME : If equal, it needs to have some sub-sorting.
        if self.__dict__[self.sorter] != other.__dict__[self.sorter]:
            return self.__dict__[self.sorter] < other.__dict__[self.sorter]
        elif self.game == other.game and self.category == other.category:
            return self.time > other.time
        elif self.game != other.game:
            return self.game < other.game
        elif self.category != other.category:
            return self.category < other.category

