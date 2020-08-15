import matplotlib.pyplot as plot
import datetime
from tools import *
from api import *
from classe import *

def plot_userchart(user):
    
    systems = {}
    for PB in user.PBs:
        try:
            systems[PB.system] += 1
        except KeyError:
            systems[PB.system] = 1
    plot.pie([systems[system] for system in systems.keys()], labels=[system for system in systems.keys()], autopct='%1.1f%%')
    
    """
    systems = {}
    for run in user.runs:
        try:
            systems[run.system] += 1
        except KeyError:
            systems[run.system] = 1
    plot.pie([systems[system] for system in systems.keys()], labels=[system for system in systems.keys()], autopct='%1.1f%%')
    """



    plot.show()






def plot_runs(PB,username, runs):

    runs.sort(reverse=True)
    plot.plot([run.time for run in runs])
    plot.axhline(y=PB.WR, c="gold")
    plot.ylabel("Time")
    plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])
    plot.xlabel("PB #")
    plot.title(f'{get_game(PB.gameID)} - {get_category(PB.categID)}')
    plot.show()

def plot_leaderboard(PB, username):
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
    
if __name__ == "__main__":
    plot_userchart(user("lackattack24"))