# Speedrun.com statistic fetcher : Version 2.3
Script written by Niamek.

# Preparation & Running the script:
First, follow this python installation guide if you don't have python : https://realpython.com/installing-python/

To run this program, open the folder in the terminal. See this if you don't know how : https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/


Once you have the folder opened on the correct terminal, type this to run the script and you're good to go!
    python main.py

Note : You'll likely need to install two modules I use for this script: the module requests and the matplotlib modules. Just type these in the terminal and hit enter:
    pip install requests
    pip install matplotlib

# Overview:
this script fetches all the runs made from a specified account on speedrun.com. With all the runs, the script will generate tables of statistics you can then analyse or look up. Statistics can range from simple percentage maths to a complete histogram.

# The Main section : The user
This section is the smallest section of the currently available, but is the section that unites all the other sections.

Informations :
    Username ; # of PBs (Total time) ; # of runs (Total runs time) ; # of systems ; # of games

Commands :
    1 : Open the PBs section
    2 : Open the Runs section
    3 : Open the Saves section
    4 : Open the Systems section
    5 : Open the Games section