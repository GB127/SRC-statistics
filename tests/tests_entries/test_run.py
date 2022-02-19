from entries.run_entry import Run
from tests.datas_fx import fill_db, dicto_m

class Test_init:
    @fill_db
    def test_init_create_attri(self):
        for attribute in ["game", "time", "system","category", "region", "emu"]:
            assert hasattr(Run(dicto_m("run")["data"]), attribute)
    @fill_db
    def test_init_del_attri(self):
        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(Run(dicto_m("run")["data"]), unwanted)

class Test_str:
    @fill_db
    def test_str(self):
        p = [4, 20, 10,9]
        string = f"{'Gamecube'[:p[0]]:{p[0]}}   {'Super Mario Sunshine'[:p[1]]:{p[1]}}   {'Any%'[:p[2]]:{p[2]}}   {'11:11:11'[:p[3]]:>{p[3]}}"
        assert str(Run(dicto_m("run")["data"])) == string
