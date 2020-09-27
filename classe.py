import datetime
import isodate
import matplotlib.pyplot as plot
import numpy
from api import *
from tools import *

class user:
    def __init__(self, username):
        """
            Class of a Speedrun.com user. The class contains informations such as username, runs, etc.

            Args:
                username (str) : Username on speedrun.com

            Attributes created:
                user.all_systems (list): List of all systems in which the user has a PB.
                user.ID (string) : User ID attributed by speedrun.com, fetched with a api request
                user.PBs (list) : List that contains *all* PBs of the user that aren't rejected.
                    All elements of this list are PB objects. Data collected with a request.
                user.rejected (dicto) : Dicto that tracks how many runs aren't
                    elligible for my stats analysis. The runs not elligible are
                    individual levels and runs shorter than 3 minutes.
                    - I decided to not include the individual levels runs because they
                        usually are very short and doesn't complete the game. I personally prefer
                        runs that actually complete the games or that does a significant part of the game.
                    - I don't include runs shorter than 3 minutes because I don't consider them long enough to be
                    worthy of analysis. I also noticed that most of these runs shorter than 3 minutes are meme runs
                    or meme games... Probably runs that wouldn't be (generally) accepted under current speedrun.com rules. 
                    - Obviously, not all runs that are "normal runs" fall under these criteria. Excluding these runs requires case
                        by case analysis, which is impossible to do because of the sheer number of games/categories.

                    Keys:
                        "level" : Quantity of individual levels (int)
                        "time" : Quantity of runs under of three minutes (int)
                user.runs (list) : List that contains *all* runs of the user that aren't rejected.
                    All elements of this list are Run objects. Data collected with a request.
                user.systems_PBs : Infos of user.PBs, grouped by systems.
                    hierachy:
                        "system" (dicto)
                            "count" (int): How many run on the said system.
                            "time" (int) : Summation of all PBs on the said system, in seconds.
                            "WR" (int) : Summation of all WRs on the said system, in seconds.
                            "delta" (int) : Summation of all deltas of WR on the said system, in seconds.
                user.systems_runs : Infos of user.runs, grouped by systems only.
                    hierachy:
                        "system" (dicto)
                            "count" (int): How many run on the said system.
                            "time" (int) : Summation of all runs on the said system, in seconds.
                user.total_PB (int) : Summation of all PB times of the user, in seconds.
                user.total_WR (int) : Summation of all Run times of the user, in seconds.
                user.username (string): Username of the user
        """
        def maker_runs_list(toupdate, list_runs, typ):
            """Function to update liste with runs.

            Args:
                toupdate (List): List to update
                list_runs (List): List of runs to verify
                typ (str): Determine if PB or run
            """

            for run in list_runs:
                if typ == "Run":
                    level = run["level"]
                    time = run["times"]["primary_t"]
                elif typ == "PB":
                    level = run["run"]["level"]
                    time = run["run"]["times"]["primary_t"]
                if level is None and time > 180:
                    if typ == "PB":
                        toupdate.append(PB(run))
                    elif typ == "Run":
                        toupdate.append(Run(run))
                elif level is not None and typ =="Run":
                    self.rejected["level"] += 1
                elif typ == "Run":
                    self.rejected["time"] += 1

        def runs_splitter_system(runs):
            tempo = {}
            try:
                for run in runs:
                    tempo[run.system]["count"] += 1
                    tempo[run.system]["time"] += run.time
                    if type(run) == PB:
                        tempo[run.system]["WR"] += run.WR    
                        tempo[run.system]["delta"] += run.delta
            except KeyError:
                if type(run) == PB:
                    tempo[run.system] = {"count" : 1,
                                         "time" : run.time,
                                         "WR" : run.WR,
                                         "delta" : run.delta}
                else:
                    tempo[run.system] = {"count" : 1,
                                         "time" : run.time}

            return tempo
        print("Fetching data...")  # Printing this because the fetching can take a couple of minutes.

        self.username = username
        self.ID = get_userID(self.username)
        self.runs, self.PBs = [], []
        self.rejected = {"level": 0, "time": 0}

        maker_runs_list(self.PBs,
                        get_PBs(self.ID),
                        typ="PB")
        maker_runs_list(self.runs,
                        get_runs(self.ID),
                        typ="Run")

        self.total_PB = sum([pb.time for pb in self.PBs])
        self.total_WR = sum([pb.WR for pb in self.PBs])
        self.total_run = sum([run.time for run in self.runs])

        self.systems_PBs = runs_splitter_system(self.PBs)
        self.systems_runs = runs_splitter_system(self.runs)
        self.systems = sorted(list(self.systems_PBs.keys()))
        print("user initialized!")

    def __str__(self):
        """ Format: username, # runs, # PBs
            """
        return f'{self.username}, {len(self.runs)} runs, {len(self.PBs)} PBs'

    def table_PBs(self):
        """ Print a table by printing all PBs. Sorting can be changed by
            changing the PB.sort variable.
        """
        self.PBs.sort()  # Always sort in case we change the sorting method?

        ### En tete of the table
        print("-"*120)
        print(f"| # |{'Sys':^6}| {'Game':^30}| {'Category':^15} | {'Time':^14}|      + \u0394WR     |{'%WR':^10}| {'  Rank      (^%)':20}")
        print("-"*120)
    
        ### Actual entry of the table.
        for no, PB in enumerate(self.PBs): print(f'{no+1:3} {PB}')
        print("-"*122)

        ### Foot of the table
        print(f'{"Total :":10}| {str_time(self.total_PB)[:17]:17}| + {str_time(self.total_PB - self.total_WR)[:13]:20}|----------|')
        print(f'{"Average :":10}| {str_time(self.total_PB/len(self.PBs))[:17]:17}| + {str_time((self.total_PB - self.total_WR)/len(self.PBs))[:13]:20}| {str(round(self.total_PB/self.total_WR * 100,2))[:6]:6} % |')

    def table_systems(self):
        """Print a table of the infos of the runs of the user by systems.
            """
        self.all_systems.sort()

        print("-" * 85)
        print(f'|   | System |{" Runs":20}|{" PBs":49}|')
        print("-" * 85)

        for no,system in enumerate(self.all_systems):
            # Current system
            current_system = f'| {system[:6]:^6} |'
            # Runs count and time (coti) of the current system
            runs_coti = f'{self.systems_runs[system]["count"]:^4}| {str_time(self.systems_runs[system]["time"])[:13]:13} |'
            # Average of runs time
            runs_av_coti = f'{str_time(self.systems_runs[system]["time"]/self.systems_runs[system]["count"])[:13]:13} |'

            # PBs count, time, delta, and %WR (infos) of the current system
            PBs_infos = f'{self.systems_PBs[system]["count"]:^4}| {str_time(self.systems_PBs[system]["time"])[:13]:13} | + {str_time(self.systems_PBs[system]["delta"])[:13]:13} | {round(100 * self.systems_PBs[system]["time"] / self.systems_PBs[system]["WR"],2):6} % |'
            # PBs average of infos
            PBs_av_infos = f'{str_time(self.systems_PBs[system]["time"]/self.systems_PBs[system]["count"])[:13]:13} | + {str_time(self.systems_PBs[system]["delta"]/self.systems_PBs[system]["count"])[:13]:13} |'

            print(f'|{no+1:^3}{current_system}{runs_coti}{PBs_infos}')
            print(f'|   |{"|--- ":>13}| {runs_av_coti}{"---":^4}| {PBs_av_infos} -------- |')
            print("-"*85)

    def fetch_runs_system(self, system, PB=False):
        liste = []
        if PB is False:
            for run in self.runs:
                if run.system == system:
                    liste.append(run)
            return liste
        elif PB:
            for run in self.PBs:
                if run.system == system:
                    liste.append(run)
            return liste

    def fetch_runs_PB(self, PB):
        """
            Find all the runs for that PBs
        """

        #FIXME : Check vari too?
        toreturn = []
        for run in self.runs:
            if run.gameID == PB.gameID and run.categID == PB.categID:
                toreturn.append(run)
        return toreturn


