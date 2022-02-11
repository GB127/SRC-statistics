from tables.runs import Table_run
from entries.run_entry import Run
from tests.datas_fx import dicto_m, fill_db

def liste_runs():
    liste = []
    for x in range(3):
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

    def test_len(self):
        assert len(Test_init.model) == 3

    def test_median(self):
        raise NotImplementedError

    def test_str(self):     
        assert str(Test_init.model) == str(Run(dicto_m("run")["data"]))


class Test_others:
    @fill_db
    def test_sum(self):
        Test_others.model = Table_run(liste_runs())
        assert sum(Test_others.model) == Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"])
    
    def test_mean(self):
        assert Test_others.model.mean() == (Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]))/ 3

    def test_sort(self):
        raise NotImplementedError

    def test_join(self):
        raise NotImplementedError