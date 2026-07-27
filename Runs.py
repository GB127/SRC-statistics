from entry import Run, PB
from utils import time_str
from statistics import mean

class Runs(list):
    def __init__(self, data):
        super().__init__([Run(**x) for x in data])
        self.sort(key=lambda x: x["game"])


    def __str__(self):
        body = "\n".join([str(x) for x in self])
        total_time = sum(x.time for x in self)
        str_total = f'{"Total":30}|{time_str(total_time):>10}|'
        mean_time = mean(x.time for x in self)
        str_mean = f'{"Mean":30}|{time_str(mean_time):>10}|'
        line = "-" * len(str_total)
        return f'{line}\n{body}\n{line}\n{str_total}\n{line}\n{str_mean}'

class PBs(list):
    def __init__(self, data):
        super().__init__([PB(**x) for x in data])
        self.sort(key=lambda x: x["game"])

    def __str__(self):
        body = "\n".join([str(x) for x in self])
        total_time = sum(x.time for x in self)
        str_total = f'{"Total :":>51}|{time_str(total_time):>10}|'
        mean_time = mean(x.time for x in self)
        str_mean = f'{"Mean :":>51}|{time_str(mean_time):>10}|'
        line = "-" * len(str_total)
        return f'{line}\n{body}\n{line}\n{str_total}\n{line}\n{str_mean}'
