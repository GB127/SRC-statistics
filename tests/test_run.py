from entries.run_entry import Run
from tests.datas_fx import fill_db, dicto_m

class Test_Run:
    @fill_db
    def test_init_create_attri(self):
        for attribute in ["game", "time", "system","category", "region", "emu"]:
            assert hasattr(Run(dicto_m("run")["data"]), attribute)
    @fill_db
    def test_init_del_attri(self):
        for unwanted in ["id", "weblink", "videos", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            assert not hasattr(Run(dicto_m("run")["data"]), unwanted)

    @fill_db
    def test_str(self):
        string = "Gamecube   Super Mario Sunshine   Any%    14:08:27"
        assert str(Run(dicto_m("run")["data"])) == string

    @fill_db
    def test_eq(self):
        assert Run(dicto_m("run")["data"]) == Run(dicto_m("run")["data"])
