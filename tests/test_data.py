from tests.datas_fx import dicto_m, link_m, id_m

def test_load_dict():
    for x in ["category", "run", "game", "system", "level", "region"]:
        assert isinstance(dicto_m(x), dict)

def test_get_link():
    for x in ["category", "run", "game", "system", "level", "region"]:
        assert "https://www.speedrun.com/api/v1/" in link_m(x)

def test_load_id():
    for x in ["category", "run", "game", "system", "level", "region"]:
        assert isinstance(id_m(x), str)
        assert len(id_m(x)) < 10
