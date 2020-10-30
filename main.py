from user import user
from tools import entry_selecter
from runs import leaderboard, PB
import os

clear = lambda: os.system('cls')


if __name__ == "__main__":
    print("speedrun.com statistics fetcher, program written by Niamek")
    user = user(input("Which sr user? "))
    clear()
    use = True
    while use:
        clear()
        print("What do you want to do?")
        command = input("[lb, PBs, systems, saves, sort, end] ")
        clear()
        if command == "sort":
            print("What will be the new sorting method?")
            PB.sort = input("[deltaWR, game, PB#, saved, system, time, %LB, %Saved, %WR] ")
        elif command == "lb":
            user.table_PBs()
            command2 = int(input(f"[0 - {len(user.PBs)}]")) - 1
            tempo = leaderboard(user.PBs[command2])
            tempo.plot_leaderboards()
            del tempo         
        elif command == "PBs":
            user.table_PBs()
            command2 = entry_selecter(user.PBs)
            if command2 == "all":
                user.histo_PBs_WR()
                user.histo_runs()
            if command2 != "all" and command2:
                user.plot_PB_leaderboard(command2)
        elif command == "systems":
            user.table_systems()
            command2 = entry_selecter(user.systems)
            if command2 == "all":
                user.pie_systems()
            if command2 != "all" and command2:
                user.histo_system(command2)
        elif command == "saves":
            user.table_saves()
            command2 = entry_selecter(user.fetch_nosolo_PBs())
            if command2 == "all":
                user.histo_saves()
                user.plot_all_runs()
            if command2 != "all" and command2:
                user.plot_saves_PB(command2)

        elif command == "end":
            print("speedrun.com statistic fetcher, program written by Niamek")
            use = False