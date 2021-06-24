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
Change the sorting of the entire table.
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

### Filter the data:
You have three options to filter the data while you are in the section.
- Enter a range (two numbers, separated by a "-") in order to take out all the entries of the table that aren't in the range. Be sure to sort before!
- Enter a single number to remove the specified entry from the list.
- reset : Remove the filters.

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
> System | Game | Category | time

- system : Systems of the PB
    - EXAMPLE : WII VC ; The run is ran on the WII Virtual Console. 
- game : Game of the run
    - EXAMPLE : Super Mario 64, Super Mario Bros., Donkey Kong Country, etc.
- category : Category of the run
    - EXAMPLE : Any%, 100%, etc.
- time : PB times
    - If run is over 24 hours, it will still display hours.
    - EXAMPLE : 1:50:07 ; The run is One hour, 50 minutes and 7 seconds.


## Commands:
### Change the sorting
Change the sorting of the entire table.
- system : Sort by systems
- game : Sort by games
- category : Sort by categories
- level : Sort by level names
- time : sort by Run times

### Histogram of the Runs:
There is only one format of histogram supported, so no selection is prompted here. The histogram of the times will be generated.

# Saves section
This section gathers all the PBs that have more than one run.

## The table:
>system | game | category | x | first | PB | perc1st

- system : Systems of the PB
    - EXAMPLE : WII VC ; The run is ran on the WII Virtual Console. 
- game : Game of the run
    - EXAMPLE : Super Mario 64, Super Mario Bros., Donkey Kong Country, etc.
- category : Category of the run
    - EXAMPLE : Any%, 100%, etc.
- X : Number of runs of this specific game - category.
    - EXAMPLE : 5 ; 5 runs on this game - category. In other words : 4 total improvements over the first run ever.
- first : The time of the very first PB of this game-category
    - EXAMPLE : 2:53:59 : the first PB is 2 hours, 53 minutes and 59 seconds.

- time : PB times and the total of time saved
    - EXAMPLE : 0:32:58 (-2:21:01) ; 
        - The current PB is 32 minutes and 58 seconds.
        - The current PB shaves 2 hours, 21 minutes and 1 seconds of the the very first PBs that was 2:53:59.
- perc1st : Percentage shaved
    - Example: 81.05 % : 81.05 % of the time is shaved.


## Commands:
### Change the sorting:
- system : Sort by system
- game : Sort by game
- category : Sort by category name
- X : Sort by Amount of time a category has been improved
- first : Sort by first PBs' times
- time : sort by current PBs' times.
- save : Sort by time saved of first PBs
- perc1st : Sort by percentage saved.




### Filter the data:
You have three options to filter the data while you are in the section.
- Enter a range (two numbers, separated by a "-") in order to take out all the entries of the table that aren't in the range. Be sure to sort before!
- Enter a single number to remove the specified entry from the list.
- reset : Remove the filters.

### Plot 1 game's saves:
Selecting this command will then ask you to select one PB to plot. This will plot the progression of the PB, from the first PB to the last run submitted.

NOTE : If you have run(s) not accepted yet that is better than your accepted run, the plot will differ from the table because  they are included in the plot.

### Plot all saves:
This will generate a giant plot that will plot all the saves. Expect to witness a giant spaghetti if the user has a lot of runs. I made this because it's fun.

### Histogram of the Saves:
You have three kinds of histogram available:
- PB%: Histogram of the Percentages shaved. Maximum will always be at least 100%
- Improvements : Histogram of the differences of PB-first run
- time : Histogram of the PB times
    - Note: The difference here vs. the PB section is that this will include only PBs that have at least one improvements.

# Systems section:
This gathers all the runs and regroup them by system.

## The table:
> System | # Runs ; Total Runs | # PBs ; Total PBs (+ Total delta WR-PB)
>
>        |    Average run time |        Average PB (Average delta WR-PB)

- System : System
- Quantity of runs : How many runs are ran on this system
- Total runs : Total time of runs ran on this system
- Average run time : Average time of runs ran on this system
- Quantity of PBs : How many Pbs on this system
- Total PBs : Total time of PBs on this system
- Total delta WR-PB : Total deltas Wr-PB on this system
- Average PB : Average PBs on this system
- Average delta WR-PB : Average of deltas Wr-PB on this system
  

