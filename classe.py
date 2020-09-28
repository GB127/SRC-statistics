import datetime
import isodate
import matplotlib.pyplot as plot
import numpy
from api import *
from tools import *
import matplotlib.pyplot as plot

class run_time:

    def __init__(self, seconds):
        self.time = seconds
    def __str__(self):
        return str(datetime.timedelta(seconds=int(self.time)))

    def __format__(self, specs):
        return format(str(self), specs)

    def __mul__(self, integ):
        return run_time(self.time * integ)
    __rmul__ = __mul__

    def __round__(self, number):
        return run_time(round(self.time, number))

    def __truediv__(self, integ):
        return self.time / integ

    def __rtruediv__(self,integ):
        return integ / self.time

    def __sub__(self, other):
        return run_time(self.time - other.time)

    def __add__(self, other):
        if isinstance(other, run_time):
            return run_time(self.time + other.time)
        if isinstance(other, int):
            return run_time(self.time + other)
    __radd__ = __add__


class user:
    def __init__(self, username):
        """
            Class of a Speedrun.com user. The class contains informations such as username, runs, etc.

            Args:
                username (str) : Username on speedrun.com

            Attributes created:
                user.all_systems (list): List of all systems in which the user has a PB.
                user.ID (string) : User ID attributed by speedrun.com, fetched with a api request
                user.PBs (list) : List that contains *all* PBs of the user that aren't rejected.
                    All elements of this list are PB objects. Data collected with a request.
                user.rejected (dicto) : Dicto that tracks how many runs aren't
                    elligible for my stats analysis. The runs not elligible are
                    individual levels and runs short1er than 3 minutes.
                    - I decided to not include the individual levels runs because they
                        usually are very short1 and doesn't complete the game. I personally prefer
                        runs that actually complete the games or that does a significant part of the game.
                    - I don't include runs short1er than 3 minutes because I don't consider them long enough to be
                    worthy of analysis. I also noticed that most of these runs short1er than 3 minutes are meme runs
                    or meme games... Probably runs that wouldn't be (generally) accepted under current speedrun.com rules. 
                    - Obviously, not all runs that are "normal runs" fall under these criteria. Excluding these runs requires case
                        by case analysis, which is impossible to do because of the sheer number of games/categories.

                    Keys:
                        "level" : Quantity of individual levels (int)
                        "time" : Quantity of runs under of three minutes (int)
                user.runs (list) : List that contains *all* runs of the user that aren't rejected.
                    All elements of this list are Run objects. Data collected with a request.
                user.systems_PBs : Infos of user.PBs, grouped by systems.
                    hierachy:
                        "system" (dicto)
                            "count" (int): How many run on the said system.
                            "time" (int) : Summation of all PBs on the said system, in seconds.
                            "WR" (int) : Summation of all WRs on the said system, in seconds.
                            "delta" (int) : Summation of all deltas of WR on the said system, in seconds.
                user.systems_runs : Infos of user.runs, grouped by systems only.
                    hierachy:
                        "system" (dicto)
                            "count" (int): How many run on the said system.
                            "time" (int) : Summation of all runs on the said system, in seconds.
                user.total_PB (int) : Summation of all PB times of the user, in seconds.
                user.total_WR (int) : Summation of all Run times of the user, in seconds.
                user.username (string): Username of the user
        """
        def maker_runs_list(toupdate, list_runs, typ):
            """Function to update liste with runs.

            Args:
                toupdate (List): List to update
                list_runs (List): List of runs to verify
                typ (str): Determine if PB or run
            """

            for run in list_runs:
                if typ == "Run":
                    level = run["level"]
                    time = run["times"]["primary_t"]
                elif typ == "PB":
                    level = run["run"]["level"]
                    time = run["run"]["times"]["primary_t"]
                if level is None and time > 180:
                    if typ == "PB":
                        toupdate.append(PB(run))
                    elif typ == "Run":
                        toupdate.append(Run(run))
                elif level is not None and typ =="Run":
                    self.rejected["level"] += 1
                elif typ == "Run":
                    self.rejected["time"] += 1

        def runs_splitter_system(runs):
            tempo = {}
            for run in runs:
                try:
                    tempo[run.system]["count"] += 1
                    tempo[run.system]["time"] += run.time
                    if type(run) == PB:
                        tempo[run.system]["WR"] += run.WR    
                        tempo[run.system]["delta"] += run.delta
                except KeyError:
                    if type(run) == PB:
                        tempo[run.system] = {"count" : 1,
                                            "time" : run.time,
                                            "WR" : run.WR,
                                            "delta" : run.delta}
                    else:
                        tempo[run.system] = {"count" : 1,
                                            "time" : run.time}
            return tempo
        print("Fetching data...")  # Printing this because the fetching can take a couple of minutes.

        self.username = username
        self.ID = get_userID(self.username)
        self.runs, self.PBs = [], []
        self.rejected = {"level": 0, "time": 0}

        maker_runs_list(self.PBs,
                        get_PBs(self.ID),
                        typ="PB")
        maker_runs_list(self.runs,
                        get_runs(self.ID),
                        typ="Run")

        self.total_PB = sum([pb.time for pb in self.PBs])
        self.average_PB = run_time(self.total_PB / len(self.PBs))

        self.total_WR = sum([pb.WR for pb in self.PBs])
        self.total_delta = self.total_PB - self.total_WR
        self.average_delta = run_time(self.total_WR / len(self.PBs))

        self.total_run = sum([run.time for run in self.runs])
        self.average_run = run_time(self.total_run / len(self.runs))


        self.systems_PBs = runs_splitter_system(self.PBs)
        self.systems_runs = runs_splitter_system(self.runs)
        self.systems = sorted(list(self.systems_PBs.keys()))
        print("user initialized!")


    def fetch_runs_PB(self, PB):
        """
            Find all the runs for that PBs
        """

        #FIXME : Check vari too?
        toreturn = []
        for run in self.runs:
            if run.gameID == PB.gameID and run.categID == PB.categID:
                toreturn.append(run)
        return toreturn


    def fetch_runs_system(self, system, PB=False):
        liste = []
        if PB is False:
            for run in self.runs:
                if run.system == system:
                    liste.append(run)
            return liste
        elif PB:
            for run in self.PBs:
                if run.system == system:
                    liste.append(run)
            return liste


    def histo_runs(self):
        """Generate 4 histograms about the system times.

            runs times | PB times
            ---------------------
            PB delta   | PB %WR

            Args:
                user (object): User object
                system (string): System to analyse.

            """

        fig, axs = plot.subplots(2, 2)

        fig.suptitle(f"{self.username}")

        axs[0,0].hist([run.time for run in self.runs])
        axs[0,0].set_title("Runs")
        plot.sca(axs[0,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str_time(tick) for tick in plot.xticks()[0]])


        axs[0,1].hist([run.time for run in self.PBs])
        axs[0,1].set_title("PBs")
        plot.sca(axs[0,1])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str_time(tick) for tick in plot.xticks()[0]])



        axs[1,0].hist([run.delta for run in self.PBs])
        axs[1,0].set_title("delta WR")
        plot.sca(axs[1,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str_time(tick) for tick in plot.xticks()[0]])

        axs[1,1].hist([run.percWR for run in self.PBs])
        axs[1,1].set_title("%WR")
        plot.sca(axs[1,1])
        plot.xlim(left=100)
        plot.xticks(plot.xticks()[0], [str(tick) + " %" for tick in plot.xticks()[0]])

        plot.show()

    def histo_system(self, system):
        """Generate 4 histograms about the system times.

            runs times | PB times
            ---------------------
            PB delta   | PB %WR

            Args:
                user (object): User object
                system (string): System to analyse.

            """

        fig, axs = plot.subplots(2, 2)

        fig.suptitle(f"{self.username}\n{system}")

        data = self.fetch_runs_system(system)
        data_2 = [run.time for run in data]
        axs[0,0].hist(data_2)
        axs[0,0].set_title("Runs")
        plot.sca(axs[0,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str_time(tick) for tick in plot.xticks()[0]])


        data = self.fetch_runs_system(system, PB=True)
        data_2 = [run.time for run in data]
        axs[0,1].hist(data_2)
        axs[0,1].set_title("PBs")
        plot.sca(axs[0,1])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str_time(tick) for tick in plot.xticks()[0]])


        data_2 = [run.delta for run in data]
        axs[1,0].hist(data_2)
        axs[1,0].set_title("delta WR")
        plot.sca(axs[1,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str_time(tick) for tick in plot.xticks()[0]])

        data_2 = [run.percWR for run in data]
        axs[1,1].hist(data_2)
        axs[1,1].set_title("%WR")
        plot.sca(axs[1,1])
        plot.xlim(left=100)
        plot.xticks(plot.xticks()[0], [str(tick) + " %" for tick in plot.xticks()[0]])

        plot.show()



    def plot_systems(self):
        """Generate 4 pies that tells the proportions of systems.

            PB#     |   run#
            -------------------
            PB time | run time

            Args:
                user (object): User object.
            """
        fig, axs = plot.subplots(2, 2)

        fig.suptitle(f'{self.username}\n{len(self.systems)} systems')

        axs[0,0].set_title("PB #")
        axs[0,0].pie([self.systems_PBs[system]["count"] for system in self.systems], labels=[system for system in self.systems], autopct='%1.1f%%', startangle=90)

        axs[0,1].set_title("run #")
        axs[0,1].pie([self.systems_runs[system]["count"] for system in self.systems], labels=[system for system in self.systems], autopct='%1.1f%%', startangle=90)

        axs[1,0].set_title("PB total time")
        axs[1,0].pie([self.systems_PBs[system]["time"] for system in self.systems], labels=[system for system in self.systems], autopct='%1.1f%%', startangle=90)

        axs[1,1].set_title("run total time")
        axs[1,1].pie([self.systems_runs[system]["time"] for system in self.systems], labels=[system for system in self.systems], autopct='%1.1f%%', startangle=90)

        plot.show()

    def plot_runs(self, PB):  #FIXME : Rework on it.
        runs = self.fetch_runs_PB(PB)
        runs.sort(reverse=True)

        plot.title(f'{PB.game}\n{PB.categID}\nWR:{str_time(PB.WR)}')
        plot.axhline(y=PB.WR, c="gold")

        if len(runs) == 1:
            plot.plot([run.time for run in runs], marker="o")
        else:
            plot.plot([run.time for run in runs])
        plot.xlabel("PB #")
        plot.ylabel("Time")
        plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])
        plot.show()

    def plot_PB_leaderboard(self, PB):
        leaderboard = get_leaderboard(PB.gameID,PB.categID, PB.vari)

        rank_toremove = []
        for rank in leaderboard:
            if rank[1] > (6 * PB.WR):
                rank_toremove.append(rank)

        for rank in rank_toremove:
            leaderboard.remove(rank)


        plot.plot([time[0] for time in leaderboard], [rank[1] for rank in leaderboard])

        plot.title(f'{get_game(PB.gameID)}\n{get_category(PB.categID)}')


        plot.ylabel("Time")
        plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])

        plot.xlabel("Rank")
        ax = plot.gca()
        ax.set_xlim(ax.get_xlim()[::-1])
        plot.annotate(f"{self.username}", xy=(PB.place, PB.time), xytext=(0.65,0.65), textcoords="figure fraction",
                        arrowprops={"arrowstyle":"->"}
                        )



        plot.show()

    def plot_all_runs(self):
        cutoff_1 = 1800
        cutoff_2 = 60 ** 2
        cutoff_3 = (60 ** 2) * 3


        fig, axs = plot.subplots(2, 2)

        fig.suptitle(f"{self.username}")

        for run in self.PBs:
            tempo = [one.time for one in self.fetch_runs_PB(run)]
            tempo.sort(reverse=True)
            if tempo[0] < cutoff_1:
                if len(tempo) != 1:
                    axs[0,0].plot(tempo)
                else:
                    axs[0,0].plot(tempo, marker=".")
            elif tempo[0] < cutoff_2:
                if len(tempo) != 1:
                    axs[0,1].plot(tempo)
                else:
                    axs[0,1].plot(tempo, marker=".")
            elif tempo[0] < cutoff_3:
                if len(tempo) != 1:
                    axs[1,0].plot(tempo)
                else:
                    axs[1,0].plot(tempo, marker=".")
            else:
                if len(tempo) != 1:
                    axs[1,1].plot(tempo)
                else:
                    axs[1,1].plot(tempo, marker=".")


        plot.sca(axs[0,0])
        plot.yticks(plot.yticks()[0], [str_time(tick) for tick in plot.yticks()[0]])
        plot.sca(axs[0,1])
        plot.yticks(plot.yticks()[0], [str_time(tick) for tick in plot.yticks()[0]])
        plot.sca(axs[1,0])
        plot.yticks(plot.yticks()[0], [str_time(tick) for tick in plot.yticks()[0]])
        plot.sca(axs[1,1])
        plot.yticks(plot.yticks()[0], [str_time(tick) for tick in plot.yticks()[0]])



        plot.show()

    def table_PBs(self):
        """ Print a table by printing all PBs. Sorting can be changed by
            changing the PB.sort variable.
        """
        self.PBs.sort()  # Always sort in case we change the sorting method?

        ### En tete of the table
        print("-"*130)
        print(f"| #  |{'Sys':^6}| {'Game':^30}| {'Category':^15} | {'Time':^9}| + \u0394WR     |{'%WR':^10}| {'  Rank      (^%)':20}")
        print("-"*130)

        ### Actual entry of the table.
        for no, PB in enumerate(self.PBs): print(f'|{no+1:3} {PB}')
        print("-"*130)

        ### Foot of the table
        print(f'| {"Total :":>60}| {self.total_PB} (+ {self.total_delta})')
        print(f'| {"Average :":>60}| {self.average_PB} (+ {self.average_delta})')

    def table_systems(self):
        #FIXME : Idea : define a new function or method that returns the thing I want.

        """Print a table of the infos of the runs of the user by systems.
            """
        print("-" * 85)
        print(f'|   | System |{" Runs":20}|{" PBs":49}|')
        print("-" * 85)

        for no,system in enumerate(self.systems):
            short1 = self.systems_runs[system]
            short2 = self.systems_PBs[system]
            # Current system
            current_system = f'| {system[:6]:^6} |'
            # Runs count and time (coti) of the current system
            runs_coti = f'{short1["count"]:^4}| {short1["time"]:13} |'
            # Average of runs time
            runs_av_coti = f'{run_time(short1["time"]/short1["count"]):13} |'

            # PBs count, time, delta, and %WR (infos) of the current system
            PBs_infos = f'{short2["count"]:^4}| {short2["time"]:13} | + {short2["delta"]:13} | {round(100 * short2["time"] / short2["WR"],2):6} % |'
            # PBs average of infos
            PBs_av_infos = f'{run_time(short2["time"]/short2["count"]):13} | + {run_time(short2["delta"]/short2["count"]):13} |'

            print(f'|{no+1:^3}{current_system}{runs_coti}{PBs_infos}')
            print(f'|   |{"|--- ":>13}| {runs_av_coti}{"---":^4}| {PBs_av_infos} -------- |')
            print("-"*85)




