from plots import *
from classe import *
import os

clear = lambda: os.system('cls')

def run_analyser(PB, username):
    stat = True
    while stat:
        stat = input("What do you want to do?")
        if stat == "lb":
            plot_leaderboard(PB, username)






if __name__ == "__main__":
    username = input("Who? ")
    user = user(username)
    clear()
    user.table_PBs()
    use = True
    while use:
        check = False
        while check is False:  # This while is to fetch which run to analyse
            try:
                which = int(input("Which Run & Category do you want to analyse? "))-1
                assert which > 0 and which < len(user.PBs), "This is a test" 
                clear()
                check = True
            except AssertionError:
                print(f"Number must be in the range of 1-{len(user.PBs)}")
            except ValueError:
                print(f"Input must be a number in the range of 1-{len(user.PBs)}")
        print(user.PBs[which])
        run_analyser(user.PBs[which], username)