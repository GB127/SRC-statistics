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
    assert 0 + Base_Entry() == Base_Entry()

def test_add_int():
    testing = Base_Entry()
    testing.__dict__ = {"int":1}
    testing2 = Base_Entry()
    testing2 = {"int":3}
    somme = testing + testing2
    assert somme.int == 4

def test_add_str_dif():
    testing, testing2 = Base_Entry(), Base_Entry()
    testing.__dict__ = {"str":"1"}
    testing2.__dict__ = {"str":"3"}
    somme = testing + testing2
    assert somme.str == {"1", "3"}

def test_add_str_same():
    testing, testing2 = Base_Entry(), Base_Entry()
    testing.__dict__ = {"str":"1"}
    testing2.__dict__ = {"str":"1"}
    somme = testing + testing2
    assert somme.str == "1"



def test_div_int():
    testing = Base_Entry()
    testing.__dict__ = {"int":2}
    quotient = testing / 2
    assert quotient.int == 1

def test_div_str_1():
    testing = Base_Entry()
    testing.__dict__ = {"str":"2222"}
    quotient = testing / 2
    assert quotient.str == "0.5 str"

def test_div_str_mul():
    testing = Base_Entry()
    testing.__dict__ = {"str":{"2", "1"}}
    quotient = testing / 2
    assert quotient.str == "1.0 str"



def test_eq():
    assert Base_Entry() == Base_Entry()
