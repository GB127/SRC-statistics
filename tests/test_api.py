from code_SRC.api import api



def test_nordanix():
    nordanix_id = api.user_id("nordanix")
    nordanix = api.user_runs(nordanix_id)
    assert len(nordanix) == 3765