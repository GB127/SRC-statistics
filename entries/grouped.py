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

