from user import user
import os
clear = lambda: os.system('cls')


def command_select(iterable, printer=True):
    while True:
        try:
            commant = input(f"Which option? [1 - {len(iterable)}]")
            if int(commant) != 0:
                return iterable[int(commant) - 1]
            raise BaseException
        except:
            if commant != "end":
                pass
            else:
                return "end"

if __name__ == "__main__":
    clear()
    print("speedrun.com statistics fetcher, program written by Niamek")
    user = user("niamek")
    commands = []
    for attribute in user.__dict__.values():
        if not isinstance(attribute, str):
            commands.append(attribute)
    while True:
        selection = command_select(commands)
        if selection == "end":
            break
        else:
            selection()