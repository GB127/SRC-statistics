from code_SRC.api import api
from entries.base import Base_Entry


class Run(Base_Entry):
    def __init__(self, data:dict):
        self.game = api.game(data["game"])
        self.category = api.category(data["category"])
        self.emu = str(data["system"]["emulated"])
        self.region = api.region(data["system"]["region"])
        self.system = api.system(data["system"]["platform"])
        self.time = data["times"]["primary_t"]
        self.subcat = ""
        subcat_tempo = []
        for field, selection in data["values"].items():
            if field in api.subcat_db:
                subcat_tempo.append(api.subcat_db[field][selection])
        if subcat_tempo:
            self.category += f' ({" - ".join(subcat_tempo)})'


        self.level = None

        if data["level"]:
            self.level = data["level"]

    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        p = [4, 20, 20,30, 9]
        liste = []
        for no, attribute in enumerate(["system", "game","level", "category", "time"]):
            if isinstance(self[attribute], (float,int)):
                liste.append(f'{time_str(self[attribute])[:p[no]]:>{p[no]}}')
            elif attribute == "level" and not self[attribute]: 
                continue
            else:
                liste.append(f'{self[attribute][:p[no]]:{p[no]}}')
        return "   ".join(liste)

