from entries.base import Base_Entry

def test_setitem():
    testing = Base_Entry()
    testing["allo"] = 1
    assert testing.__dict__["allo"] == 1


def test_getitem():
    testing = Base_Entry()
    testing.__dict__ = {"allo2":1}
    testing.allo = 0
    assert testing["allo"] == 0 and testing["allo2"] == 1


def test_add_0():
    assert Base_Entry() + 0 == Base_Entry()

def test_add_int():
    raise NotImplementedError

def test_add_str():
    raise NotImplementedError

def test_div_int():
    raise NotImplementedError

def test_div_str():
    raise NotImplementedError

def test_eq():
    assert Base_Entry() == Base_Entry()
