from code_SRC.run_entry import Run
from tests.test_datas import run_base, run_subcat
from copy import copy


class Test_Run:
    test_base = Run(copy(run_base))
    test_subcat = Run(copy(run_subcat))

    def test_Run_attributes(self):
        for attribute in ["game", "system", "category", "date", "time", "emu", "region"]:
            assert hasattr(Test_Run.test_base, attribute), f'{attribute} not created'

    def test_Run_del_unwanted_attri(self):
        for attribute in ["id", "weblink", "videos","ruleset", "comment", "status", "submitted", "times", "splits", "links"]:
            assert not hasattr(Test_Run.test_base, attribute), f'{attribute} is still created'

    def test_Run_init_game(self):
        assert Test_Run.test_base["game"] == "Bomberman Hero"

    def test_Run_init_system(self):
        assert Test_Run.test_base["system"] == "Wii VC"

    def test_Run_init_categ(self):
        assert Test_Run.test_base["category"] == "US Any%"

    def test_Run_init_date(self):
        assert Test_Run.test_base["date"] == "2021-08-06"

    def test_Run_init_time(self):
        assert Test_Run.test_base["time"] == 14560

    def test_Run_init_emu(self):
        assert Test_Run.test_base["emu"] == False

    def test_Run_init_region(self):
        assert Test_Run.test_base["region"] == "US"

    def test_Run_str(self):
        wanted_str = " | ".join(["WiiVC", "Bomberman Hero", "Any %", "3:07:40"])
        assert str(Test_Run.test_base) == wanted_str


    def test_Run_add_time_from0(self):
        assert (Test_Run.test_base + 0) == Test_Run.test_base



    def test_Run_add_time(self):
        somme = Test_Run.test_base + Test_Run.test_base
        assert (Run(run_base)["time"] * 2) == somme["time"]

    def test_Run_add_game_same(self):
        somme = Test_Run.test_base + Test_Run.test_base
        assert Test_Run.test_base["game"] == somme["game"]

    def test_Run_add_game_diff(self):
        somme = Test_Run.test_base + Test_Run.test_subcat
        assert somme["game"] == {Test_Run["game"], Test_Run.test_subcat["game"]}

    def test_Run_add_game_group_present(self):
        somme = Test_Run.test_base + Test_Run.test_subcat
        somme += Test_Run.test_base
        assert somme["game"] == {Test_Run["game"], Test_Run.test_subcat["game"]}

    def test_Run_add_game_group_absent(self):
        raise NotImplementedError


    def test_Run_div_time(self):
        divide = Test_Run.test_base / 2
        assert Run(copy(run_base))["time"] / 2 == divide["time"]
