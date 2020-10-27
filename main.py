from user import user
from runs import leaderboard, PB
import os

clear = lambda: os.system('cls')


if __name__ == "__main__":
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
            command2 = input(f"[0 - {len(user.PBs)}, all]")
            if command2 == "all":
                user.histo_PBs_WR()
                user.histo_runs()
            if command2 != "all":
                user.plot_PB_leaderboard(user.PBs[int(command2) -1])
        elif command == "systems":
            user.table_systems()
            command2 = input(f"[0 - {len(user.systems)}, all]")
            if command2 == "all":
                user.pie_systems()
            if command2 != "all":
                user.histo_system(user.systems[int(command2)-1])
        elif command == "saves":
            user.table_saves()
            command2 = input(f"[0 - {len(user.PBs)}, all]")  #FIXME
            if command2 == "all":
                user.histo_saves()
                user.plot_all_runs()
            if command2 != "all":
                user.plot_saves_PB(user.PBs[int(command2)-1])

        elif command == "end":
            use = False