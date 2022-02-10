from entries.rank_entry import Rank
from tests.datas_fx import fill_db, dicto_m

class Test_init:
    @fill_db
    def test_init_create_attri(self):
        for attribute in ["place", "game", "time", "system","category","WR_perc", "region", "emu", "WR"]:
            assert hasattr(Rank(dicto_m("rank")["data"], 50000), attribute), f"{attribute} not created"
    @fill_db
    def test_init_del_attri(self):
        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(Rank(dicto_m("rank")["data"], 50000), unwanted)

    def test_init_WR(self):
        assert Rank(dicto_m("rank")["data"], 50000).WR == 50000

    def test_init_WR_perc(self):
        assert Rank(dicto_m("rank")["data"], 80542 / 2).WR_perc == 2

    @fill_db
    def test_eq(self):
        assert Rank(dicto_m("rank")["data"],50000)  == Rank(dicto_m("Rank")["data"], 50000)


class Test_misc:
    @fill_db
    def test_str(self):

        string = "50    22:22:22   -11:11:11   200.00%"
        assert str(Rank(dicto_m("rank")["data"],80542 / 2)) == string