from entries.pb_entry import PB
from tests.datas_fx import fill_db, dicto_m
from tests.tests_entries.mocks import PB_mock

class Test_init:
    @fill_db
    def test_init_create_attri(self):
        Test_init.model = PB(dicto_m("pb")["data"])
        for attribute in ["leaderboard"]:
            assert hasattr(Test_init.model, attribute), f"{attribute} not created"

    def test_init_del_attri(self):
        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(Test_init.model, unwanted)



class Test_others:
    def test_str(self):
        testing_1 = PB_mock()
        assert str(testing_1) == 'string'