from tables.leaderboard import LB
from tests.datas_fx import dicto_m, fill_db

class Test_init:
    @fill_db
    def test_WR(self):
        tempo = LB(dicto_m("lb")["data"]["runs"])
        assert tempo.WR == 40271

    def test_add(self):
        assert NotImplementedError
    
    def test_add_int(self):
        assert NotImplementedError