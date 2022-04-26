from tables.base import Base_Table

class LB(Base_Table):
    """Class representing a leaderboard on SRC.

        Attributes:
            data (list): List of Rank objects. Classed by place.
                id 0 == WR
                id -1 == last place
            WR (int): WR of the leaderboard. TODO : Consider changing this to a method...
        """
    def __init__(self, list_Ranks:list):
        """
            Args:
                list_Ranks (list): List of Dictionnaries of the leaderboard received from SRC.
                    See lb_entry.py for format of dictionnaries.
            """
        self.data = []
        self.WR = list_Ranks[0]["run"]["times"]["primary_t"]

        #for data in list_Ranks:
        #    self.data.append(Rank(data, self.WR))

    def sum(self):
        tempo = super().sum()
        tempo["WR %"] = tempo.time / tempo["WR time"]
        return tempo