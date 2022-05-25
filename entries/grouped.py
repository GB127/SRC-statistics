from code_SRC.composantes import Time

class Grouped:
    def __init__(self,group_name,  runs:list, pbs:list):
        self.group_name = group_name
        self.runs = runs
        self.pbs = pbs
        self.mode = sum

    def __str__(self):
        return f'{self.group_name}   {len(self.runs)}   {Time(self.mode([x.time.seconds for x in self.runs]))}   {len(self.pbs)}   {Time(sum([x.time.seconds for x in self.pbs]))}'