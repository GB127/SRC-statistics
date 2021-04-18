from tools import run_time, command_select
from generic import table, entry
from allRuns import Run
from plots import plots



class Save(entry):
    sorter = "PB"
    table_size =  [1, 17, 13, 3, 5, 19, 4]
    def sortable(self):
        tempo = list(self.__dict__)
        tempo.remove("runs")
        return tempo



    def __init__(self, PB, Runs):
        self.system = PB.system
        self.game = PB.game
        self.category = PB.category
        self.runs = []
        for run in Runs:
            if run.game == self.game and run.category == self.category:
                self.runs.append(run)
        self.X = len(self.runs)

        Run.sorter = "time"
        self.runs.sort()
        self.first = self.runs[-1].time
        self.PB = PB.time
        self.save = self.first - self.PB
        self.perc1st = round(self.save/self.first * 100, 2)

    def __str__(self):
        return " | ".join([
                            f'{self.system[:6]:^6}',
                            f'{self.game[:20]:20}',
                            f'{self.category[:20]:20}',
                            f'{self.X:^3}',
                            f'{self.first:>9}',
                            f'{self.PB:>9}' + f' (-{self.save})',
                            f'(-{self.perc1st:6} %)'
                        ]) + "|"


class Saves(table):

    def histo(self):
        plots({"PBs" : [run.PB.time for run in self.data],
                "Firsts" : [run.first.time for run in self.data]}
            )()




    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("runs")
        types.remove("save")
        return types

    def __str__(self):
        return f"{len(self.data)} PBs with multiple runs"

    def __init__(self, PBs, Runs):
        self.data = []
        for pb in PBs:
            tempo = Save(pb, Runs)
            if tempo.first != tempo.PB:
                self.data.append(tempo)

    def foot(self):
        total_X = sum([category.X for category in self.data])
        total_first = sum([category.first for category in self.data])
        total_PB = sum([category.PB for category in self.data])
        total_delta = total_first - total_PB
        perc_delta = round(total_delta / total_first * 100, 2)

        string1 = "-" * 114 + "\n"
        string2 = f'{len(self.data)} PBs{"":47}Total:|{total_X:^5}| {total_first:>9} | {total_PB:>9} (-{total_delta})| (- {perc_delta:>5} %)|\n'
        string3 = f'{"Average:":>59}|{round(total_X/len(self.data)):^5}| {run_time(total_first/len(self.data)):>9} | {run_time(total_PB/len(self.data)):>9} (-{run_time(total_delta/len(self.data))}) | (- {perc_delta:>5} %)|'


        return string1 + string2 + string3

    def plot_2(self):
        all_plots = []
        for category in self.data:
            all_plots.append(list(reversed([run.time.time for run in category.runs])))

        #plot_table(all_plots)

    def methods(self):
        tempo = super().methods()
        #tempo["Plot the table : alternate"] = self.plot_2
        return tempo

    def plot(self):
        #plot_table([
        #                [save.first.time for save in self.data],
        #                [save.PB.time for save in self.data]],
        #            [
        #                "red",
        #                "blue"]
        #            )
        pass
