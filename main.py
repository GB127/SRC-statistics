from user import user

if __name__ == "__main__":
    user = user(input("Which sr user? "))
    use = True
    while use:
        print("What do you want to do?")
        command = input("[PBs, systems,sort, end] ")
        if command == "PBs":
            user.table_PBs()
            command2 = input(f"[0 - {len(user.PBs)}, all]")
            if command2 == "all":
                user.histo_runs()
                user.plot_all_runs()
            if command2 != "all":
                user.plot_runs(user.PBs[int(command2)-1])
                user.plot_PB_leaderboard(user.PBs[int(command2) -1])
        if command == "systems":
            user.table_systems()
            command2 = input(f"[0 - {len(user.systems)}, all]")
            if command2 == "all":
                user.pie_systems()
            if command2 != "all":
                user.histo_system(user.systems[int(command2)-1])
        if command == "end":
            use = False