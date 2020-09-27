from plots import *
from classe import *
import os
from tools import input_which

clear = lambda: os.system('cls')

def run_analyser(user):
    """Runs analyser module.

        Args:
            user (object): User object from class.py
    """
    clear()
    user.table_PBs()
    user.PBs.sort()
    which = input_which(user.PBs)
    if which == "all":
        user.histo_all_runs()
        user.plot_all_runs()
    else:
        PB = user.PBs[which]
        user.plot_PB_leaderboard(PB)
        user.plot_runs(PB)

def system_analyser(user):
    """System analyser module.

        Args:
            user (object): User object from class.py
    """
    clear()
    user.table_systems()
    which = input_which(user.systems)
    if which == "all":
        user.plot_systems()
    else:
        user.plot_system(user.systems[which])

    # pie chart of WR difference per system
    # pie chart of WR% per system


if __name__ == "__main__":
    user = user(input("Who? "))
    main = True
    while main:
        command = input("[system, run, sort, user, end] ")
        if command == "system":
            system_analyser(user)
        if command == "user":
            user.summarize()
        elif command == "run":
            run_analyser(user)
        elif command == "sort":
            PB.sort = input("Which sorting method? [game, system, time, delta, %WR, %LB] ")
        elif command == "end": main = False