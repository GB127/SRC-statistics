from classe import *
from api import *


if __name__ == "__main__":
    print("Fetching data, please wait...")
    user = runner("cheese")
    #user = runner(input("Which user name would you like to see? "))
    print("Fetching complete!")
    use = True
    while use:
        command = input("What would you like to do? ")
        if command == "plot":
            user.plot()
        if command == "plots":
            user.plot_all()
        if command == "exit" or command == "end":
            use = False
    print("Program terminated")