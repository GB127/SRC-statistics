import matplotlib.pyplot as plot
import datetime
from tools import *
from api import *

def plot_leaderboard(gameID, categID, PB=None, username=None): #TODO: Convert to user method
    leaderboard = get_leaderboard(gameID,categID)
    plot.plot([time[0] for time in leaderboard], [rank[1] for rank in leaderboard])
    plot.ylabel("Time")
    plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])
    plot.xlabel("Rank")
    plot.title(f'{get_game(gameID)} - {get_category(categID)}')
    ax = plot.gca()
    ax.set_xlim(ax.get_xlim()[::-1])
    if PB and username:
        plot.annotate(f"{username}", xy=(PB.place, PB.time), xytext=(0.65,0.65), textcoords="figure fraction",
                        arrowprops={"arrowstyle":"->"}
                        )
    plot.show()
    
if __name__ == "__main__":
    histo_leaderboard("smb", "Any")