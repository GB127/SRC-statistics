from tables.leaderboard import LB
from tests.datas_fx import dicto_m, fill_db

class Test_init:
    @fill_db
    def test_WR(self):
        tempo = LB(dicto_m("lb")["data"]["runs"])
        assert tempo.WR == 40271

    def test_add(self):
        tempo = LB(dicto_m("lb")["data"]["runs"])
        assert 6 == tempo + tempo

    def test_add_int(self):
        tempo = LB(dicto_m("lb")["data"]["runs"])
        assert 3 == tempo + 0
        assert 3 == 0 + tempo