import matplotlib.pyplot as plot
import datetime
from tools import *
from api import *
from classe import *

def plot_systems(user):
    """Generate 4 pies that tells the proportions of systems.

        PB#     |   run#
        -------------------
        PB time | run time

        Args:
            user (object): User object.
        """
    fig, axs = plot.subplots(2, 2)

    fig.suptitle(user.username)

    axs[0,0].set_title("PB #")
    axs[0,0].pie([user.systems_PBs[system]["count"] for system in user.all_systems], labels=[system for system in user.all_systems], autopct='%1.1f%%', startangle=90)


    axs[0,1].set_title("run #")
    axs[0,1].pie([user.systems_runs[system]["count"] for system in user.all_systems], labels=[system for system in user.all_systems], autopct='%1.1f%%', startangle=90)

    axs[1,0].set_title("PB total time")
    axs[1,0].pie([user.systems_PBs[system]["time"] for system in user.all_systems], labels=[system for system in user.all_systems], autopct='%1.1f%%', startangle=90)

    axs[1,1].set_title("run total time")
    axs[1,1].pie([user.systems_runs[system]["time"] for system in user.all_systems], labels=[system for system in user.all_systems], autopct='%1.1f%%', startangle=90)



    plot.show()


def plot_runs(PB,username, runs):  #FIXME : Rework on it.

    runs.sort(reverse=True)
    plot.plot([run.time for run in runs])
    plot.axhline(y=PB.WR, c="gold")
    plot.ylabel("Time")
    plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])
    plot.xlabel("PB #")
    plot.title(f'{get_game(PB.gameID)} - {get_category(PB.categID)}')
    plot.show()


def plot_leaderboard(PB, username):  #FIXME : Rework on it.
    leaderboard = get_leaderboard(PB.gameID,PB.categID, PB.vari)
    plot.plot([time[0] for time in leaderboard], [rank[1] for rank in leaderboard])
    plot.ylabel("Time")
    plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])
    plot.xlabel("Rank")
    plot.title(f'{get_game(PB.gameID)} - {get_category(PB.categID)}')
    ax = plot.gca()
    ax.set_xlim(ax.get_xlim()[::-1])
    if PB and username:
        plot.annotate(f"{username}", xy=(PB.place, PB.time), xytext=(0.65,0.65), textcoords="figure fraction",
                        arrowprops={"arrowstyle":"->"}
                        )
    plot.show()
    
def plot_system(user, system):
    """Generate 4 histograms about the system times.

        runs times | PB times
        ---------------------
        PB delta   | PB %WR

        Args:
            user (object): User object
            system (string): System to analyse.

        """

    fig, axs = plot.subplots(2, 2)

    fig.suptitle(f"{system}")

    data = user.fetch_runs_system(system)
    data_2 = [run.time for run in data]
    axs[0,0].hist(data_2)
    axs[0,0].set_title("Runs")
    plot.sca(axs[0,0])
    plot.xlim(left=0)
    plot.xticks(plot.xticks()[0], [str_time(tick) for tick in plot.xticks()[0]])


    data = user.fetch_runs_system(system, PB=True)
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


if __name__ == "__main__":
    testing = user("pac")
    testing.table_systems()
    plot_system(testing, "NES")