from entries.run_entry import Run
from tests.datas_fx import fill_db, dicto_m
from tests.mocks import Run_mock

class Test_init:
    @fill_db
    def test_init_create_attri(self):
        for attribute in ["game", "time", "system","category", "region", "emu", "level"]:
            assert hasattr(Run(dicto_m("run")["data"]), attribute), f"{attribute} not created"
        dicto = dicto_m("run")["data"]
        dicto["level"] = "ha71kldd"
        for attribute in ["game", "time", "system","category", "region", "emu", "level"]:
            assert hasattr(Run(dicto), attribute), f"{attribute} not created"
        assert bool(Run(dicto).level)
    def test_init_del_attri(self):
        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(Run(dicto_m("run")["data"]), unwanted)



class Test_str:
    def test_str(self):
        testing_1 = Run_mock()
        assert "syst   game                   Category       0:00:01" == str(testing_1)
        testing_1.category = {"Category1", "Category2"}
        assert str(testing_1) == "syst   game                   2 category     0:00:01"
        testing_2 = Run_mock(include_level=True)
        assert str(testing_2) == "syst   game                   level                  Category       0:00:01"
