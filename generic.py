from tools import command_select, run_time

class entry:
    def sortable(self):
        return list(self.__dict__)

    def change_sort(self):
        for no, one in enumerate(self.sortable()):
            print(no + 1, one)
        self.__class__.sorter = command_select(self.sortable())

    def __lt__(self, other):
        return self.__dict__[self.sorter] < other.__dict__[self.sorter]

class table:
    def head(self):
        header = " no |"
        for no, size in enumerate(self.data[0].table_size):
            header += f' {self.get_header()[no]}' + " "*size + "|"
        return header        
    def __call__(self):
        def table():
            header = self.head()
            header += "\n" + ("-" * len(header))
            print(header)
            for no, entry in enumerate(self):
                print(f'{no+1:^3} | {entry}')
            print(self.foot())
        while True:
            table()
            command = input("What do you want to do? [sort, end]")
            if command == "end": break
            elif command == "sort":
                self.data[0].change_sort()
                self.data.sort()

    def foot(self):
        pass

    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)


    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        return types

