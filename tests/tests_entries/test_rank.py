from entries.rank_entry import Rank
from tests.datas_fx import fill_db, dicto_m
from tests.mocks import Rank_mock

class Test_init:
    @fill_db
    def test_init(self):
        testing = Rank(dicto_m("rank")["data"], 50000)
        for attribute in ["place", "game", "time", "system","category","WR %", "region", "emu", "WR time"]:
            assert hasattr(testing, attribute), f"{attribute} not created"

        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(testing, unwanted)

        assert testing["WR time"] == 50000
        assert testing["WR %"] == 1.61084


class Test_misc:
    @fill_db
    def test_str(self):
        testing_1 = Rank_mock()
        assert str(testing_1) == "  0:00:02   -0:00:01   200.00%"
    
    def test_operations_perc(self):
        testing_1 = Rank_mock()
        somme = testing_1 + testing_1
        assert somme["WR %"] == 2
        quotient = testing_1 / 2
        assert quotient["WR %"] == 2