from tools import run_time, command_select
from run import Run, PB, Save, System, Game
from generic import table, plot_table, histo_table

class Runs(table):
    def __init__(self, data):
        self.data = []
        for run in data:
            if run["times"]["primary_t"] >= 180 and not run["level"]:
                self.data.append(Run(run))

    def foot(self):  # TODO: Move calculs to variables so it uses less computer power?
        string1 = f"{'-' * 72}\n" 
        string2 = f"{'Total |':>60}{sum([x.time for x in self.data]):>11}\n"
        string3 = f"{'Average |':>60}{run_time(sum([x.time for x in self.data]) / len(self)):>11}\n"
        return string1 + string2 + string3

    def __str__(self):
        return f'{len(self)} runs ({sum([x.time for x in self.data]).days()})'

    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("IDs")
        return types

    def histo(self):
        histo_table([[run.time.time for run in self.data]], ["orange"])

    def plot(self):
        pass  # TODO: REDO IT
class PBs(Runs):
    def __init__(self, data):
        self.data = []
        for pb in data:
            if pb["run"]["times"]["primary_t"] > 180 and not pb["run"]["level"]:
                self.data.append(PB(pb))

    def __str__(self):
        return f'{len(self)} PBs ({sum([x.time for x in self.data]).days()})'

    def plot(self):
        plot_table([
                        [run.time.time for run in self.data],
                        [run.WR.time for run in self.data]],
                    [
                        "blue",
                        "gold"]
                    )


    def histo(self):
        histo_table([[run.time.time for run in self.data]], ["blue"])

    def get_header(self):
        types = super().get_header()
        types.remove("leaderboard")
        types.remove("WR")
        return types


    def foot(self):
        string1, string2, string3 = super().foot()
        return string1 + string2 + string3

class Saves(table):

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
        string2 = f'{len(self.data)} PBs{"":47}Total:|{total_X:^5}| {total_first:>9} | {total_PB:>9} (-{total_delta}) | (- {perc_delta:>5} %)|\n'
        string3 = f'{"Average:":>59}|{round(total_X/len(self.data)):^5}| {run_time(total_first/len(self.data)):>9} | {run_time(total_PB/len(self.data)):>9} (-{run_time(total_delta/len(self.data))}) | (- {perc_delta:>5} %)|'


        return string1 + string2 + string3

    def plot_2(self):  #TODO : use the generic plot
        for category in self.data:
            plot.plot(list(reversed([run.time.time for run in category.runs])))  #TODO : Move this to elsewhere

        plot.ylabel("Time")
        plot.ylim(bottom=0)
        plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])
        plot.legend()
        plot.show()


    def methods(self):
        tempo = super().methods()
        tempo["Plot the table : alternate"] = self.plot_2
        return tempo

    def histo(self):
        plot.hist([[run.PB.time for run in self.data], [run.first.time for run in self.data]], label=["PBs","Firsts"], color=["Blue", "Red"])
        plot.xlabel("Time")
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0],[str(run_time(x)) for x in plot.xticks()[0]])
        plot.legend()
        plot.show()

    def plot(self):
        plot_table([
                        [save.first.time for save in self.data],
                        [save.PB.time for save in self.data]],
                    [
                        "red",
                        "blue"]
                    )


class Games(table):
    def __init__(self, PBs, Runs):
        self.data = []
        data_PBs, data_Runs = {},{}
        for pb in PBs:
            data_PBs[pb.game] = data_PBs.get(pb.game, []) + [pb]
        for run in Runs:
            data_Runs[run.game] = data_Runs.get(run.game, []) + [run]

        for game in data_PBs.keys():
            self.data.append(Game(game, data_PBs[game], data_Runs[game]))

    def __str__(self):
        return f'{len(self.data)} Games'

    def foot(self):
        runs_count = sum([game.Run_count for game in self.data])
        total_runs = sum([game.Run_Total for game in self.data])
        total_PBs = sum([game.PB_Total for game in self.data])
        PBs_count = sum([game.PB_count for game in self.data])
        total_WRs = sum([game.WR_Total for game in self.data])
        total_deltas = sum([game.PB_Total_delta for game in self.data])
        perc_average = round(total_PBs / total_WRs * 100, 2)


        string1 = "-" * 93 + "\n"
        string2 = f"{len(self.data):<3} games{'':28}|{runs_count:3} | {total_runs:9} |{PBs_count:3} | {total_PBs:>9} (+{total_deltas:7})| {perc_average} %\n"
        string3 = f"{len(self.data):<3} games{'':28}|{int(runs_count/len(self.data)):3} | {run_time(total_runs/len(self.data)):9} |{int(PBs_count/len(self.data)):3} | {run_time(total_PBs/len(self.data)):>9} (+{run_time(total_deltas/len(self.data)):7}) | {perc_average} %"

        return string1 + string2 + string3

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

    def foot(self):
        return "To complete"