class Run:
    sort = "time"

    def __init__(self, data):
        """
            Args:
                data ([json]): data from requests to speedrun.com

            Attributes:
                self.categID (string) : ID of the category ran
                self.emulated (bool): True if emulated, False if not emulated
                self.gameID (string): ID of the game ran
                self.ID (string): ID of the run
                self.system (string): System the run is on
                self.time (int): duration of the run, in seconds
                FIXME self.vari : "subcategories" of the category.
        """
        self.system = get_system(data["system"]["platform"])
        self.emulated = True if data["system"]["emulated"] else False
        self.ID = data["id"]
        self.gameID = data["game"]
        self.categID = data["category"]
        self.vari = data["values"]
        self.time = data["times"]["primary_t"]


    def __str__(self):
        """ Format: System|Game|Category|Time
            """
        return f'{self.system[:6]:^6}| {get_game(self.gameID)[:30]:30} | {get_category(self.categID)[:15]:15} | {datetime.timedelta(seconds=self.time)}'


    def __lt__(self, other):
        if get_game(self.gameID) != get_game(other.gameID):
            return get_game(self.gameID) <= get_game(other.gameID)
        elif get_category(self.categID) != get_category(other.categID):
            return get_category(self.categID) <= get_category(other.categID)
        else:
            return self.time <= other.time

