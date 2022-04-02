from code_SRC.api import api
from entries.base_entry import Base_Entry


class Run(Base_Entry):
    """Class related to one Run on SRC.
        Attributes:
            game (str): Game of the speedrun
                example: Super Mario 64

            level (str or None) : Level of the speedrun, if the run is on a level. If the run is not on a level, the value is None
                example : Dragon Roost Cavern (a dungeon in Zelda: Wind Waker)

            category (str): Category of the speedrun. String in parenthesis is the subcategory if there is one.
                example : 120 stars (WII VC)

            emu (bool): True if run is ran on an emulator. False otherwise

            region (str): Region of the game being ran.
                example : USA / NTSC

            system (str): System of the run.
                example : Gamecube

            time (float) : Time of the speedrun, in seconds.

        """

    def __init__(self, data: dict):
        """Args:
            data (dict): Dicto received from SRC.
                Used keys from dicto:
                    id
                    game
                    level
                    category
                    times => primary_t
                    system: => platform + emulated + region
                    values: => {field : selection}
            """
        self.game = api.game(data["game"])
        self.category = api.category(data["category"])
        self.emu = str(data["system"]["emulated"])
        self.region = api.region(data["system"]["region"])
        self.system = api.system(data["system"]["platform"])
        self.time = data["times"]["primary_t"]

        subcat_tempo = []
        for field, selection in data["values"].items():
            if field in api.subcat_db:
                subcat_tempo.append(api.subcat_db[field][selection])
        if subcat_tempo:
            self.category += f' ({" - ".join(subcat_tempo)})'

        self.level = None
        if data["level"]:
            self.level = api.level(data["level"])

    def __str__(self):
        time_str = lambda x: f"{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}"
        p = [4, 20, 20, 30, 9]
        liste = []
        for no, attribute in enumerate(["system", "game", "level", "category", "time"]):
            if isinstance(self[attribute], (float, int)):
                liste.append(f"{time_str(self[attribute])[:p[no]]:>{p[no]}}")
            elif attribute == "level" and not self[attribute]:
                continue
            else:
                liste.append(f"{self[attribute][:p[no]]:{p[no]}}")
        return "   ".join(liste)
