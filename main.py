from user import user
import os
clear = lambda: os.system('cls')


if __name__ == "__main__":
    clear()
    print("speedrun.com statistics fetcher, program written by Niamek")
    #user = user(input("Which sr user? "))
    user = user("lackattack")
    print(user)