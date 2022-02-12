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

    @fill_db
    def test_str_sets(self):
        setted = Run(dicto_m("run")["data"])
        for x in ["game", "category", "system"]:
            setted[x] = {setted[x], "setted[x]"}
        p = [4, 20, 10,9]
        string = f"{'2'[:p[0]]:{p[0]}}   {'2'[:p[1]]:{p[1]}}   {'2'[:p[2]]:{p[2]}}   {'11:11:11'[:p[3]]:>{p[3]}}"
        assert str(setted) == string


class Test_add:
    def test_time(self):
        somme = Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"])
        assert somme.time == Run(dicto_m("run")["data"]).time * 2

    def test_0(self):
        assert Run(dicto_m("run")["data"]) + 0 == Run(dicto_m("run")["data"])


    def test_same_game(self):
        somme = Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"])
        assert somme.game == Run(dicto_m("run")["data"]).game

    def test_diff_game(self):
        tempo = Run(dicto_m("run")["data"])
        tempo.game = "Random Game"
        somme = Run(dicto_m("run")["data"]) + tempo
        assert somme.game == {Run(dicto_m("run")["data"]).game, tempo.game}

    def test_same_system(self):
        somme = Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"])
        assert somme.system == Run(dicto_m("run")["data"]).system

    def test_diff_system(self):
        tempo = Run(dicto_m("run")["data"])
        tempo.system = "Random system"
        somme = Run(dicto_m("run")["data"]) + tempo
        assert somme.system == {Run(dicto_m("run")["data"]).system, tempo.system}


class Test_div:
    def test_int(self):
        result = Run(dicto_m("run")["data"]) / 2 
        assert result.time == Run(dicto_m("run")["data"]).time / 2


class Test_misc_operators:
    @fill_db
    def test_eq(self):
        assert Run(dicto_m("run")["data"]) == Run(dicto_m("run")["data"])

    def test_set(self):
        tempo = Run(dicto_m("run")["data"])
        tempo["game"] = "Allo"
        assert tempo["game"] == "Allo"

    def test_get(self):
        assert Run(dicto_m("run")["data"])["game"] == "Super Mario Sunshine"