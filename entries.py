from generic import Entry, table
from api import requester

class Leaderboard(table):
    def __init__(self, IDs, level=False):
        def get_leaderboard(IDs):
            """Fetch the leaderboard data from SRC.

            Args:
                IDs (list) : List of IDs (str).
                    format : [Gameid, level_id/category_ID]
            """
            base_URL = f"/leaderboards/{IDs[0]}/"
            full_level = f"category/{IDs[1]}"
            rep = requester(f"{base_URL}{full_level}")
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
        tempo.LB = int(tempo.LB)
        tempo.place = int(tempo.place)

        return tempo

class PB(Ranking):
    str_order = ["system", "game", "category", "time", "WR time","delta time", "%", "place", "LB", "% LB"]
    def __init__(self, data):
        tempo = [data["run"]["game"], data["run"]["category"]]
        super().__init__(data)
        self.leaderboard = Leaderboard(tempo)
        self.__dict__["WR time"] = self.leaderboard[0].time
        self.__dict__["delta time"] = self.time - self.__dict__["WR time"]
        self.__dict__["%"] = self.time / self.__dict__["WR time"]
        self.__dict__["LB"] = len(self.leaderboard)
        self.__dict__["% LB"] = (len(self.leaderboard) - self.place) / len(self.leaderboard)

    def __truediv__(self, other):
        tempo = super().__truediv__(other)
        tempo.__dict__["% LB"] = (tempo.LB - tempo.place) / tempo.LB
        return tempo

    def __add__(self, other):
        tempo = super().__add__(other)
        tempo.__dict__["% LB"] = (tempo.LB - tempo.place) / tempo.LB
        return tempo




if __name__ == "__main__":
    entry_data = {  "place" : 14, 
                    "run": {
                        'id': 'z073gloy' ,
                        'weblink': 'https://www.speedrun.com/bhero/run/z073gloy',
                        'game': 'nd2eeqd0', 
                        'level': None, 
                        'category': 'zd3yzr2n', 
                        'videos': {'links': [{'uri': 'https://www.twitch.tv/videos/1110770410'}]}, 
                        'comment': 'Blind race. Stellar hitboxes right here.', 
                        'status': {'status': 'verified', 'examiner': '98rpeqj1', 'verify-date': '2021-08-08T19:00:00Z'}, 
                        'players': [{'rel': 'user', 'id': 'x7qz6qq8', 'uri': 'https://www.speedrun.com/api/v1/users/x7qz6qq8'}], 
                        'date': '2021-08-06', 'submitted': '2021-08-07T05:35:16Z',
                        'times': {'primary': 'PT4H2M40S', 'primary_t': 28418, 'realtime': 'PT4H2M40S', 'realtime_t': 14560, 'realtime_noloads': None, 'realtime_noloads_t': 0, 'ingame': None, 'ingame_t': 0}, 'system': {'platform': 'nzelreqp', 'emulated': False, 'region': 'pr184lqn'}, 'splits': None, 'values': {}, 'links': [{'rel': 'self', 'uri': 'https://www.speedrun.com/api/v1/runs/z073gloy'}, {'rel': 'game', 'uri': 'https://www.speedrun.com/api/v1/games/nd2eeqd0'}, {'rel': 'category', 'uri': 'https://www.speedrun.com/api/v1/categories/zd3yzr2n'}, {'rel': 'platform', 'uri': 'https://www.speedrun.com/api/v1/platforms/nzelreqp'}, {'rel': 'region', 'uri': 'https://www.speedrun.com/api/v1/regions/pr184lqn'}, {'rel': 'examiner', 
                        'uri': 'https://www.speedrun.com/api/v1/users/98rpeqj1'}]}}
    test_class = PB(entry_data)
    print(test_class.leaderboard)
    print(test_class)