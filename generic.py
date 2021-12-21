from api import requester

spacing = {"game" : 20, "system" : 4, "category":15}


class table:
    def __init__(self,classe, list_data, level=False):
        self.data = []
        for one in list_data:
            self.data.append(classe(one))

    def __str__(self):
        header = []
        for attribu, value in self.data[0].__dict__.items():
            try:
                header.append(f'{attribu[:spacing[attribu]]:^{spacing[attribu]}}')
            except KeyError:
                header.append(f'{attribu[:10]:^10}')
        header = " | ".join(header)


        stringed = "\n".join([str(x) for x in self.data])
        return "\n".join([header, stringed])


    # Basic stuffs for making the stuff an iterable and all.
    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)

class Entry:
    games = {}
    categories = {}
    subcategories = {}
    systems = {}
    def __init__(self, data, level=None):
        def get_variable(variID):
            """ Returns json data about the speedrun variable identified by ID.
                => Notable infos: 
                    "is-subcategory"
                    "values", "values", "label"
                """
            rep = requester(f'/variables/{variID}')
            return rep["data"]

        def get_system(ID):
            """Return the system.
                Returns: (str) full name of the system.
                """
            rep = requester(f"/platforms/{ID}")
            print(f"Got system : {rep['data']['name']}")
            return rep["data"]["name"]

        def get_game(ID):
            """Fetch the full name of the game with an ID or acronym(str).
                """
            rep = requester(f"/games/{ID}")
            print(f"Got game name : {rep['data']['names']['international']}")
            return rep["data"]["names"]["international"]

        def get_category(ID):
            """Fetch the full name of the category with an ID.
                Returns (str): Full name of the category
                """
            rep = requester(f'/categories/{ID}')
            print(f"Got {self.game}'s category: {rep['data']['name']}")
            return rep["data"]["name"]

        self.__dict__ = data
        self.__dict__["system"] = data["system"]["platform"]

        if not level:
            del self.level

        for attribute, repertoire, funct_req in zip(
                ["game",        "category",         "system"], 
                [Entry.games,   Entry.categories,   Entry.systems], 
                [get_game,      get_category,       get_system]
                ):
            try:
                self.__dict__[attribute] = repertoire[data[attribute]]
            except KeyError:
                repertoire[data[attribute]] = funct_req(data[attribute])
                self.__dict__[attribute] = repertoire[data[attribute]]

    def __str__(self):
        stringed = []
        for attribu, value in self.__dict__.items():
            try:
                stringed.append(f'{str(value)[:spacing[attribu]]:{spacing[attribu]}}')
            except KeyError:
                stringed.append(f'{str(value)[:10]:10}')
        return " | ".join(stringed)

if __name__ == "__main__":
    entry_data = {'id': 'z073gloy','place': 14 , 'weblink': 'https://www.speedrun.com/bhero/run/z073gloy', 'game': 'nd2eeqd0', 'level': None, 'category': 'zd3yzr2n', 'videos': {'links': [{'uri': 'https://www.twitch.tv/videos/1110770410'}]}, 'comment': 'Blind race. Stellar hitboxes right here.', 'status': {'status': 'verified', 'examiner': '98rpeqj1', 'verify-date': '2021-08-08T19:00:00Z'}, 'players': [{'rel': 'user', 'id': 'x7qz6qq8', 'uri': 'https://www.speedrun.com/api/v1/users/x7qz6qq8'}], 'date': '2021-08-06', 'submitted': '2021-08-07T05:35:16Z', 'times': {'primary': 'PT4H2M40S', 'primary_t': 14560, 'realtime': 'PT4H2M40S', 'realtime_t': 14560, 'realtime_noloads': None, 'realtime_noloads_t': 0, 'ingame': None, 'ingame_t': 0}, 'system': {'platform': 'nzelreqp', 'emulated': False, 'region': 'pr184lqn'}, 'splits': None, 'values': {}, 'links': [{'rel': 'self', 'uri': 'https://www.speedrun.com/api/v1/runs/z073gloy'}, {'rel': 'game', 'uri': 'https://www.speedrun.com/api/v1/games/nd2eeqd0'}, {'rel': 'category', 'uri': 'https://www.speedrun.com/api/v1/categories/zd3yzr2n'}, {'rel': 'platform', 'uri': 'https://www.speedrun.com/api/v1/platforms/nzelreqp'}, {'rel': 'region', 'uri': 'https://www.speedrun.com/api/v1/regions/pr184lqn'}, {'rel': 'examiner', 'uri': 'https://www.speedrun.com/api/v1/users/98rpeqj1'}]}
    test_class = Entry(entry_data)
    print(test_class)