import matplotlib.pyplot as plot



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
    testing = user("zfg")
    plot_all_runs(testing)