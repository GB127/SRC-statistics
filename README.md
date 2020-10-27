# Speedrun.com statistics fetcher

Python script that fetches data from speedrun.com's API to plot graphs (histograms or simple plot) or to display tables.

The program divides the stats into the following categories:
+ PBs
    + Category that covers all PBs and compares them to the leaderboard and WR.
+ Systems
    + Category that covers all systems stats of the said user.
+ Saves
    + Category that covers runs improvements.

The details of each categories will be covered further in the README.

# How to use the script:
First you must have python 3.8 installed in your computer. To run the program, you need to learn how to run a script from a command line (the black windows stuffs). In the future I will try to make it more user friendly, but I have other projects I'm interested in working on.

Running the script will first ask you which user you wish to analyse.
> Which sr user?

Type the speedrun username you want to analyse, then hit "enter".
> Which sr user? niamek

The script will then be fetching data and can't accept commands during the process.**The more run the user have, the longer the process will be.**
> Fetching data...

Once the process is done, you will be asked an option from the "main menu".
> What do you want to do?
> [PBs, systems, saves, sort, end]

Type down the category you want to display data. **The commands are case sensitives**.
> What do you want to do?
> [PBs, systems, saves, sort, end] PBs

# PBs
# systems
# saves
This category of data will show statistics regarding the improvements of your PBs. For this category, all runs that have only one attempt are omitted. A table will be listed, and then you will be asked to select an entry of the table or all of them.
> [0 - 19, all]
Selecting a single entry will make a plot of the progression of the PBs.
Selecting all of them will combine every plots into a single plot.

## The table
Selecting this category will print a table with all runs you have submitted to speedrun.com that have more than 1 attempt. The following infos are displayed in culumns in the table:
+ game : Game of the run
+ Category : category of the run
    + A current issue with my table is that it doesn't display the differences of two PBs of a game that has a same category, but a different subcategory. They will have all the same category, but, in the background, the script makes a distinction between all of them.
    + Example : https://www.speedrun.com/alttp
        + All runs of the No Major Glitches will be listed as the same category "No Major Glitches".
+ Number : This is the number of personal bests you have in this category.
+ First PB : This is the first PB of the category.
+ Current PB : This is the current PB of the category.
+ Saved (%) : Amount of time saved and the percentage saved.
    + - 0:05:00 (5.00 %) => 5 minutes saved since first PB, representing 5.00 % of First PB.

At the foot of the table:
+ The total time of the first runs, and the total of time saved is displayed.
+ The average time of the first runs, and the average of time saved is displayed.
+ the total of runs that don't have more than one attempt will be displayed, as well as the total of time.

## The single plot:
Title of the plot is the username of the runner as well as the selected game and category.

The plot is the progression of your times (y axis) over the number of PBs (x axis). The yellow line at the bottom is the **current** WR.

Legend is the current WR.

Notice : The WR does change over time, making the gap between PB and WR not always consistent. Making the changes in the plot will increase the data fetching time. I opted to not consider it in the plot.


## The combined plots
Two plots will be drawn. One appearing at a time. First an histogram will be created.

### The histogram:
The histogram combines two histograms : The histogram of all the first PBs and the histogram of all the current PBs. The histograms represent the frequency of a time.

Title of the graphic is the runner and the number of PBs that has saves.

Red histogram : Represent all the first PBs together.
Green histogram : Represent all the current PBs together.

Overall, the green bars should be more to the left than the red bars, showing the improvements. Note that if runs with smaller improvements will have a good chance to appear on the same time bar and not shift to a different time bar.

## The combined PB progressions plot
The runs with saves are divided in four plots with different time frames to minimize a crushed look. This plot combines all the single plots.

# sort
# end
This command ends the script.