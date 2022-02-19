from random import shuffle
from tables.base import Base_Table
from entries.base import Base_Entry

def test_len():
    testing = Base_Table()
    testing.data = [1,2,3,4,5,6,7,8,9]
    assert len(testing) == 9

def test_getitem():
    testing = Base_Table()
    testing.data = [1,2,3]
    assert testing[0] == 1

def test_mean():
    testing = Base_Table()
    testing.data = [1,3,8]
    assert testing.mean() == 4

def test_sum():
    testing = Base_Table()
    testing.data = [1,1,1]
    assert testing.sum() == 3


def test_eq():
    testing1 = Base_Table()
    testing1.data = [1]
    testing2 = Base_Table()
    assert testing1 != testing2
    testing2.data = [1]
    assert testing1 == testing2


def test_sort():
    testing = Base_Table()
    testing.data = [{"allo":-x, "patate":x} for x in range(5)]
    shuffle(testing.data)
    testing.sort("allo") 
    assert testing.data == [{"allo":-x, "patate":x} for x in range(4,-1, -1)]
    shuffle(testing.data)
    testing.sort("patate")
    assert testing.data == [{"allo":-x, "patate":x} for x in range(5)]


def test_str():
    testing = Base_Table()
    testing.data = [1,2,3]
    stringed = "  1   1\n  2   2\n  3   3\n-------\n  ∑   6\n  X̅   2.0"
    assert str(testing) == stringed

def test_median():
    testing = Base_Table()
    testing.data = [{"allo":1},{"allo":10000}, {"allo":12}]
    assert testing.median("allo") == {"allo":12}


def test_join():
    testing = Base_Table()
    testing.data = [Base_Entry() for _ in range(6)]
    for index, dicto in enumerate([{"joined":lettre, "addition":chiffre} for lettre,chiffre in [("A", 1),("A", 2),("A", 3),("B", 4),("C", 5),("B", 6)]]):
        testing.data[index].__dict__ = dicto


    desired = Base_Table()
    desired.data = [Base_Entry() for _ in range(3)]
    for index, dicto in enumerate([{"joined":lettre, "addition":chiffre} for lettre,chiffre in [("A", 6),("B", 10),("C", 5),]]):
        desired.data[index].__dict__ = dicto
    for one in testing.join("joined"):
        assert any([one==x for x in desired]), f'{one.__dict__} | {[x.__dict__ for x in desired]}'