class Run:
    sort = "time"

    def __init__(self, data):
        """
            Args:
                data ([json]): data from requests to speedrun.com

            Attributes:
                self.categID (string) : ID of the category ran
                self.emulated (bool): True if emulated, False if not emulated
                self.gameID (string): ID of the game ran
                self.ID (string): ID of the run
                self.system (string): System the run is on
                self.time (int): duration of the run, in seconds
                FIXME self.vari : "subcategories" of the category.
        """
        self.ID = data["id"]
        self.time = run_time(data["times"]["primary_t"])

        self.gameID = data["game"]
        self.game = get_game(self.gameID)

        self.categID = data["category"]
        self.categ = get_category(self.categID)
        self.vari = data["values"]

        self.system = get_system(data["system"]["platform"])
        self.emulated = data["system"]["emulated"]
        
    def __str__(self):
        """ Format: System|Game|Category|Time
            """
        return f'{self.system[:6]:^6}| {self.game[:30]:30} | {self.categ[:15]:15} | {self.time}'

    def __lt__(self, other):
        if get_game(self.gameID) != get_game(other.gameID):
            return get_game(self.gameID) <= get_game(other.gameID)
        elif get_category(self.categID) != get_category(other.categID):
            return get_category(self.categID) <= get_category(other.categID)
        else:
            return self.time <= other.time

