# SRC-Statistics
This script fetches data from SRC's free api (as of time of writting). With the data fetched, it will calculate some statistics and display them on the terminal or on a qt application.

The entire project is written by Niamek.

<b>API link:</b>
+ Base link: https://www.speedrun.com/api/v1
+ Documentation : https://github.com/speedruncomorg/api/tree/master/version1


## Development:
For future features requests or to report a bug, create an issue on the project's github page.
>link: https://github.com/GB127/SRC-statistics/issues

# Current version : Beta-V3:
The version is beta because it doesn't have *some* features from old versions.

Improvements from older version from user's perspective :
  + Considerably faster data collection from SRC's API. It is also much more efficient.
  + It's faster to change data charted if same type of chart used 
    + (example : pie chart of games -> pie chart of systems)

I plan to reimplement the lost features. I'm however taking a small break from this project right now. To get access to the lost features, just download an older version for now.

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

# User
The full runs and the individual runs are separated into two seperate data for analysis. Here is the current format:
+ User
  + Full game Runs
  + Full game PBs
  + Individual level Runs
  + Individual level PBs

You will be asked to select one of these datas with entering a number. The script will open the selected data.

Sample:
>   Niamek<br>
    Full runs:<br>
    124 Runs     (201:11:21)  :   60 PBs    (118:31:37)<br>
    0 pbs<br>
    1 runs<br>
    Select option: [0-1] | Type end to exit<br>
    Input : ▯

Here is an example that opens PBs by typing 0, then press enter. Here how the last line should looks:
>Input: 0

To exit the script, either close the window, or type end and press enter.
>Input: end
# Tables in general
All tables in the script will display the entries of the table line by line. Then, it will display the sum of each columns except *some* columns. And finally, it will calculate the mean and the geometric mean of each columns except *some* columns.

## Runs:
Format of a single entry:
>System Game [level] Category (Subcategory) time

Example of a single run's entry in the displayed table (not adjusted to how the display is on the command line):
>NES    Super Mario Bros.      Warpless                           2:53:59
+ System : NES
+ Game : Super Mario Bros.
+ level : Not a level, so it is not displayed.
+ Category : Warpless
+ Time : 2:43:59

Available commands:
+ Histo : Open the window application illustrating the histograms of the datas. More infos on the histogram section.
+ pie : Open the window application illustrating the pie charts of the data. More infos on the pie charts section.
+ sort : Sort the data of the table.

## PBs:
Format of a single entry:
>System Game [level] Category (Subcategory) WRtime PBtime +DeltaWR WR% place/leaderboard %LB
+ WRtime : Time of the WR.
+ PBtime : Time of the Personal Best of the user.
+ DeltaWR : Represents the difference of the PB compared to the WR.
  + PBtime - WRtime
+ WR% : Represents the percentage of the PB, comapred to the WR.
  + Formula : (PBtime) / WRtime
  + Example : 200% : The PB is 2 times longer than WR.
+ %LB : Represent the percentage of people the PB beats. In other words, it's the % of people that are slower than the PB.
  + Formula : (leaderboard - place)/leaderboard
  + Example : 50% : The PB beats 50% of the people on the leaderboard.

Example of a single run's entry in the displayed table (not adjusted to how the display is on the command line):
>NES    Super Mario Bros.      Warpless                 0:18:56    0:32:58 +0:14:01   (173.98%)    296/321   7.79%

DeltaWR WR% place/leaderboard %LB

+ System : NES
+ Game : Super Mario Bros.
+ level : Not a level, so it is not displayed.
+ Category : Warpless
+ subcategory : Don't have a subcategory. It is therefore not displayed.
+ WRtime : 0:18:56
+ PBtime : 0:32:58
+ DeltaWR : The PB is 0:14:01 behind the WR
+ WR% : The PB is 173,98% the WR.
+ place/leaderboard : The PB is 296th on the leaderboard that has 321 entries.
+ %LB: The runs beats 7,79% of the people on the leaderboard. In other words, 7,79% represents the 25 peoples that are slower than the PB.

Available commands:
+ Histo : Open the window application illustrating the histograms of the datas. More infos on the histogram section.
+ pie : Open the window application illustrating the pie charts of the data. More infos on the pie charts section.
+ sort : Sort the data of the table.

# Histogram:
The Histogram window displays an histogram on the right. The data displayed is specified on the title of the histogram. On the Y axis, it is always the frequency. On the X axis, it is always the specified data on the title.

>Example: PB - time => The histogram is an histogram of the PBs, according to their time (x axis is therefore time).

To change the histogram, simply press on one of the button on the bottom.

To exit the window and return to the last section, simply close by clicking on the x.

## Trimming the data
In order to make the histogram more pleasing to look and more informing, the data is trimmed to removing extreme datas. Doing this allows the program to display an histogram that use the most of the space availabe instead of grouping most of the data on a single bar.

The trimmed datas are colored in red on list displayed on the left. The green datas are on the histogram.

The triming formula is a recursive trimming using the InterQuantile Range method. It will trim using this method until it doesn't remove data.

# Pie charts:
The Histogram window displays an ie chart on the right. The data represented is specified on the title of the histogram. The colors on the pie are reused in the list on the left. To change the chart, press on one of the buttons on the bottom. Datas lower than 5% are grouped together in "others".

>Example : PBs - game => Means the pie chart represents the games proportions in the PBs by frequency.

To exit the window and return to the last section, simply close by clicking on the x.