## Commands:
### Change the sorting:
- system : Sort by system.
- Run_count : Sort by Total runs amount
- Run_Total : Sort by total runs time 
- Run_average : Sort by Run average
- PB_count : Sort by total PBs amount
- PB_Total : Sort by total PBs time
- PB_average : Sort by PBs average
- WR_Total : Sort by Total WR time
    - Not displayed on the table
- PB_Total_delta : Sort by total delta of PB-WR

### Filter the data:
You have three options to filter the data while you are in the section.
- Enter a range (two numbers, separated by a "-") in order to take out all the entries of the table that aren't in the range. Be sure to sort before!
- Enter a single number to remove the specified entry from the list.
- reset : Remove the filters.

### Pie the table:
Two informations can be generated in a pie: the frequency of the runs (X) and the total time. The pies will always have both the runs' pie and the PBs' pie.

# Games section:
This section gathers all the PBs and split them by games.

## The table:
> Game | # | Run total | # | PB total (delta PB-WR) | WR%

- Game : Game name
    - EXAMPLE : Super Mario 64, Donkey Kong Country
- Quantity of runs : How many runs on a specific game
    - 5 ; 5 runs are made on this game
- Run total : Total time of all runs on a specific game
    - 4:35:02 ; Total time of all the runs on the specific game
- Quantity of PBs : How many PBs on a specific game
    - 4 : The user have 4 PBs in this game.
- PB Total (delta PB-WR):
    - Total PB time on a specific game
        - EXAMPLE : 1:28:12 : The combined time of all the PBs of the user on this game is one hour, 28 minutes and 12 seconds.
    - Total delta PB-WR on a specific game
        - EXAMPLE : (+3:10:41) ; The total time of deltas PB-WR is 3 hours, 10 minutes and 41 seconds.
- WR% : Percentage of PBs times vs. WR.
    - EXAMPLE : 200.0% : All the times of this game is 2x longer the total time of the WRs.


## Commands:
### Change the sorting:
- game : Sort by game
- Run_count : Sort by Amount of runs
- Run_Total : Sort by total runs time
- PB_count : Sort by PBs
- PB_Total : Sort by Total PBs time
- PB_Total_delta : Sort by total delta of PB-WR
- WR_Total : Sort by total WRs
    - WRs aren't displayed on the table
- PB_perc
    - Sort by PB percentage relative to WR

### Filter the data:
You have three options to filter the data while you are in the section.
- Enter a range (two numbers, separated by a "-") in order to take out all the entries of the table that aren't in the range. Be sure to sort before!
- Enter a single number to remove the specified entry from the list.
- reset : Remove the filters.


# Leaderboard section:
This section gathers the leaderboard of the selected game on the specific category (and level).

## the table:
> time | delta | perc | moy_rank

- time : time of the leaderboard entry
    - EXAMPLE : 1:13:50 ; This entry's run is 1 hours, 13 minutes and 50 seconds long.
- delta : difference of the entry compared to the first entry
    - EXAMPLE : 0:00:00 ; This run is the WR (unless the difference is smaller than one second)
    - EXAMPLE : 0:01:01 ; This run is 1 minutes and 1 second slower than WR.
- perc : Percentage of this run compared to the WR.
    - EXAMPLE : 200.0 % The run is twice as long as the WR.
    - EXAMPLE : 100.0 % : This run is the WR.
- moy_rank : Average time to save in order to gain one rank on the leaderboard.
    - NOTE : The average can be very very small if there are a lot of runs and/or not a big difference from WR.
    - EXAMPLE : 0:00:05 ; On average, 5 seconds will improve this entry's rank by one. Improving this run by 25 seconds COULD improve the rank by 5.
    - EXAMPLE : 0:00:00 : Either it's the WR, either the average is smaller than 1 second.

## Commands:


### Truncate the data:
You have two options to filter the data while you are in the section.
- Enter the number of the last entry you want to keep. The script will  take out all the entries of the table that below the number.
- reset : Untruncate the data.



### Plot the leaderboard evolution:
This command will plot the leaderboard line for each year since the earliest run on the leaderboard. If there are 2 lines, it means there are only 2 years to plot (so the earliest run is 2 years old.)

### Plot the position:
This command will plot the current leaderboard with a dot of the position of the user.