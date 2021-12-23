from api import requester

spacing = {"game" : 25, "system" : 4, "category":25, "time":12}


class table:
    def __init__(self,classe, list_data, level=False):
        self.data = []
        for one in list_data:
            self.data.append(classe(one))

    def __str__(self):
        header = []
        for attribu in self.data[0].str_order:
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
    str_order = ["game", "category"]
    games = {}
    categories = {}
    subcategories = {}
    systems = {}
    def __init__(self, data, level=None):
        def game_system_category():
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

        def subcateg():
            def get_variable(variID):
                """ Returns json data about the speedrun variable identified by ID.
                    => Notable infos: 
                        "is-subcategory"
                        "values", "values", "label"
                    """
                rep = requester(f'/variables/{variID}')
                return rep["data"]

            sub = []
            for category, subcat in self.values.items():
                try:
                    if Entry.subcategories[category]:
                        sub.append(Entry.subcategories[category][subcat])
                except KeyError:
                    Entry.subcategories[category] = {}
                    données = get_variable(category)
                    if données["is-subcategory"]:
                        Entry.subcategories[category][subcat] = f"{données['values']['values'][subcat]['label']}"
                        sub.append(Entry.subcategories[category][subcat])
                    else:
                        Entry.subcategories[category] = False
            if sub:
                self.category += f' ({", ".join(sub)})'
            del self.values

        self.__dict__ = data
        self.__dict__["system"] = data["system"]["platform"]

        if not level:
            del self.level
        del self.date

        game_system_category()
        subcateg()

    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        stringed = []

        for attribu in self.str_order:
            try:
                if "time" not in attribu:
                    stringed.append(f'{str(self.__dict__[attribu])[:spacing[attribu]]:{spacing[attribu]}}')
                else:
                    stringed.append(f'{time_str(self.__dict__[attribu]):{spacing["time"]}}')
            except KeyError:
                stringed.append(f'{str(self.__dict__[attribu])[:10]:10}')

        return " | ".join(stringed)



    def __str2(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'

        stringed = []
        for attribu, value in self.__dict__.items():
            try:
                if "time" not in attribu:
                    stringed.append(f'{str(value)[:spacing[attribu]]:{spacing[attribu]}}')
                else:
                    stringed.append(f'{time_str(value):{spacing["time"]}}')
            except KeyError:
                stringed.append(f'{str(value)[:10]:10}')
        return " | ".join(stringed)

if __name__ == "__main__":
    entry_data = {'place': 14 , 'game': 'nd2eeqd0', 'level': None, 'category': 'zd3yzr2n', 'date': '2021-08-06', 'times': 14560, 'system': {'platform': 'nzelreqp', 'emulated': False, 'region': 'pr184lqn'}, 'values': {}}
    test_class = Entry(entry_data)
    print(test_class)