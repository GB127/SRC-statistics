from plots import *
from classe import *
import os

clear = lambda: os.system('cls')

def run_analyser(user):
    #TODO : Get which PB
    which = int(input(f"Enter a number from 1 to {len(user.PBs)} ")) -1
    PB = user.PBs[which]


    stat = True

    while stat:
        stat = input("[lb, pb, end] ")
        if stat == "lb":
            plot_leaderboard(PB, user.username)
        elif stat == "pb":
            plot_runs(PB, username, user.runs_PB(PB) )
        elif stat == "end":
            stat = False


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
    command = input("[all, 1]")
    if command == "all":
        pass
    if command == "1":
        run_analyser(user)