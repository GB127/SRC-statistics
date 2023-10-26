from entries import Run, PB

class Table_Runs(list):
    def __init__(self, runs):
        super().__init__((Run(x) for x in runs))

    def __str__(self):
        return "\n".join([str(x) for x in self])

    def sort(self, key="game"):
        self[0].__class__.sorting_mode = key
        super().sort()

class Table_PBs(Table_Runs):
    def __init__(self, pbs):
        list.__init__(self, (PB(x) for x in pbs))


