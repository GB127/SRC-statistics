from tests.test_datas import run_base, run_base2, run_subcat, run_level
from code_SRC.table_run import Table_Runs
from copy import copy
from code_SRC.run_entry import Run


class Test_table_Runs:
    classe_nolvl = Table_Runs([copy(run_level), copy(run_base), copy(run_base2)], level=False)
    classe_lvl = Table_Runs([copy(run_level), copy(run_base), copy(run_base2), copy(run_subcat)], level=True)

    def test_table_run_init_nolvl(self):
        assert Test_table_Runs.classe_nolvl.liste == [Run(copy(run_base)), Run(copy(run_base2)), Run(copy(run_subcat))]

    def test_table_run_init_lvl(self):
        assert Test_table_Runs.classe_lvl.liste == [Run(copy(run_level))]

    def test_table_run_sort(self):
        raise NotImplementedError("Testing case not written")

    def test_table_run_str(self):
        raise NotImplementedError("Testing case not written")

    def test_table_run_len(self):
        assert len(Test_table_Runs.classe_nolvl) == 2
