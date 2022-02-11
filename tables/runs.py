from entries.run_entry import Run

class Table_run:
    def __init__(self, list_runs:list):
        self.data = []
        for data in list_runs:
            self.data.append(Run(data))

    def __getitem__(self, id):
        return self.data[id]

    def __len__(self):
        return len(self.data)

    def sort(self, key=None):
        self.data.sort(key=key)

    def mean(self):
        return sum(self) / len(self)

