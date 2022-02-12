from random import shuffle
from tables.runs import Table_run
from entries.run_entry import Run
from tests.datas_fx import dicto_m, fill_db
from copy import deepcopy

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

    def test_len(self):
        assert len(Test_init.model) == 5


class Test_operations:

    def test_sum(self):
        assert sum(Test_init.model) == Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"])
    
    def test_mean(self):
        assert Test_init.model.mean() == (Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]) + Run(dicto_m("run")["data"]))/ 4

    def test_join(self):
        join_test = Table_run(liste_runs())
        for no, x in enumerate(["game", "system", "category"]):
            join_test.data[no][x] += "1"
        for attribute in ["game", "system", "category"]:
            assert len(join_test.join(attribute)) == 4

    def test_str(self):   
        for attribute in ["game", "system", "category", "time"]:
            for x in range(5):
                Test_init.model[x][attribute] += str(x) if isinstance(Test_init.model[x][attribute], str) else x
        body = "\n".join([f'{x+1:3} {Test_init.model[x]}' for x in range(5)])
        total =   "  ∑ 5      5                      5             55:56:05"
        moyenne = "MOY 1.0    1.0                    1.0           11:11:13"

        assert str(Test_init.model) == "\n".join([body, total, moyenne])

    def test_sort(self):
        backup = deepcopy(Test_init.model)
        for testing_key in ["game", "category", "system", "time"]:
            shuffle(Test_init.model.data)
            Test_init.model.sort(sorting_key=testing_key)
            assert Test_init.model == backup

    def test_median(self):
        shuffle(Test_init.model.data)
        assert Test_init.model.median("time") == Test_init.model.data[2]
