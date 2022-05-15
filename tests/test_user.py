from requests_mock import Mocker
from tests.class_builder import build_user
from code_SRC.user import User

class Test_user:
    def test_init(self, requests_mock:Mocker):
        test = build_user(requests_mock)
        assert test.__dict__ == {"allo"}
