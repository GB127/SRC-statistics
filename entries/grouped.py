from code_SRC.composantes import Time
from statistics import StatisticsError, mean, geometric_mean as geomean

class Grouped:
    mode = sum
    def __init__(self,group_name,  runs:list, pbs:list):
        self.group_name = group_name
        self.runs = [x.time.seconds for x in runs]
        self.pbs = [x.time.seconds for x in pbs]

    def __str__(self):
        if Grouped.mode == geomean:
            filtered_data = [x for x in self.pbs if x != 0]
            if filtered_data:
                return f'{self.group_name[:30]:30}   {len(self.runs):3}   {Time(Grouped.mode(self.runs))}   {len(self.pbs):2}   {Time(Grouped.mode(filtered_data))}'
            else:
                return f'{self.group_name[:30]:30}   {len(self.runs):3}   {Time(Grouped.mode(self.runs))}   {len(self.pbs):2}   ---------'
        try:
            return f'{self.group_name[:30]:30}   {len(self.runs):3}   {Time(Grouped.mode(self.runs))}   {len(self.pbs):2}   {Time(Grouped.mode(self.pbs))}'
        except StatisticsError:
            return f'{self.group_name[:30]:30}   {len(self.runs):3}   {Time(Grouped.mode(self.runs))}   {len(self.pbs):2}   ---------'

    def keys(self):
        return "len_runs", "len_pbs", "runs_times", "pbs_times", "group_name"

    def __getitem__(self, clé):
        if clé == "len_runs":
            return len(self.runs)
        elif clé == "len_pbs": 
            return len(self.pbs)
        elif clé == "runs_times":
            return Grouped.mode(self.runs)
        elif clé == "pbs_times":
            return Grouped.mode(self.pbs)
        elif clé == "group_name":
            return self.group_name
        raise BaseException(f"Oops! check again {clé}")

class Saved:
    def __init__(self,group_name,  runs:list, pbs:list):
        self.category = group_name
        self.runs = tuple(sorted([x.time.seconds for x in runs], reverse=True))
        self.attempts = len(self.runs)
        self.first = Time(self.runs[0])
        self.pb = pbs.time
        self.WR = pbs["WR"]


    def __getitem__(self, clé):
        if clé == "save":
            return self.pb - self.first
        elif clé == "perc_save":
            return -(1 - self.pb / self.first)
        elif clé == "max_save":
            return self.WR - self.first
        elif clé == "max_perc":
            return -(1 - self.WR / self.first)
        elif clé == "perc_potential":
            return self["max_perc"] - self["perc_save"]
        elif clé == "save_potential":
            return self["max_save"] - self["save"]
        return self.__dict__[clé]

    def keys(self):
        return "first", "pb", "save", 
        , "perc_potential", "save_potential", "attempts"
        return "attempts", "first", "pb", "save", "perc_save", "max_save", "max_perc"
    def __str__(self):
        string_first = f'{len(self.runs):3}  {self.first}'
        string_pb = f'{self.pb} {self["save"]} {self["perc_save"]:>7.2%}'
        string_WR = f'{self["max_save"]} {self["max_perc"]:>7.2%}'
        string_potential = f'{self["save_potential"]} {self["perc_potential"]:>7.2%}'
        return f'{self.category[:40]:40} {string_first} | {string_pb} | {string_WR} | {string_potential}'