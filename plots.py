import matplotlib.pyplot as plot
import datetime
from api import *

def plot_leaderboard(gameID, categID):
    leaderboard = get_leaderboard(gameID,categID)
    plot.plot([time[0] for time in leaderboard], [rank[1] for rank in leaderboard])
    plot.ylabel("Time")
    plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])
    plot.xlabel("Rank")
    plot.title(f'{get_game("o1y9wo6q")} - {get_category("7dgrrxk4")}')
    ax = plot.gca()
    ax.set_xlim(ax.get_xlim()[::-1])
    plot.show()

if __name__ == "__main__":
    plot_leaderboard("o1y9wo6q", "7dgrrxk4")