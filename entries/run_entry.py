from code_SRC.api import api
from entries.base import Base_Entry


class Run(Base_Entry):
    def __init__(self, data:dict):
        # self.__dict__ = data
        self.game = api.game(data["game"])
        self.category = api.category(data["category"])
        self.emu = data["system"]["emulated"]
        self.region = data["system"]["region"]
        self.system = api.system(data["system"]["platform"])
        self.time = data["times"]["primary_t"]

    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        p = [4, 20, 10, 9]

        liste = []
        for no, attribute in enumerate(["system", "game","category", "time"]):
            if isinstance(self[attribute], (float,int)):
                if "time" in attribute:
                    liste.append(f'{time_str(self[attribute])[:p[no]]:>{p[no]}}')
                else:
                    liste.append(f'{str(self[attribute])[:p[no]]:{p[no]}}')
            elif isinstance(self[attribute], set):
                liste.append(f'{str(len(self[attribute]))[:p[no]]:{p[no]}}')
            else:
                liste.append(f'{self[attribute][:p[no]]:{p[no]}}')
        return "   ".join(liste)
