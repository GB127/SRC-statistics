# Speedrun.com statistic fetcher : Version 2
Script written by Niamek.

# Preparation & Running the script:
First, follow this python installation guide if you don't have python : https://realpython.com/installing-python/

To run this program, open the folder in the terminal. See this if you don't know how : https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/


Once you have the folder opened on the correct terminal, type this to run the script and you're good to go!
>python main.py

Note : You'll likely need to install two modules I use for this script: the module requests and the matplotlib modules. Just type these in the terminal and hit enter:
>pip install requests
>
>pip install matplotlib

# Overview:
this script fetches all the runs made from a specified account on speedrun.com. With all the runs, the script will generate tables of statistics you can then analyse or look up. Statistics can range from simple percentage maths to a complete histogram.

Note : for most of the selection commands, you can type "end" too.

# Sections :
Here is the current tree:

- User
    - PBs
        - Leaderboard

    - Runs
    - Saves
    - Systems
    - Games

Note : Existing a section will come back to the "father section". 


# The user section : the main section
This section is the smallest section of the sections currently supported, but is the section that unites all the other sections.

It displays some general informations.
>Username ; # of PBs (Total time) ; # of runs (Total runs time) ; # of systems ; # of games

## Commands :
1. Open the PBs section
2. Open the Runs section
3. Open the Saves section
4. Open the Systems section
5. Open the Games section
6. end : End the script



# PBs section :
This section gather all the PBs of the specified user.

## The table:
> No of PB | System | Game | Category | time | Delta of PB-WR | Percentage relative to WR | Rank/Total runners | % of runners ranked under

- system : Systems of the PB
    - EXAMPLE : WII VC ; The PB is ran on the WII Virtual Console. 
- game : Game of the PB
    - EXAMPLE : Super Mario 64, Super Mario Bros., Donkey Kong Country, etc.
- category : Category of the PB
    - EXAMPLE : Any%, 100%, etc.
- level : Sort by level names
    - EXAMPLE : TODO
- time : sort by PB times
    - If run is over 24 hours, it will still display hours.
    - EXAMPLE : 1:50:07 ; The PB is One hour, 50 minutes and 7 seconds.
- delta_WR : Sort by difference of PB-WR
    - EXAMPLE : + 1:09:12 ; The PB is 1 hours, 9 minutes and 12 seconds behind the WR.
    - EXAMPLE : + 0:00:00 ; The PB is the WR.
- perc_WR : Sort by Percentage relative to WR
    - EXAMPLE : 100.00% : The PB is the WR.
    - EXAMPLE : 200.00% : The PB is twice the duration of the WR.
- place : place on the leaderboard
    - EXAMPLE : 48/60 : The PB is 48th on a leaderboard that has 60 speedrunners.
- perc_LB : Sort by percentage of people ranked under the user
    - EXAMPLE : 1/1 | 0.0% : The PB is not better than any speedrunners because it's the only run on the leaderboard.
    - EXAMPLE : 1/10 | 90.0% : The WR is better than 90% of the speedrunners.
    - EXAMPLE : 4/12 | 66.67% : 66.67 % of the speedrunners on the leaderboard are ranked under this PB.



## Commands:
### Change the sorting
- Change the sorting of the entire table.
    - system : Sort by systems
    - game : Sort by games
    - category : Sort by categories
    - level : Sort by level names
    - time : sort by PB times
    - WR : Sort by WR 
        - Note : WR times are not displayed on tabl)
    - delta_WR : Sort by difference of PB-WR
    - perc_WR : Sort by Percentage relative to WR
    - perc_LB : Sort by percentage of people ranked under the user

### Histogram of the PBs:
You have three kind of histogram available:
- WR%: Histogram of the Percentages of the WRs. Minimum will always be at least 100%
- delta_WR : Histogram of the difference of PB-WR
- time : Histogram of the PB times

### Leaderboard : Opening the leaderboard section
Selecting this command will ask you to select one PB. After selecting the PB, it will open the leaderboard section. Look for the leaderboard section further in this README.

# Runs section :
This section gather all the Runs of the specified user, including the obsoleted runs.

## The table:
> No of PB | System | Game | Category | time

- system : Systems of the PB
    - EXAMPLE : WII VC ; The PB is ran on the WII Virtual Console. 
- game : Game of the PB
    - EXAMPLE : Super Mario 64, Super Mario Bros., Donkey Kong Country, etc.
- category : Category of the PB
    - EXAMPLE : Any%, 100%, etc.
- time : PB times
    - If run is over 24 hours, it will still display hours.
    - EXAMPLE : 1:50:07 ; The PB is One hour, 50 minutes and 7 seconds.


## Commands:
### Change the sorting
- Change the sorting of the entire table.
    - system : Sort by systems
    - game : Sort by games
    - category : Sort by categories
    - level : Sort by level names
    - time : sort by Run times

### Histogram of the Runs:
There is only one format of histogram supported, so no selection is prompted here. The histogram of the times will be generated.

