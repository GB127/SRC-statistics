from plots import *
from classe import *
import os

clear = lambda: os.system('cls')

def run_analyser(user):
    #TODO : Get which PB


    stat = True
    commands = ["Plot leaderboard", "Plot PB progression", "end"]

    while stat:
        for no, command in enumerate(commands): print(no, command)
        stat = commands[input_which(commands)]
        if stat == "Plot leaderboard":
            plot_leaderboard(PB, user.username)
        elif stat == "Plot PB progression":
            plot_runs(PB, username, runs )
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
    command = input("[all, one]")
    if command == "all":
        pass
    if command == "one":
        run_analyser(user)