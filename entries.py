from generic import Entry

class Run(Entry):
    def __init__(self, data):
        super().__init__(data)
        self.__dict__["time"] = data["times"]["primary_t"]
        for unwanted in ["weblink", "videos", "comment","times", "links", "splits", "submitted", "players", "id", "status"]:
            del self.__dict__[unwanted]

class PB(Run):
    def __init__(self, data):
        corrected_data = data["run"]
        corrected_data["place"] = data["place"]
        super().__init__(corrected_data)

if __name__ == "__main__":
    entry_data = {'id': 'z073gloy' ,"place": 15, 'weblink': 'https://www.speedrun.com/bhero/run/z073gloy', 'game': 'nd2eeqd0', 'level': None, 'category': 'zd3yzr2n', 'videos': {'links': [{'uri': 'https://www.twitch.tv/videos/1110770410'}]}, 'comment': 'Blind race. Stellar hitboxes right here.', 'status': {'status': 'verified', 'examiner': '98rpeqj1', 'verify-date': '2021-08-08T19:00:00Z'}, 'players': [{'rel': 'user', 'id': 'x7qz6qq8', 'uri': 'https://www.speedrun.com/api/v1/users/x7qz6qq8'}], 'date': '2021-08-06', 'submitted': '2021-08-07T05:35:16Z', 'times': {'primary': 'PT4H2M40S', 'primary_t': 14560, 'realtime': 'PT4H2M40S', 'realtime_t': 14560, 'realtime_noloads': None, 'realtime_noloads_t': 0, 'ingame': None, 'ingame_t': 0}, 'system': {'platform': 'nzelreqp', 'emulated': False, 'region': 'pr184lqn'}, 'splits': None, 'values': {}, 'links': [{'rel': 'self', 'uri': 'https://www.speedrun.com/api/v1/runs/z073gloy'}, {'rel': 'game', 'uri': 'https://www.speedrun.com/api/v1/games/nd2eeqd0'}, {'rel': 'category', 'uri': 'https://www.speedrun.com/api/v1/categories/zd3yzr2n'}, {'rel': 'platform', 'uri': 'https://www.speedrun.com/api/v1/platforms/nzelreqp'}, {'rel': 'region', 'uri': 'https://www.speedrun.com/api/v1/regions/pr184lqn'}, {'rel': 'examiner', 'uri': 'https://www.speedrun.com/api/v1/users/98rpeqj1'}]}
    test_class = PB(entry_data)
    print(test_class)