from generic import Entry, Filtered_Entry, table
from api import requester

class Leaderboard(table):
    def __init__(self, IDs, level=False):
        def get_leaderboard(IDs):
            """Fetch the leaderboard data from SRC.

                Args:
                    IDs (list) : List of IDs (str).
                        format : [Gameid, level_id/category_ID, subcategories_ID]
                """
            subcategories = ""
            if len(IDs) == 3:
                subcategories = "?" + "&var".join([f'var-{variable}={selection}' for variable, selection in IDs[2]])
            category = f"category/{IDs[1]}"
            rep = requester(f"/leaderboards/{IDs[0]}/{category}{subcategories}")
            return rep["data"]
        data = get_leaderboard(IDs)

        super().__init__(Ranking, data["runs"], level)
        for rank in self.data:
            rank.__dict__["WR time"] = self.data[0].time
            rank.__dict__["delta time"] = rank.time - rank.__dict__["WR time"]
            rank.__dict__["%"] = rank.time / rank.__dict__["WR time"]

class Run(Entry):
    str_order = ["system", "game", "category", "time"]
    def __init__(self, data):
        super().__init__(data)
        self.__dict__["time"] = data["times"]["primary_t"]
        for unwanted in ["weblink", "videos", "comment","times", "links", "splits", "submitted", "players", "id", "status"]:
            try:
                del self.__dict__[unwanted]
            except KeyError:
                continue

class Ranking(Run):
    str_order = ["place", "time","delta time", "%"]
    def __init__(self, data):
        corrected_data = data["run"]
        corrected_data["place"] = data["place"]
        super().__init__(corrected_data)

    def __add__(self, other):
        tempo = super().__add__(other)
        tempo.__dict__["%"] = tempo.time / tempo.__dict__["WR time"]
        return tempo

    def __truediv__(self, other):
        tempo = super().__truediv__(other)
        tempo.__dict__["%"] = tempo.time / tempo.__dict__["WR time"]
        tempo.place = int(tempo.place)

        return tempo

class PB(Ranking):
    str_order = ["system", "game", "category", "time", "WR time","delta time", "%", "place", "LB", "% LB"]
    def __init__(self, data):
        tempo = [data["run"]["game"], data["run"]["category"]]
        super().__init__(data)
        self.leaderboard = Leaderboard(tempo + [self.sub_IDs])
        self.__dict__["WR time"] = self.leaderboard[0].time
        self.__dict__["delta time"] = self.time - self.__dict__["WR time"]
        self.__dict__["%"] = self.time / self.__dict__["WR time"]
        self.__dict__["LB"] = len(self.leaderboard)
        self.__dict__["% LB"] = (len(self.leaderboard) - self.place) / len(self.leaderboard)

    def __truediv__(self, other):
        tempo = super().__truediv__(other)
        tempo.__dict__["LB"] = int(tempo.__dict__["LB"])
        tempo.__dict__["% LB"] = (tempo.LB - tempo.place) / tempo.LB
        return tempo

    def __add__(self, other):
        tempo = super().__add__(other)
        tempo.__dict__["% LB"] = (tempo.LB - tempo.place) / tempo.LB
        return tempo

class Saves(table):
    def __init__(self, PBs, Runs):
        self.data = []
        for pb in PBs:
            same_categ = []
            for run in Runs:
                if run.game == pb.game and run.category == pb.category:
                    same_categ.append(run)
            if len(same_categ) > 1:
                self.data.append(Save(pb, same_categ))

class Save(Entry):
    str_order = ["game", "category","#", "1st time", "PB time", "Saved time", "%"]
    def __init__(self, PB, Runs):
        self.game = PB.game
        self.category = PB.category
        self.PB = PB
        self.Runs = Runs
        self.__dict__["PB time"] = PB.time
        self.__dict__["1st time"] = max([x.time for x in self.Runs])
        self.__dict__["Saved time"] = self.__dict__["1st time"] - self.__dict__["PB time"]
        self.__dict__["%"] = (self.__dict__["1st time"] - self.__dict__["PB time"])/self.__dict__["1st time"]
        self.__dict__["#"] = len(self.Runs)


    def __str__(self):
        return super().__str__()

    def __add__(self, other):
        tempo = super().__add__(other)
        tempo.__dict__["%"] = (tempo.__dict__["1st time"] - tempo.__dict__["PB time"])/tempo.__dict__["1st time"]
        return tempo
    def __truediv__(self, other):
        tempo = super().__truediv__(other)
        tempo.__dict__["%"] = (tempo.__dict__["1st time"] - tempo.__dict__["PB time"])/tempo.__dict__["1st time"]
        return tempo


if __name__ == "__main__":
    test = {'place': 58, 
            'run': {
                'id': 'y659ro0z',
                'weblink': 'https://www.speedrun.com/goof_troop/run/y659ro0z',
                'game': 'y65lq71e',
                'level': None,
                'category': '7dgv34d4',
                'videos': {'links': [{'uri': 'https://www.youtube.com/watch?v=j6IDNjDFi48'}]}, 'comment': None, 'status': {'status': 'verified', 'examiner': '18vnevjl', 'verify-date': '2020-05-24T21:15:27Z'}, 'players': [{'rel': 'user', 'id': '8l06v078', 'uri': 'https://www.speedrun.com/api/v1/users/8l06v078'}], 'date': '2020-05-23', 'submitted': '2020-05-24T01:53:29Z', 'times': {'primary': 'PT43M3S', 'primary_t': 2583, 'realtime': 'PT43M3S', 'realtime_t': 2583, 'realtime_noloads': None, 'realtime_noloads_t': 0, 'ingame': 'PT40M20S', 'ingame_t': 2420}, 'system': {'platform': '83exk6l5', 'emulated': True, 'region': 'pr184lqn'}, 'splits': None,
                'values': {'5ly1mjl4': '4lxzde41'}, 
                'links': [{'rel': 'self', 'uri': 'https://www.speedrun.com/api/v1/runs/y659ro0z'}, {'rel': 'game', 'uri': 'https://www.speedrun.com/api/v1/games/y65lq71e'}, {'rel': 'category', 'uri': 'https://www.speedrun.com/api/v1/categories/7dgv34d4'}, {'rel': 'platform', 'uri': 'https://www.speedrun.com/api/v1/platforms/83exk6l5'}, {'rel': 'region', 'uri': 'https://www.speedrun.com/api/v1/regions/pr184lqn'}, {'rel': 'examiner', 'uri': 'https://www.speedrun.com/api/v1/users/18vnevjl'}]}}

    test2 = PB(test)
    print(test2)