class PB(Run):
    sort = "game"
    def __init__(self, data):
        """
            NOTES:
                Some extra infos not eally related to the PB 
                are stored because of the maths I want to do.

            New Attributes:
                self.delta (int): Time difference of PB compared to WR, in seconds. 
                self.place (int): Rank of the PB
                self.lenrank (int): Length of the leaderboard
                self.perclenrank (int): Percentage of people you beat in the leaderboard.
                    Note : If you are the only runner on the leaderboard, you will
                    have 0% even if you have the WR! This is because you don't beat anyone.
                    Will never be 100% because it doesn't count you : you ar emerely the threshold
                    for the maths.
                self.percWR (int): % of the WR. 100% means it's the WR. 200% means the time is exactly double
                    the WR
                self.WR (int): WR of the said run, in seconds)
        """
        super().__init__(data["run"])
        self.place = data["place"]
        self.lenrank = get_len_leaderboard(self.gameID, self.categID, self.vari)
        self.perclenrank = round(100 * (self.lenrank - self.place) / self.lenrank, 2)
        self.WR = run_time(get_WR(self.gameID, self.categID, self.vari))
        self.delta = self.time - self.WR
        self.percWR = round((self.time * 100/self.WR), 2)


    def __str__(self):  # FIXME : Documentate this
        def str_game(self):
            return f'|{self.system[:6]:^6}| {self.game[:30]:30}| {self.categ[:15]:15}'
        def str_rank(self):
            calculation = f'{self.place}/{self.lenrank}'
            calculation2 = f'({self.perclenrank:^5} %)'
            return str(f'{calculation:^9} {calculation2}')
        def str_times(self):
            return f'{self.time:8} | + {self.delta:8}| {self.percWR:^6} %'
        return f'{str_game(self)} | {str_times(self)} | {str_rank(self)}'


    def __lt__(self, other):
        if PB.sort == "game":
            return get_game(self.gameID) < get_game(other.gameID)
        elif PB.sort == "system":
            return self.system < other.system
        elif PB.sort == "time":
            return self.time < other.time
        elif PB.sort == "delta":
            return self.delta < other.delta
        elif PB.sort == "%WR":
            return self.percWR < other.percWR
        elif PB.sort == "%LB":
            return self.perclenrank > other.perclenrank



class leaderboard:
    def __init__(self):
        pass


    def plot_leaderboard(leaderboards):

        for year in leaderboards.keys():
            if len(leaderboards[year]) == 1:
                plot.plot([time[0] for time in leaderboards[year]], [rank[1] for rank in leaderboards[year]], label=year, marker="*")
            else:
                plot.plot([time[0] for time in leaderboards[year]], [rank[1] for rank in leaderboards[year]], label=year)

        plot.ylabel("Time")
        plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])

        plot.xlabel("Rank")
        ax = plot.gca()
        ax.set_xlim(ax.get_xlim()[::-1])
        


        plot.show()






if __name__ == "__main__":
    test = user("niamek")
    test.table_systems()