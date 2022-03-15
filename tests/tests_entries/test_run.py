from entries.run_entry import Run
from tests.datas_fx import fill_db, dicto_m
from tests.tests_entries.mocks import Run_mock

class Test_init:
    @fill_db
    def test_init_create_attri(self):
        for attribute in ["game", "time", "system","category", "region", "emu"]:
            assert hasattr(Run(dicto_m("run")["data"]), attribute)

    def test_init_del_attri(self):
        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(Run(dicto_m("run")["data"]), unwanted)



class Test_str:
    def test_str(self):
        testing_1 = Run_mock()
        assert "string" == str(testing_1)