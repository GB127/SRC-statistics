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

    def pie(self):
        pie_systems(self)()


class System(entry):
    sorter = "system"
    def __init__(self, system, pbs, runs):
        self.system = system
        self.runs = runs
        self.pbs = pbs

        sum_Runs = sum(runs)
        sum_Pbs = sum(pbs)

        self.Run_count = len(self.runs)
        self.Run_Total = sum_Runs.time


        self.PB_count = len(pbs)
        self.PB_Total = sum_Pbs.time
        self.WR_Total = sum_Pbs.WR
        self.PB_delta = sum_Pbs.delta_p

        self.Run_average = run_time(self.Run_Total / self.Run_count)
        self.PB_average = run_time(self.PB_Total / self.PB_count)
        self.WR_average = run_time(self.WR_Total / self.PB_count)
        self.PB_delta_average = run_time(self.PB_delta / self.PB_count)


    def __str__(self):
        original = super().__str__()
        tempo = original.split(" | ")
        totals = tempo[:-4]
        averages = tempo[-4:]

        averages.insert(1, "   ")



        tempo2 = " | ".join(totals)
        tempo3 = " | ".join(averages)

        return f'{tempo2}\n{"":18}| {tempo3}'



    def __add__(self, other):
        tempo = super().__add__(other)

        tempo.Run_average = run_time(tempo.Run_Total / tempo.Run_count)
        tempo.PB_average = run_time(tempo.PB_Total / tempo.Run_count)
        tempo.WR_average = run_time(tempo.WR_Total / tempo.Run_count)
        tempo.PB_delta_average = run_time(tempo.PB_delta / tempo.Run_count)


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

