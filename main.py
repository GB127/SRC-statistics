from plots import *
from classe import *
import os

clear = lambda: os.system('cls')

def run_analyser(user):
    clear()
    user.table_PBs()
    which = int(input(f"Enter a number from 1 to {len(user.PBs)} ")) -1
    PB = user.PBs[which]

    plot_leaderboard(PB, user.username)
    plot_runs(PB, user.username, user.runs_PB(PB) )

def system_analyser(user):
    clear()
    user.table_systems()


    plot_systems(user)


    # Emu vs. non-emu


    # pie chart of WR difference per system
    # pie chart of WR% per system
    # Histogram as well
    # Histogram as well

def input_which(length):
    try:
        return int(input(f"Enter a number from 1 to {len(length)}"))
    except ValueError:
        print("allo this is a test")

if __name__ == "__main__":
    #user = user(input("Who? "))
    user = user("baffan")
    main = True
    while main:
        clear()
        command = input("[system, run, sort end] ")
        if command == "system":
            system_analyser(user)
        elif command == "run":
            run_analyser(user)
        elif command == "sort":
            PB.sort = input("Which sorting method? [game, system, time, delta, %WR, %LB] ")
        elif command == "end": main = False