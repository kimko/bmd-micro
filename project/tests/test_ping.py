# project/tests/test_ping.py
"""Test the ping rounte
"""

import json


def test_ping(test_app):
    client = test_app.test_client()
    resp = client.get("/ping")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "success" in data["status"]
