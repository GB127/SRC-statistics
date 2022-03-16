from random import shuffle
from tables.base import Base_Table
from entries.base import Base_Entry


class Test_op:
    def test_len(self):
        testing = Base_Table()
        testing.data = [1,2,3,4,5,6,7,8,9]
        assert len(testing) == 9

    def test_getitem(self):
        testing = Base_Table()
        testing.data = [1,2,3]
        assert testing[0] == 1

    def test_mean(self):
        testing = Base_Table()
        testing.data = [1,3,8]
        assert testing.mean() == 4

    def test_sum(self):
        testing = Base_Table()
        testing.data = [1,1,1]
        assert testing.sum() == 3


    def test_eq(self):
        testing1 = Base_Table()
        testing1.data = [1]
        testing2 = Base_Table()
        assert testing1 != testing2
        testing2.data = [1]
        assert testing1 == testing2


    def test_sort(self):
        testing = Base_Table()
        testing.data = [{"allo":-x, "patate":x} for x in range(5)]
        shuffle(testing.data)
        testing.sort("allo") 
        assert testing.data == [{"allo":-x, "patate":x} for x in range(4,-1, -1)]
        shuffle(testing.data)
        testing.sort("patate")
        assert testing.data == [{"allo":-x, "patate":x} for x in range(5)]



    def test_median(self):
        testing = Base_Table()
        testing.data = [{"allo":1}, {"allo":10000}, {"allo":12}]
        assert testing.median("allo") == {"allo":12}




class Test_misc:
    def test_str(self):
        testing = Base_Table()
        testing.data = [1,2,3]
        stringed = "  1   1\n  2   2\n  3   3\n-------\n  ∑   6\n  X̅   2.0"
        assert str(testing) == stringed
