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

    def sort(self, sorting_key=None):
        self.data.sort(key= lambda x: x[sorting_key])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def mean(self):
        return sum(self) / len(self)

    def __str__(self):
        body = "\n".join([f'{no:3} {x}' for no,x in enumerate(self.data, start=1)])
        return "\n".join([body, f'  ∑ {sum(self)}', f'MOY {self.mean()}'])

    def median(self, filter):
        self.sort(filter)
        return self[len(self) // 2]