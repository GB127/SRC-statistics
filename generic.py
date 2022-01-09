from api import SRC_request, URL
from copy import deepcopy

spacing = {"game" : 30, "system" : 4, "category":20, "time":9, "%":7, "#":3}


class table:
    def __init__(self,classe, list_data, level=False):
        self.data = []
        for one in list_data:
            self.data.append(classe(one))

    def __str__(self):
        def médiane():
            médi = deepcopy(self.data[0])
            for attribute in self.data[0].__dict__:
                try: all_data = sorted([x.__dict__[attribute] for x in self.data])
                except TypeError: continue
                médi.__dict__[attribute] = all_data[len(all_data) // 2]
                if isinstance(médi.__dict__[attribute], str): médi.__dict__[attribute] = ""
            return médi


        header = []
        for attribu in self.data[0].str_order:
            if "time" in attribu:
                header.append(f'{attribu[:spacing["time"]]:^{spacing["time"]}}')
                continue
            elif "%" in attribu:
                header.append(f'{attribu[:spacing["%"]]:^{spacing["%"]}}')
                continue
            try:
                header.append(f'{attribu[:spacing[attribu]]:^{spacing[attribu]}}')
            except KeyError:
                header.append(f'{attribu[:10]:^10}')
        header = " | ".join(header)

        stringed = "\n".join([str(x) for x in self.data])

        line = "\n" + "-" * len(str(self.data[0])) + "\n"  # FIXME : Try with or
        if str(self.data[0]).find("\n") != -1:
            line = "\n" + "-" * str(self.data[0]).find("\n") + "\n"

        total = sum(self.data)
        moyenne = total / len(self.data)
        return (line).join([header, stringed,f'{total}', f'{moyenne}', f'{médiane()}'])

    # Basic stuffs for making the stuff an iterable and all.
    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)

    def sort(self):
        self.data.sort()  #FIXME : Consider trying with key

class filtered_table(table):
    def __init__(self, filter, *datas):
        self.data = []
        clés = set()
        def filtered(data):
            filtré = {}
            # TODO: See if I can add an empty list here instead of a loop outside of the filter.
            for run in data:
                filtré[run.__dict__[filter]] = filtré.get(run.__dict__[filter], []) + [run]
                clés.add(run.__dict__[filter])
            return filtré


        données_filtrées = list(map(filtered, datas))

        for clé in données_filtrées[0].keys():
            for run_type in données_filtrées[1:]:
                if not clé in run_type:
                    run_type[clé] = []

        for clé in clés:
            self.data.append(Filtered_Entry(filter, [données_filtrées[x][clé] for x in range(len(données_filtrées))]))


