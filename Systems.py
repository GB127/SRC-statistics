from tools import run_time, command_select
from generic import table, entry
import matplotlib.pyplot as plot



class Systems(table):
    def __init__(self, PBs, Runs):
        print("Initializing Systems data")
        self.data = []
        self.backup = []
        data_PBs, data_Runs = {},{}
        for pb in PBs:
            data_PBs[pb.system] = data_PBs.get(pb.system, []) + [pb]
        for run in Runs:
            data_Runs[run.system] = data_Runs.get(run.system, []) + [run]

        for one_system in data_PBs.keys():
            self.data.append(System(one_system, data_PBs[one_system], data_Runs[one_system]))


    def get_header(self):
        types = ["system", "Runs","PBs"]
        return types


    def pie(self):
        pie_systems(self)()



    def foot(self):  #TODO: use local variable to reduce computer usage
        string1 = f'               | {sum([one.Run_count for one in self.data]):>3} Runs ;{sum([one.Run_Total for one in self.data]):>10} | {sum([one.PB_count for one in self.data]):>2}  PBs ;{sum([one.PB_Total for one in self.data]):>10} (+{sum([one.PB_Total_delta for one in self.data]):>9})\n'
        string2 = f'               | {int(sum([one.Run_count for one in self.data])/len(self)):>3} Runs ;{run_time(sum([one.Run_Total for one in self.data])/len(self)):>10} | {int(sum([one.PB_count for one in self.data])/len(self)):>2}  PBs ;{run_time(sum([one.PB_Total for one in self.data])/len(self)):>10} (+{run_time(sum([one.PB_Total_delta for one in self.data])/len(self)):>9})'
        return string1 + string2


    def methods(self):
        metho = super().methods()
        metho["Pie the table"] = self.pie
        return metho


class System(entry):
    table_size = [3, 17, 28]
    sorter = "system"
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

    def sortable(self):
        tempo = list(self.__dict__)
        tempo.remove("Pbs")
        tempo.remove("Runs")
        return tempo


class pie_systems:
    def __init__(self, systems):
        self.data = {"Runs":{},
                    "PBs":{}}
        for one_system in systems:
            self.data["Runs"][one_system.system] = [run.time.time for run in one_system.Runs]
            self.data["PBs"][one_system.system] = [run.time.time for run in one_system.Pbs]

    def pie_time(self):

        fig, axs = plot.subplots(1, 2)

        fig.suptitle(f'systems')

        axs[0].set_title("Runs Total time")
        axs[0].pie([sum(x) for x in self.data["Runs"].values()], 
                    labels=self.data["Runs"].keys(), 
                    autopct='%1.1f%%', 
                    pctdistance=0.8,
                    labeldistance=1.1,
                    startangle=90)

        axs[1].set_title("PBs Total time")
        axs[1].pie([sum(x) for x in self.data["PBs"].values()], 
                    labels=self.data["Runs"].keys(), 
                    autopct='%1.1f%%',
                    pctdistance=0.8,
                    labeldistance=1.1,
                    startangle=90)
        plot.show()

    def pie_frequency(self):

        fig, axs = plot.subplots(1, 2)

        fig.suptitle(f'systems')

        axs[0].set_title("Runs #")
        axs[0].pie([len(x) for x in self.data["Runs"].values()], 
                    labels=self.data["Runs"].keys(), 
                    autopct='%1.1f%%', 
                    pctdistance=0.8,
                    labeldistance=1.1,
                    startangle=90)

        axs[1].set_title("PBs #")
        axs[1].pie([len(x) for x in self.data["PBs"].values()], 
                    labels=self.data["Runs"].keys(), 
                    autopct='%1.1f%%',
                    pctdistance=0.8,
                    labeldistance=1.1,
                    startangle=90)
        plot.show()

    def __call__(self):
        commands = {"end" : "end",
                    "Pie chart : Frequency" : self.pie_frequency,
                    "Pie chart : total time" : self.pie_time}
        while True:
            command_key = command_select(sorted(commands.keys()), printer=True)
            command = commands[command_key]
            if command != "end":
                command()
            else:
                break

