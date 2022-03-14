from code_SRC.user import User
from tables.runs import Table_run
from tables.pbs import Table_pb
from tests.datas_fx import dicto_m
from tests.datas_fx import fill_db

class User_mock(User):
    """Class mock to avoid all api calls.
        """
    @fill_db
    def __init__(self):
        self.username = "Test"
        self.id = "kjpdr4jq"
        self.runs = Table_run([dicto_m("run")["data"] for _ in range(3)])
        self.pbs = Table_pb([dicto_m("pb")["data"] for _ in range(3)])
