from entries.pb_entry import PB
from tests.datas_fx import fill_db, dicto_m
from tests.mocks import PB_mock


class Test_others:
    def test_str(self):
        testing_1 = PB_mock()
        assert str(testing_1) == 'syst   game                   Category        0:00:01     0:00:02 (200.00%)       2/20      (90.00%)'
        testing_1.category = {"Category1", "Category2"}
        assert str(testing_1) == 'syst   game                   2 category      0:00:01     0:00:02 (200.00%)       2/20      (90.00%)'
        testing_2 = PB_mock(include_level=True)
        assert str(testing_2) == 'syst   game                   level                  Category        0:00:01     0:00:02 (200.00%)       2/20      (90.00%)'
