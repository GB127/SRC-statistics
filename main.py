from plots import *
from classe import *

if __name__ == "__main__":
    user = user("malzakiel")
    user.table_PBs()
    command = True
    while command != "end":
        command = input("[lb]")
        if command == "PBs": user.table_PBs()
        if command == "lb":
            which = int(input("Please enter a number")) -1
            plot_leaderboard(user.PBs[which].gameID,
                            user.PBs[which].categID,
                            PB=user.PBs[which],
                            username=user.username)

    print("Script ended, thank you!")