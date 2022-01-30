from code_SRC.run_entry import Run
from tests.test_datas import run_base, run_subcat
from copy import copy

def test_Run_attributes():
    for attribute in ["game", "system", "category", "date", "time", "emu", "region"]:
        assert hasattr(Run(copy(run_base)), attribute), f'{attribute} not created'

def test_Run_del_unwanted_attri():
    for attribute in ["id", "weblink", "videos","ruleset", "comment", "status", "submitted", "times", "splits", "links"]:
        assert not hasattr(Run(copy(run_base)), attribute), f'{attribute} is still created'

def test_Run_init_game():
    assert Run(copy(run_base))["game"] == "Bomberman Hero"

def test_Run_init_system():
    assert Run(copy(run_base))["system"] == "Wii VC"

def test_Run_init_categ():
    assert Run(copy(run_base))["category"] == "US Any%"

def test_Run_init_date():
    assert Run(copy(run_base))["date"] == "2021-08-06"

def test_Run_init_time():
    assert Run(copy(run_base))["time"] == 14560

def test_Run_init_emu():
    assert Run(copy(run_base))["emu"] == False

def test_Run_init_region():
    assert Run(copy(run_base))["region"] == "US"

def test_Run_str():
    assert str(Run(copy(run_base))) == " | ".join(["WiiVC", "Bomberman Hero", "Any %", "3:07:40"])


def test_Run_add_time():
    somme = Run(copy(run_base)) + Run(copy(run_base))
    assert Run(run_base)["time"] * 2 == somme["time"]
    assert Run(run_base) + 0 == Run(run_base)

def test_Run_add_game():
    somme = Run(copy(run_base)) + Run(copy(run_base))
    assert Run(run_base)["game"] == somme["game"]

def test_Run_div_time():
    divide = Run(copy(run_base)) / 2
    assert Run(copy(run_base))["time"] / 2 == divide["time"]

def test_Run_lt():
    assert Run(copy(run_base)) > Run(copy(run_subcat))

def test_Run_eq():
    assert Run(copy(run_base)) == Run(copy(run_base))

