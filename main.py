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
        pass
    else:
        PB = user.PBs[which]

        plot_PB_leaderboard(PB, user)
        plot_runs(PB, user)

def leaderboard_analyser(user):
    clear()
    user.table_PBs()
    which = input_which(user.PBs)
    if which == "all": pass
    else:
        plot_leaderboard(user.PBs[which])

def system_analyser(user):
    """System analyser module.

        Args:
            user (object): User object from class.py
    """
    clear()
    user.table_systems()
    which = input_which(user.all_systems)
    if which == "all":
        plot_systems(user)
    else:
        plot_system(user, user.all_systems[which])

    # pie chart of WR difference per system
    # pie chart of WR% per system


if __name__ == "__main__":
    user = user(input("Who? "))
    main = True
    while main:
        command = input("[system, run, lb, sort end] ")
        if command == "system":
            system_analyser(user)
        elif command == "run":
            run_analyser(user)
        elif command == "sort":
            PB.sort = input("Which sorting method? [game, system, time, delta, %WR, %LB] ")
        elif command == "end": main = False
        elif command == "lb":
            leaderboard_analyser(user)