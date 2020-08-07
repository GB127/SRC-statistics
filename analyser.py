def run_analyser(PB, username):
    stat = True
    while stat:
        stat = input("What do you want to do?")
        if stat == "lb":
            plot_leaderboard(PB, username)
        if stat == "end":
            return