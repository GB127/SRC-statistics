from plots import *
from classe import *
import os

clear = lambda: os.system('cls')

def run_analyser(user):
    clear()
    user.table_PBs()
    which = input_which(user.PBs)
    if which == "all":
        pass
    else:
        PB = user.PBs[which]

        plot_leaderboard(PB, user.username)
        plot_runs(PB, user.username, user.runs_PB(PB) )

def system_analyser(user):
    clear()
    user.table_systems()
    which = input_which(user.all_systems)
    if which == "all":
        plot_systems(user)
    else:
        plot_system(user, user.all_systems[which])

    # pie chart of WR difference per system
    # pie chart of WR% per system

def input_which(length):
    command = input(f"[1 - {len(length)}, all] ")
    try:
        return int(command) - 1
    except ValueError:
        return command

if __name__ == "__main__":
    user = user(input("Who? "))
    main = True
    while main:
        command = input("[system, run, sort end] ")
        if command == "system":
            system_analyser(user)
        elif command == "run":
            run_analyser(user)
        elif command == "sort":
            PB.sort = input("Which sorting method? [game, system, time, delta, %WR, %LB] ")
        elif command == "end": main = False