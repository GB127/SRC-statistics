class Systems(table):
    def __init__(self, PBs, Runs):
        self.data = []
        data_PBs, data_Runs = {},{}
        for pb in PBs:
            data_PBs[pb.system] = data_PBs.get(pb.system, []) + [pb]
        for run in Runs:
            data_Runs[run.system] = data_Runs.get(run.system, []) + [run]

        for one_system in data_PBs.keys():
            self.data.append(System(one_system, data_PBs[one_system], data_Runs[one_system]))

    def __str__(self):
        return f'{len(self.data)} systems'

    def foot(self):  #TODO: use local variable to reduce computer usage
        string1 = f'{len(self)} systems{"":7}{sum([one.Run_count for one in self.data])} Runs ; {sum([one.Run_Total for one in self.data]):>11} | {sum([one.PB_count for one in self.data])} PBs ; {sum([one.PB_Total for one in self.data]):>10} (+{sum([one.PB_Total_delta for one in self.data]):>9})\n'
        string2 = f'{len(self)} systems{"":7}{int(sum([one.Run_count for one in self.data])/len(self))} Runs ; {run_time(sum([one.Run_Total for one in self.data])/len(self)):>11} | {int(sum([one.PB_count for one in self.data])/len(self))} PBs ; {run_time(sum([one.PB_Total for one in self.data])/len(self)):>10} (+{run_time(sum([one.PB_Total_delta for one in self.data])/len(self)):>9})'
        return string1 + string2



class System(entry):
    table_size = [3, 17, 21]
    sorter = "system"


    def sortable(self):
        tempo = list(self.__dict__)
        tempo.remove("Pbs")
        tempo.remove("Runs")
        return tempo


    def __init__(self, system, pbs, runs):
        self.system = system
        self.Runs = runs
        self.Run_count = len(self.Runs)
        self.Run_Total = sum([run.time for run in self.Runs])
        self.Run_average = run_time(sum([run.time for run in self.Runs]) / self.Run_count)


        self.Pbs = pbs
        self.PB_count = len(pbs)
        self.PB_Total = sum([pb.time for pb in self.Pbs])
        self.PB_average = run_time(self.PB_Total / self.PB_count)
        self.WR_Total = sum([pb.WR for pb in self.Pbs])
        self.PB_Total_delta = self.PB_Total - self.WR_Total
        self.PB_Total_delta_average = run_time(self.PB_Total_delta / self.PB_count)


    def __str__(self):
        tempo = [f"{self.system:^8}",
                f'{self.Run_count:^3} Runs ; {self.Run_Total:>9}',
                f'{self.PB_count:^3} PBs ; {self.PB_Total:>9} (+{self.PB_Total_delta:>8})\n   ',
                f'        ',
                f'           {self.Run_average:>9}', 
                f'          {self.PB_average:>9} (+{self.PB_Total_delta_average:>8})\n' + "-" * 80]
        return " | ".join(tempo)
