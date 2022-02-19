from code_SRC.user import User
from tables.runs import Table_run
from tests.datas_fx import dicto_m
from tests.datas_fx import fill_db

class User_mock(User):
    """Class mock to avoid all api call.
        """
    @fill_db
    def __init__(self):
        self.username = "Test"
        self.id = "kjpdr4jq"
        self.runs = Table_run([dicto_m("run")["data"] for _ in range(3)])

class Test_init:
    model = User_mock()

    def test_mock_user(self):
        assert Test_init.model.username == "Test"

    def test_mock_str(self):
        assert isinstance(Test_init.model.runs, Table_run)

    def test_str(self):
        raise NotImplementedError