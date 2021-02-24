from user import user
import os
clear = lambda: os.system('cls')


if __name__ == "__main__":
    clear()
    print("speedrun.com statistics fetcher, program written by Niamek")
    #user = user(input("Which sr user? "))
    user = user("niamek")
    check = True
    while check:
        print(user)
        command = input("What do you want to do? ")
        if command == "end":
            check = False
        elif command == "PBs":
            clear()
            user.table_data(user.PBs)
        elif command == "Runs":
            clear()
            user.table_data(user.Runs)