import numpy
import matplotlib.pyplot as plot

from api import *
from tools import run_time, percent
from runs import Run, PB


class user:
    def __init__(self, username):
        """
            Class of a Speedrun.com user. The class contains informations such as username, runs, etc.

            Args:
                username (str) : Username on speedrun.com
        """
        self.username = username
        self.ID = get_userID(self.username)

        print("user initialized!")

if __name__ == "__main__":
    test = user("niamek")
