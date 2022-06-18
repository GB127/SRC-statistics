# SRC-Statistics
This script fetches data from SRC's free api (as of time of writting). With the data fetched, it will calculate some statistics and display them on the terminal or on a qt application.

The entire project is written by Niamek.

<b>API link:</b>
+ Base link: https://www.speedrun.com/api/v1
+ Documentation : https://github.com/speedruncomorg/api/tree/master/version1


## Development:
For future features requests or to report a bug, create an issue on the project's github page.
>link: https://github.com/GB127/SRC-statistics/issues

# Current version : V4:
Note : I know there are some issues on the displaying.
- Tables of levels aren't perfectly done.
- Some graphics should get a title.

# Installation required before using the script
Before using the script, you need to have python 3.10 installed on the computer. 
- WINDOWS : https://phoenixnap.com/kb/how-to-install-python-3-windows
- MAC : https://docs.python-guide.org/starting/install3/osx/

>I'm not 100% sure if any Python 3 version will work since the interpreter I have is 3.10. If you have any python 3 versions, you can try it first before updating.

Currently, to use this script and to install requirements, you'll need to know how to run a file from the command line. Here's how to open a command line in the folder of the script:
- WINDOWS : https://www.lifewire.com/open-command-prompt-in-a-folder-5185505
- MAC : https://www.maketecheasier.com/launch-terminal-current-folder-mac/

After installing python 3, you'll need to install some modules on the computer.
Here are the three modules the script needs in order to work correctly:
- pyqt5
- matplotlib
- requests

Here is the command you need to type in the command line to install all of them at once: `pip install requests pyqt5 matplotlib`.
If you are on MAC, you'll need to type this: `pip3 install requests pyqt5 matplotlib`.

# Using the script
To use the script, you'll need to open the terminal on the folder of the script and type `python main.py`. If you are on a MAC, you will need to write `python3 main.py`. You will be prompted to enter a SRC username. It can take a couple of time before the command line gets updated with the infos fetched. The more a user has runs, the longer it can be.

# Full description of the features
Coming soon!