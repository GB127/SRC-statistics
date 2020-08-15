from plots import *
from classe import *
import os

clear = lambda: os.system('cls')

def run_analyser(user):
    which = int(input(f"Enter a number from 1 to {len(user.PBs)} ")) -1
    PB = user.PBs[which]

    plot_leaderboard(PB, user.username)
    plot_runs(PB, username, user.runs_PB(PB) )

def user_analyser(user):
    plot_userchart(user)


def input_which(length):
    try:
        return int(input(f"Enter a number from 1 to {len(length)}"))
    except ValueError:
        print("allo this is a test")

if __name__ == "__main__":
    username = input("Who? ")
    user = user(username)
    clear()
    user.table_PBs()
    main = True
    while main:
        command = input("[all, 1, list, end] ")
        if command == "all":
            user_analyser(user)
        elif command == "1":
            run_analyser(user)
        elif command == "list":
            clear()
            user.table_PBs()
        elif command == "end": main = False