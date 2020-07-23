import matplotlib.pyplot as plot
import datetime
from api import get_leaderboard

def plot_leaderboard():
    leaderboard = get_leaderboard()
    plot.plot([time[0] for time in leaderboard], [rank[1] for rank in leaderboard])
    plot.ylabel("Time")
    plot.yticks(plot.yticks()[0],[datetime.timedelta(seconds=x) for x in plot.yticks()[0]])
    plot.xlabel("Rank")
    ax = plot.gca()
    ax.set_xlim(ax.get_xlim()[::-1])
    plot.show()

if __name__ == "__main__":
    plot_leaderboard()