class Entry:
    str_order = ["game", "category", "times"]
    sorter = "time"
    systems, games, categories, subcategories = {}, {}, {}, {}

    def __init__(self, data, level=None):
        def game_system_category():
            def get_system(ID):
                """Return the system.
                    Returns: (str) full name of the system.
                    """
                rep = SRC_request(f"{URL}/platforms/{ID}")
                print(f"Got system : {rep['data']['name']}")
                return rep["data"]["name"]

            def get_game(ID):
                """Fetch the full name of the game with an ID or acronym(str).
                    """
                rep = SRC_request(f"{URL}/games/{ID}")
                print(f"    Got game name : {rep['data']['names']['international']}")
                return rep["data"]["names"]["international"]

            def get_category(ID):
                """Fetch the full name of the category with an ID.
                    Returns (str): Full name of the category
                    """
                rep = SRC_request(f'{URL}/categories/{ID}')
                print(f"        Got {self.game}'s category: {rep['data']['name']}")
                return rep["data"]["name"]

            for attribute, repertoire, funct_req in zip(
                    ["game",        "category",         "system"], 
                    [Entry.games,   Entry.categories,   Entry.systems], 
                    [get_game,      get_category,       get_system]
                    ):
                if not data[attribute]:
                    self.__dict__[attribute] = "???"
                    continue
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
                rep = SRC_request(f'{URL}/variables/{variID}')
                print(f"                Got {self.game}'s variable: {rep['data']['name']}")
                return rep["data"]

            sub = []
            self.sub_IDs = []
            for category, subcat in self.values.items():
                if not category in Entry.subcategories:
                    Entry.subcategories[category] = {}
                elif not Entry.subcategories[category]:
                    continue
                try:
                    if Entry.subcategories[category][subcat]:
                        sub.append(Entry.subcategories[category][subcat])
                        self.sub_IDs.append((category, subcat))
                except KeyError:
                    données = get_variable(category)
                    if données["is-subcategory"]:
                        for ID, subcat_name in données["values"]["values"].items():
                            Entry.subcategories[category][ID] = f"{subcat_name['label']}"
                        sub.append(Entry.subcategories[category][subcat])
                        self.sub_IDs.append((category, subcat))
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
                if isinstance(self.__dict__[attribu], set):
                    stringed.append(f"{f'{len(self.__dict__[attribu])} {attribu}'[:spacing[attribu]]:{spacing[attribu]}}")
                elif "%" in attribu:
                    stringed.append(f'{self.__dict__[attribu]:>7.2%}')
                elif "time" not in attribu:
                    stringed.append(f'{str(self.__dict__[attribu])[:spacing[attribu]]:{spacing[attribu]}}')
                else:
                    stringed.append(f'{time_str(self.__dict__[attribu]):{spacing["time"]}}')
            except KeyError:
                stringed.append(f'{str(self.__dict__[attribu])[:10]:10}')

        return " | ".join(stringed)

    def __lt__(self, other):
        assert type(self) == type(other), "Can only sort things of same type."
        return self.__dict__[self.sorter] <= other.__dict__[other.sorter]


    def __truediv__(self, other):
        copie = deepcopy(self)
        for attribute in self.__dict__:
            if isinstance(self.__dict__[attribute], (int, float)):
                copie.__dict__[attribute] /= other
            elif isinstance(self.__dict__[attribute], set):
                copie.__dict__[attribute] = len(copie.__dict__[attribute]) / other
        else:pass
        return copie


    def __add__(self, other):
        copie = deepcopy(self)
        if other == 0:
            return copie
        else:
            for attribute in self.__dict__:
                if isinstance(copie.__dict__[attribute], (int, float)):
                    copie.__dict__[attribute] += other.__dict__[attribute]
                elif isinstance(copie.__dict__[attribute], str) and copie.__dict__[attribute] != other.__dict__[attribute]:
                    copie.__dict__[attribute] = {copie.__dict__[attribute]}
                if isinstance(copie.__dict__[attribute], set):
                    if isinstance(other.__dict__[attribute], set):
                        copie.__dict__[attribute] |= other.__dict__[attribute]
                    else:
                        copie.__dict__[attribute] |= {other.__dict__[attribute]}
            return copie

    def __radd__(self,other):
        return self.__add__(other)

class Filtered_Entry(Entry):
    str_order = ["filter", "Run", "Run #", "PB", "PB #"]
    sorter = "filter"
    def __init__(self, filter, data):
        self.label = filter
        self.filter = deepcopy(data[0][0].__dict__[filter])
        for id, sorte in enumerate(data):
            try:
                self.__dict__[type(sorte[0]).__name__] = sum(deepcopy(sorte))
                self.__dict__[f'{type(sorte[0]).__name__} #'] = len(deepcopy(sorte))
            except IndexError:
                self.__dict__[["Run", "PB"][id]] = "" 


    def __str__(self):
        total =  " | ".join([f'{self.__dict__["Run #"]:3}', 
                                str(self.Run)[63:], 
                                f'{self.__dict__["PB #"]:3}', 
                                str(self.PB)[63:]])
        moyenne =  " | ".join([ "  ",
                                str(self.Run / self.__dict__["Run #"])[63:],
                                "   ",
                                str(self.PB / self.__dict__["PB #"])[63:]])

        filtre = self.filter
        if isinstance(self.filter, set):
            filtre = f'{len(self.filter)} {self.label}'

        return f'{filtre[:30]:30}| {total}\n{" " * 30}|  {moyenne}'

    def __add__(self, other):
        if other == 0:
            return deepcopy(self)
        copie = deepcopy(self)
        for clé in self.__dict__:
            if clé in ["label", "str_order"]: continue
            try:copie.__dict__[clé] += other.__dict__[clé]
            except TypeError: copie.__dict__[clé] |= {other.__dict__[clé]}
        copie.filter = copie.__dict__["Run"].__dict__[self.label]
        return copie

    def __truediv__(self, other):
        copie = deepcopy(self)
        for clé in self.__dict__:
            if clé in ["label", "str_order"]: continue
            try: copie.__dict__[clé] /= other
            except TypeError: copie.__dict__[clé] = f'{len(copie.__dict__[clé]) / other} {clé}'

        return copie

if __name__ == "__main__":
    entry_data = {  'place': 14 ,
                    'game': 'nd2eeqd0',
                    'level': None, 
                    'category': 'zd3yzr2n',
                    'date': '2021-08-06',
                    'times': 14560, 
                    'system': {'platform': 'nzelreqp', 'emulated': False, 'region': 'pr184lqn'}, 
                    'values': {}}
    test_class = Entry(entry_data)
