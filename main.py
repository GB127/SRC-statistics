from user import user
from tools import command_select
from os import system

clear = lambda: system('cls')

if __name__ == "__main__":
    clear()
    print("speedrun.com statistics fetcher, program written by Niamek")
    user = user("niamek")
    commands = []
    for attribute in user.__dict__.values():
        if not isinstance(attribute, str):
            commands.append(attribute)
    while True:
        clear()
        selection = command_select(commands)
        if selection == "end":
            break
        else:
            selection()