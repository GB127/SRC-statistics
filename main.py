from plots import *
from classe import *

if __name__ == "__main__":
    user = user("pac")
    command = True
    while command != "end":
        command = "lb"
        if command == "lb":
            user.listPBs()
            which = 1
            plot_leaderboard(user.PBs[which].gameID,
                            user.PBs[which].categID,
                            PB=user.PBs[which],
                            username=user.username)



        command = "end"
    print("Script ended, thank you!")