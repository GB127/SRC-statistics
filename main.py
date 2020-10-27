from user import user
from runs import leaderboard, PB


if __name__ == "__main__":
    user = user(input("Which sr user? "))
    use = True
    while use:
        print("What do you want to do?")
        command = input("[PBs, systems, saves, sort, end] ")
        if command == "sort":
            print("What will be the new sorting method?")
            PB.sort = input("[deltaWR, game, PB#, saved, system, time, %WR, %LB, %Saved] ")
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