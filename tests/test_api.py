from code_SRC.api import api
from code_SRC.user import User



def off_test_nordanix():
    nordanix_id = api.user_id("nordanix")
    nordanix = User(nordanix_id)
    assert len(nordanix.runs) == 3765