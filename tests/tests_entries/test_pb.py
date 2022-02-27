from entries.pb_entry import PB
from tests.datas_fx import fill_db, dicto_m

class Test_init:
    @fill_db
    def test_init_create_attri(self):
        Test_init.model = PB(dicto_m("pb")["data"])
        Test_init.model.leaderboard.data = Test_init.model.leaderboard.data[:20]
        Test_init.model.WR_perc = 1.1034

        for attribute in ["leaderboard"]:
            assert hasattr(Test_init.model, attribute), f"{attribute} not created"
    @fill_db
    def test_init_del_attri(self):
        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(Test_init.model, unwanted)

    def test_str(self):
        assert str(Test_init.model) == "Game   Super Mario Sunshine   Any%            0:48:54    11:11:11 (110.34%)    10/20    (50.00%)", str(Test_init.model.__dict__)