import numpy
import matplotlib.pyplot as plot

from api import *
from tools import run_time
from runs import Run, PB


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
        self.average_WR = self.total_WR / len(self.PBs)



        self.total_delta = self.total_PB - self.total_WR
        self.average_delta = run_time(self.total_delta / len(self.PBs))

        self.total_run = sum([run.time for run in self.runs])
        self.average_run = run_time(self.total_run / len(self.runs))

        self.average_perc = sum([one.percWR for one in self.PBs]) / len(self.PBs)

        self.systems_PBs = runs_splitter_system(self.PBs)
        self.systems_runs = runs_splitter_system(self.runs)
        self.systems = sorted(list(self.systems_PBs.keys()))

        for pb in self.PBs:
            pb.set_pb_number(self.fetch_runs_PB(pb))
            pb.saved(self.fetch_1st_PB(pb))

        print("user initialized!")


    def set_time_progression(self):
        progression = [run_time(0) for _ in range(sorted([x.number for x in self.PBs])[-1])]
        for pb in self.PBs:
            for no, run in enumerate(sorted(self.fetch_runs_PB(pb), reverse = True)):
                progression[no] += run.time
            for no in range(pb.number, len(progression)):
                progression[no] += pb.time
        return progression

    def fetch_1st_PB(self, PB):
        liste = self.fetch_runs_PB(PB)
        return liste[0]


    def fetch_runs_PB(self, PB):
        """
            Find all the runs for that PBs
        """
        toreturn = []
        for run in self.runs:
            if run.gameID == PB.gameID and run.categID == PB.categID and PB.vari == run.vari:
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

        axs[0,0].hist([run.time.time for run in self.runs])
        axs[0,0].set_title("Runs")
        plot.sca(axs[0,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str(run_time(tick)) for tick in plot.xticks()[0]])


        axs[0,1].hist([run.time.time for run in self.PBs])
        axs[0,1].set_title("PBs")
        plot.sca(axs[0,1])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str(run_time(tick)) for tick in plot.xticks()[0]])



        axs[1,0].hist([run.delta.time for run in self.PBs])
        axs[1,0].set_title("delta WR")
        plot.sca(axs[1,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str(run_time(tick)) for tick in plot.xticks()[0]])

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
        data_2 = [run.time.time for run in data]
        axs[0,0].hist(data_2)
        axs[0,0].set_title("Runs")
        plot.sca(axs[0,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str(run_time(tick)) for tick in plot.xticks()[0]])


        data = self.fetch_runs_system(system, PB=True)
        data_2 = [run.time.time for run in data]
        axs[0,1].hist(data_2)
        axs[0,1].set_title("PBs")
        plot.sca(axs[0,1])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str(run_time(tick)) for tick in plot.xticks()[0]])


        data_2 = [run.delta.time for run in data]
        axs[1,0].hist(data_2)
        axs[1,0].set_title("delta WR")
        plot.sca(axs[1,0])
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [str(run_time(tick)) for tick in plot.xticks()[0]])

        data_2 = [run.percWR for run in data]
        axs[1,1].hist(data_2)
        axs[1,1].set_title("%WR")
        plot.sca(axs[1,1])
        plot.xlim(left=100)
        plot.xticks(plot.xticks()[0], [str(tick) + " %" for tick in plot.xticks()[0]])

        plot.show()


    def pie_systems(self):
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
        axs[1,0].pie([self.systems_PBs[system]["time"].time for system in self.systems], labels=[system for system in self.systems], autopct='%1.1f%%', startangle=90)

        axs[1,1].set_title("run total time")
        axs[1,1].pie([self.systems_runs[system]["time"].time for system in self.systems], labels=[system for system in self.systems], autopct='%1.1f%%', startangle=90)

        plot.show()


    def plot_saves_PB(self, PB):  #FIXME : Rework on it.
        runs = self.fetch_runs_PB(PB)
        runs.sort(reverse=True)

        plot.title(f'{self.username}\n{PB.game}\n{PB.categ}')

        if len(runs) == 1:
            plot.plot([run.time.time for run in runs], marker="o", label=f'PB : {PB.time}')
        else:
            plot.plot([run.time.time for run in runs], label=f'PB : {PB.time}')

        plot.axhline(y=PB.WR.time, c="gold", label=f"WR : {PB.WR}")

        plot.xlabel("PB #")
        plot.ylabel("Time")
        plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])  # FIXME
        plot.legend()
        plot.show()


    def plot_PB_leaderboard(self, PB):
        leaderboard = get_leaderboard(PB.gameID,PB.categID, PB.vari)

        rank_toremove = []
        for rank in leaderboard:
            if rank[1] > (6 * PB.WR.time):
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
        plot.annotate(f"{self.username}", xy=(PB.place, PB.time.time), xytext=(0.65,0.65), textcoords="figure fraction",
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
            tempo = [one.time.time for one in self.fetch_runs_PB(run)]
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
        plot.yticks(plot.yticks()[0], [str(run_time(tick)) for tick in plot.yticks()[0]])
        plot.sca(axs[0,1])
        plot.yticks(plot.yticks()[0], [str(run_time(tick)) for tick in plot.yticks()[0]])
        plot.sca(axs[1,0])
        plot.yticks(plot.yticks()[0], [str(run_time(tick)) for tick in plot.yticks()[0]])
        plot.sca(axs[1,1])
        plot.yticks(plot.yticks()[0], [str(run_time(tick)) for tick in plot.yticks()[0]])



        plot.show()


    def histo_saves(self):
        data = []
        for run in self.PBs:
            if run.number > 1:
                data.append(run)
        plot.hist([[pb.time.time for pb in data], [pb.first.time.time for pb in data]],
        color=["green", "red"], label=["current", "first"])
        plot.legend()
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0],[datetime.timedelta(seconds=x) for x in plot.xticks()[0]])  # FIXME
        plot.title(f'{self.username}\n{len(data)} runs')



        plot.show()



    def histo_PBs_WR(self):
        plot.hist([[pb.WR.time for pb in self.PBs], [pb.time.time for pb in self.PBs]],
        color=["gold", "green"], label=["WR", "PBs"])
        plot.legend()
        plot.xlim(left=0)
        plot.xticks(plot.xticks()[0], [datetime.timedelta(seconds=x) for x in plot.xticks()[0]])  # FIXME
        plot.title(f'{self.username}\n{len(self.PBs)} runs')



        plot.show()




    def table_PBs(self):
        """ Print a table by printing all PBs. Sorting can be changed by
            changing the PB.sort variable.
        """
        self.PBs.sort()

        ### En tete of the table
        print("-"*130)
        print(f"| #  |{'Sys':^6}| {'Game':^30}| {'Category':^15} |{'Time':^9}| + \u0394WR     |{'%WR':^10}| {'  Rank      (^%)':20}")
        print("-"*130)

        ### Actual entry of the table.
        for no, PB in enumerate(self.PBs): print(f'|{no+1:3} {PB}')
        print("-"*130)

        ### Foot of the table
        print(f'| {"Total :":>60}| {self.total_PB} (+ {self.total_delta})')
        print(f'| {"Average :":>60}| {self.average_PB} (+ {self.average_delta}) | ({round(self.average_perc, 2)} %)')

    def table_saves(self):
        self.PBs.sort()
        solo, solo_time = 0, run_time(0)
        count, group, group_time, group_first, group_saved= 0, 0, run_time(0),run_time(0), run_time(0)
        print(f'   |{"game":30}|{"category":20}|###| {"First PB":10}| {"Current PB":10}| {"saved":^10} ({"%":^8})')
        print("-" * 106)
        for no, pb in enumerate(self.PBs):
            if pb.number != 1:
                print(f'{no+1:3}|{pb.game[:30]:30}|{pb.categ[:20]:20}|{pb.number:^3}| {pb.first.time:10}| {pb.time:10}| -{pb.saved:10}({round(100 - (pb.time*100/pb.first.time), 2):<6} %)')
                count += pb.number
                group += 1
                group_first += pb.first.time
                group_time += pb.time
                group_saved += pb.saved
            elif pb.number == 1:
                solo += 1
                solo_time += pb.time
        print("-" * 106)
        print(f'{"Total :" :>55}|{count:^3}| {group_first}  | {group_time}| -{group_saved}  ({round(100 - (group_time * 100 / group_first),2)} %)')
        print(f'{"Average :" :>55}|{count / group:^3}| {run_time(group_time / group)}  | -{run_time(group_saved / group)}')

        print("-" * 106)
        print(f'{solo} PBs with only 1 attempt, total time : {solo_time}')
        print(f'total time : {solo_time + group_time}')

    def table_saves_combined(self):
        data = self.set_time_progression()
        print(f'{"1"} | {data[0]} | ')
        for no, i in enumerate(data[1:]): 
            
            print(f'{no + 2} | {i} | {data[no] - i} | {round(100 - (i * 100 / data[no]),2)} %')

    def table_systems(self):

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




if __name__ == "__main__":
    # test = user("helienne")
    # test = user("deadephant")
    # test = user("zfg")
    test = user("lackattack24")
    # test = user("niamek")
    # test = user("baffan")
    # test = user("iateyourpie")
    # test = user("darbian")
    test.histo_PBs_WR()