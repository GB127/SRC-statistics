from entries.pb_entry import PB
from tables.pbs import Table_pb
from entries.run_entry import Run
from tests.datas_fx import dicto_m, fill_db


def liste_runs():
    liste = []
    for _ in range(5):
        liste.append(dicto_m("pb")["data"])
    return liste

class Test_init:
    @fill_db
    def test_attributes(self):
        Test_init.model = Table_pb(liste_runs(), include_lvl=False)
        hasattr(Test_init.model, "data")

    def test_apply_Run(self):
        assert isinstance(Test_init.model[0], PB)

    def test_all_included(self):
        assert len(Test_init.model.data) == len(liste_runs())
