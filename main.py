from user import user
from tools import command_select, clear

if __name__ == "__main__":
    clear()
    print("speedrun.com statistics fetcher, program written by Niamek")
    user = user(input("Who? "))
    commands = []
    for attribute in user.__dict__.values():
        if not isinstance(attribute, str):
            commands.append(attribute)

    while True:
        clear()
        print(user)
        for no, attribute in enumerate(commands):
            print(f'{no + 1} : {attribute}')
        selection = command_select(commands, printer=True)
        if selection == "end":
            break
        else:
            selection()
