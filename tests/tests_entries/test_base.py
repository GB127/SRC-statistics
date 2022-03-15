from entries.base import Base_Entry

def test_set_get_item():
    testing = Base_Entry()
    testing["allo"] = 1
    assert testing.allo == 1  # Check the set
    assert testing["allo"] == 1  # Check the get

def test_add():
    test_1 = Base_Entry()
    test_1.__dict__ = {
        "int":1, 
        "none":None,
        "bool" : True,
        "difstr": "A",
        "samestr": "X",
        "set_str": {"set", "set1", "set2"},
        "set_set": {"set", "set1", "set2"}}
    test_2 = Base_Entry()
    test_2.__dict__ = {
        "int":2,
        "bool":False,
        "none":None, 
        "difstr": "B",
        "samestr": "X",
        "set_str": "set3",
        "set_set": {"set3", "set4"}}

    # With 0:
    assert test_1 + 0 == test_1
    assert 0 + test_1 == test_1

    somme = test_1 + test_2
    assert somme.none == None  # Check if None stays None
    assert somme.int == 3  # Check the addition of int
    assert somme.difstr == {"A", "B"}  # Check the addition of 2 diff str
    assert somme.samestr == "X"  # Check the addition of the same str
    assert somme.set_str == {"set", "set1", "set2", "set3"}
    assert somme.set_set == {"set", "set1", "set2", "set3","set4"}
    assert isinstance(somme.bool, bool)

def test_div():
    test_1 = Base_Entry()
    test_1.__dict__ = {
        "int":2,
        "none":None,
        "bool" : True,
        "str": "string",
        "set": {"set1", "set2"}}

    quotient = test_1 / 2
    assert quotient.int == 1
    assert quotient.none == None  # Check if None stays None
    assert quotient.str == "0.5 str"
    assert quotient.set == "1.0 set"
    assert isinstance(quotient.bool, bool)


def test_eq():
    assert Base_Entry() == Base_Entry()

def test_get_keys():
    assert Base_Entry().keys() == Base_Entry().__dict__.keys()