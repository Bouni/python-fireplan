import logging
import string
import random
import fireplan


def test_token():
    token = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(64)
    )
    fp = fireplan.Fireplan(token)
    assert fp.headers == {"utoken": token, "content-type": "application/json"}

