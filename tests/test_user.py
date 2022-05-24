from requests_mock import Mocker
from tables.solo_runs import Table_pb, Table_run
from tests.class_builder import build_user

class Test_user:
    def test_init(self, requests_mock:Mocker):

        test = build_user(requests_mock)
        for clé, identity in [("pbs", Table_pb),
                                ("pbs_l", Table_pb),
                                ("runs", Table_run),
                                ("runs_l", Table_run),
                                ("username", str)
                                ]:
            assert clé in test.__dict__.keys() and isinstance(test.__dict__[clé], identity)
