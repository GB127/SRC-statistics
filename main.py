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
        histo_all_runs(user)
        plot_all_runs(user)
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
        pb_tempo = user.PBs[which]
        lead_tempo = get_leaderboards(pb_tempo.gameID, pb_tempo.categID, pb_tempo.vari)
        plot_leaderboard(lead_tempo)

def system_analyser(user):
    """System analyser module.

        Args:
            user (object): User object from class.py
    """
    clear()
    user.table_systems()
    which = input_which(user.systems)
    if which == "all":
        plot_systems(user)
    else:
        plot_system(user, user.systems[which])

    # pie chart of WR difference per system
    # pie chart of WR% per system


if __name__ == "__main__":
    user = user(input("Who? "))
    main = True
    while main:
        command = input("[system, run, lb, sort, user, end] ")
        if command == "system":
            system_analyser(user)
        if command == "user":
            user.summarize()
        elif command == "run":
            run_analyser(user)
        elif command == "sort":
            PB.sort = input("Which sorting method? [game, system, time, delta, %WR, %LB] ")
        elif command == "end": main = False
        elif command == "lb":
            leaderboard_analyser(user)