from tables.runs import Table_run
from entries.run_entry import Run

def liste_runs():
    pass

class Test_init:
    model = Table_run(liste_runs())
    def test_attributes(self):
        hasattr(Test_init.model, "data")

    def test_apply_Run(self):
        assert isinstance(Test_init.model[0], Run)

    def test_exclude_level(self):
        raise NotImplementedError

    def test_include_level(self):
        raise NotImplementedError

    def test_all_included(self):
        assert len(Test_init.model.data) == len(liste_runs())

class Test_others:
    def test_sum(self):
        raise NotImplementedError
    
    def test_mean(self):
        raise NotImplementedError

    def test_median(self):
        raise NotImplementedError

    def test_str(self):
        raise NotImplementedError

    def test_sort(self):
        raise NotImplementedError