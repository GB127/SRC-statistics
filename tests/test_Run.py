from code_SRC.run_entry import Run
from tests.test_datas import run_base, run_subcat, run_base2, run_level
from copy import copy

class Test_Run:
    test_base = Run(copy(run_base))
    test_subcat = Run(copy(run_subcat))
    test_base2 = Run(copy(run_base2))
    test_level = Run(copy(run_level))

    def test_Run_attributes_nolevel(self):
        for attribute in ["game", "system", "category", "date", "time", "emu", "region"]:
            assert hasattr(Test_Run.test_base, attribute), f'{attribute} not created'

    def test_Run_eq(self):
        assert Test_Run.test_base == Run(copy(run_base))

    def test_Run_attributes_level(self):
        for attribute in ["game", "system", "level", "date", "time", "emu", "region"]:
            assert hasattr(Test_Run.test_level, attribute), f'{attribute} not created'


    def test_Run_del_unwanted_attributes(self):
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
        wanted_str = "Wii VC   Bomberman Hero   US Any%   3:07:40"
        assert str(Test_Run.test_base) == wanted_str


    def test_Run_add_time_from_0(self):
        assert (Test_Run.test_base + 0) == Test_Run.test_base

    def test_Run_add_time(self):
        somme = Test_Run.test_base + Test_Run.test_base
        assert (Run(copy(run_base))["time"] * 2) == somme["time"]

    def test_Run_add_game_same(self):
        somme = Test_Run.test_base + Test_Run.test_base
        assert Test_Run.test_base["game"] == somme["game"]

    def test_Run_add_game_diff(self):
        somme = Test_Run.test_base + Test_Run.test_subcat
        assert somme["game"] == {Test_Run.test_base["game"], Test_Run.test_subcat["game"]}

    def test_Run_add_game_group_present(self):
        somme = Test_Run.test_base + Test_Run.test_subcat
        somme += Test_Run.test_base
        assert somme["game"] == {Test_Run.test_base["game"], Test_Run.test_subcat["game"]}

    def test_Run_add_game_group_absent(self):
        somme = Test_Run.test_base + Test_Run.test_subcat
        somme += Test_Run.test_base2
        assert somme["game"] == {Test_Run.test_base["game"], Test_Run.test_subcat["game"], Test_Run.test_base2["game"]}


    def test_Run_div_time(self):
        divide = Test_Run.test_base / 2
        assert 14560 / 2 == divide["time"]


    def test_Run_div_sets(self):
        divide = (Test_Run.test_base2 + Test_Run.test_base) / 2
        assert divide["game"] == "1.0 game"
