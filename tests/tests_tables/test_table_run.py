from tables.runs import Table_run
from entries.run_entry import Run
from tests.datas_fx import dicto_m, fill_db

def liste_runs():
    liste = []
    for _ in range(5):
        liste.append(dicto_m("run")["data"])
    return liste

class Test_init:
    @fill_db
    def test_attributes(self):
        Test_init.model = Table_run(liste_runs())
        hasattr(Test_init.model, "data")

    def test_apply_Run(self):
        assert isinstance(Test_init.model[0], Run)

    def test_all_included(self):
        assert len(Test_init.model.data) == len(liste_runs())