class PB(Run):
    sort = "%WR"
    def __init__(self, data):
        """
            NOTES:
                Some extra infos not eally related to the PB 
                are stored because of the maths I want to do.

            New Attributes:
                self.delta (int): Time difference of PB compared to WR, in seconds. 
                self.place (int): Rank of the PB
                self.lenrank (int): Length of the leaderboard
                self.perclenrank (int): Percentage of people you beat in the leaderboard.
                    Note : If you are the only runner on the leaderboard, you will
                    have 0% even if you have the WR! This is because you don't beat anyone.
                    Will never be 100% because it doesn't count you : you ar emerely the threshold
                    for the maths.
                self.percWR (int): % of the WR. 100% means it's the WR. 200% means the time is exactly double
                    the WR
                self.WR (int): WR of the said run, in seconds)
        """
        super().__init__(data["run"])
        self.place = data["place"]
        self.lenrank = get_len_leaderboard(self.gameID, self.categID, self.vari)
        self.perclenrank = round(100 * (self.lenrank - self.place) / self.lenrank, 2)
        self.WR = get_WR(self.gameID, self.categID, self.vari)
        self.delta = self.time - self.WR
        self.percWR = round((self.time * 100/self.WR), 2)


    def __str__(self):  # FIXME : Documentate this
        def str_game(self):
            return f'|{self.system[:6]:^6}| {get_game(self.gameID)[:30]:30}| {get_category(self.categID)[:15]:15}'
        def str_rank(self):
            calculation = f'{self.place}/{self.lenrank}'
            calculation2 = f'({str(self.perclenrank):^5} %)'
            return str(f'{calculation:^9} {calculation2}')
        def str_times(self):
            return f'{str_time(self.time)[:13]:13} | + {str_time(self.delta)[:13]:13}| {self.percWR:^6} %'
        return f'{str_game(self)} | {str_times(self)} | {str_rank(self)}'


    def __lt__(self, other):
        if PB.sort == "game":
            return get_game(self.gameID) < get_game(other.gameID)
        elif PB.sort == "system":
            return self.system < other.system
        elif PB.sort == "time":
            return self.time < other.time
        elif PB.sort == "delta":
            return self.delta < other.delta
        elif PB.sort == "%WR":
            return self.percWR < other.percWR
        elif PB.sort == "%LB":
            return self.perclenrank > other.perclenrank

if __name__ == "__main__":
    test = user("pac")
    print(test)