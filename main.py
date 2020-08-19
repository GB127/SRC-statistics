from plots import *
from classe import *
import os

clear = lambda: os.system('cls')

def run_analyser(user):
    which = int(input(f"Enter a number from 1 to {len(user.PBs)} ")) -1
    PB = user.PBs[which]

    plot_leaderboard(PB, user.username)
    plot_runs(PB, user.username, user.runs_PB(PB) )

def user_analyser(user):




    plot_user_pies_systems(user)


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
    user = user(input("Who? "))
    main = True
    while main:
        clear()
        user.table_PBs()
        command = input("[all, 1, end] ")
        if command == "all":
            user_analyser(user)
        elif command == "1":
            run_analyser(user)
        elif command == "end": main = False