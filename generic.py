from tools import command_select, run_time
import matplotlib.pyplot as plot

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

class table:
    # TABLE RELATED STUFFS : Calling the class will create the table and the command promp
    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        return types
    def head(self):
        header = " no |"
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
                print(f'{no+1:^3} | {entry}')
            print(self.foot())
        while True:
            self.data.sort()
            table()
            command_key = command_select(sorted(self.methods().keys()), printer=True)
            command = self.methods()[command_key]
            if command != "end":
                command()
            else:
                break

    # COMMAND PROMPT related
    def methods(self):
        return {"Change the sorting": self.change_sort,
                "end": "end"}

    def change_sort(self):
        self.data[0].change_sort()



    # Basic stuffs for making the stuff an iterable and all.
    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)

    # graph stuffs
def plot_table(toplot, plotcolor=None):
    if plotcolor:
        for no, topl in enumerate(toplot):  #TODO: Improve this (Pretty sure a zip thingy does this)
            plot.plot(topl, color=plotcolor[no])
    else:
        for no, topl in enumerate(toplot):  #TODO: Improve this (Pretty sure a zip thingy does this)
            plot.plot(topl)



    plot.xlabel("Time")
    plot.xlim(left=0)
    plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])
    plot.show()

def histo_table(toplot, plotcolor):
    for no, topl in enumerate(toplot):  #TODO: Improve this (Pretty sure a zip thingy does this)
        plot.hist(topl, color=plotcolor[no])

    plot.xlim(left=0)
    plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
    plot.show()

def pie_table(toplot):
    pass